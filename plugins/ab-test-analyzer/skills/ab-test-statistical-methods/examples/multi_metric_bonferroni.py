"""
multi_metric_bonferroni.py
==========================
Complete worked example: simultaneous testing of 5 metrics with Bonferroni correction.

Scenario
--------
A growth team ran an A/B test on a redesigned onboarding flow.
They tracked 5 metrics simultaneously:
  1. Signup conversion rate  (primary)
  2. Day-1 retention         (guardrail)
  3. Day-7 retention         (secondary)
  4. Profile completion rate (secondary)
  5. First-purchase rate     (secondary)

Pre-specified family-wise alpha: 0.05
Pre-specified MDE: varies by metric (see METRICS below)

Bonferroni-adjusted alpha per metric: 0.05 / 5 = 0.01

Expected false positive without correction:
  P(at least one false positive in 5 tests at alpha=0.05) = 1 - 0.95^5 ≈ 22.6%
With Bonferroni correction at alpha=0.01:
  P(at least one false positive) ≤ 0.05  (guaranteed by construction)
"""

import numpy as np
from scipy import stats


# ── Experiment data ───────────────────────────────────────────────────────────
# Each metric: name, type, control users, control successes,
#              treatment users, treatment successes, MDE (absolute)

METRICS = [
    {
        "name": "Signup conversion rate",
        "role": "primary",
        "n_control": 10_204,
        "successes_control": 510,     # 5.00%
        "n_treatment": 10_187,
        "successes_treatment": 571,   # 5.60%
        "mde": 0.005,                 # 0.5pp
    },
    {
        "name": "Day-1 retention",
        "role": "guardrail",
        "n_control": 10_204,
        "successes_control": 6_735,   # 66.0%
        "n_treatment": 10_187,
        "successes_treatment": 6_680, # 65.6%  — slight dip, investigate
        "mde": 0.01,                  # 1.0pp
    },
    {
        "name": "Day-7 retention",
        "role": "secondary",
        "n_control": 10_204,
        "successes_control": 3_061,   # 30.0%
        "n_treatment": 10_187,
        "successes_treatment": 3_157, # 31.0%
        "mde": 0.01,
    },
    {
        "name": "Profile completion rate",
        "role": "secondary",
        "n_control": 10_204,
        "successes_control": 4_082,   # 40.0%
        "n_treatment": 10_187,
        "successes_treatment": 4_258, # 41.8%
        "mde": 0.015,
    },
    {
        "name": "First-purchase rate",
        "role": "secondary",
        "n_control": 10_204,
        "successes_control": 1_020,   # 10.0%
        "n_treatment": 10_187,
        "successes_treatment": 1_060, # 10.4%
        "mde": 0.01,
    },
]

ALPHA_FAMILY = 0.05


# ── Analysis ──────────────────────────────────────────────────────────────────

def compute_proportion_test(m, alpha_adjusted):
    """Run a two-proportion z-test for one metric and return result dict."""
    n_c = m["n_control"]
    s_c = m["successes_control"]
    n_t = m["n_treatment"]
    s_t = m["successes_treatment"]

    p_c = s_c / n_c
    p_t = s_t / n_t
    delta = p_t - p_c
    relative_lift = delta / p_c if p_c > 0 else 0.0

    p_pooled = (s_c + s_t) / (n_c + n_t)
    se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_c + 1 / n_t))
    se_unpooled = np.sqrt(p_c*(1-p_c)/n_c + p_t*(1-p_t)/n_t)

    z_stat = delta / se_pooled if se_pooled > 0 else 0.0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    z_crit_adj = stats.norm.ppf(1 - alpha_adjusted / 2)
    ci_lower = delta - z_crit_adj * se_unpooled
    ci_upper = delta + z_crit_adj * se_unpooled

    sig_adjusted = p_value < alpha_adjusted
    sig_unadjusted = p_value < ALPHA_FAMILY
    practical = abs(delta) >= m["mde"] if sig_adjusted and ci_lower > 0 else False

    return {
        "name": m["name"],
        "role": m["role"],
        "p_control": p_c,
        "p_treatment": p_t,
        "delta": delta,
        "relative_lift": relative_lift,
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "sig_adjusted": sig_adjusted,
        "sig_unadjusted": sig_unadjusted,
        "practical": practical,
        "mde": m["mde"],
    }


def format_p(p):
    return "< 0.0001" if p < 0.0001 else f"{p:.4f}"


def run_analysis():
    k = len(METRICS)
    alpha_adjusted = ALPHA_FAMILY / k

    results = [compute_proportion_test(m, alpha_adjusted) for m in METRICS]

    # ── Header ────────────────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("MULTI-METRIC A/B TEST — BONFERRONI-CORRECTED ANALYSIS")
    print("=" * 70)
    print()
    print("1. TEST SELECTED")
    print("   Two-proportion z-test applied to each metric independently.")
    print("   Bonferroni correction applied across all metrics simultaneously.")
    print()
    print(f"   Metrics in family:       {k}")
    print(f"   Family-wise alpha:        {ALPHA_FAMILY}")
    print(f"   Adjusted alpha per test:  {alpha_adjusted:.4f}  "
          f"(= {ALPHA_FAMILY} / {k})")
    print()
    print("   Without correction, testing {k} metrics at alpha=0.05 yields a".format(k=k))
    fp_prob = 1 - (1 - ALPHA_FAMILY)**k
    print(f"   {fp_prob:.1%} chance of at least one false positive.")
    print("   Bonferroni correction controls this to <= 5%.")
    print()

    # ── Per-metric results ────────────────────────────────────────────────────
    print("2. TEST STATISTIC AND P-VALUE — PER METRIC")
    print()
    for r in results:
        role_tag = f"[{r['role'].upper()}]"
        print(f"   {r['name']}  {role_tag}")
        print(f"   Control:   {r['p_control']:.4%} | Treatment: {r['p_treatment']:.4%}")
        print(f"   z = {r['z_stat']:.4f}  |  p = {format_p(r['p_value'])}")
        print(f"   Significant at adj. alpha ({alpha_adjusted:.4f}): "
              f"{'YES' if r['sig_adjusted'] else 'NO'}")
        print()

    # ── Confidence intervals ──────────────────────────────────────────────────
    print("3. BONFERRONI-ADJUSTED CI ON EFFECT (per metric)")
    print(f"   (CI computed at {(1 - alpha_adjusted)*100:.1f}% level — "
          f"adjusted for family-wise error rate)")
    print()
    col_w = 32
    print(f"   {'Metric':<{col_w}} {'Delta':>9}  {'Adj. CI':>22}  {'CI > 0?':>8}")
    print(f"   {'-'*col_w} {'-'*9}  {'-'*22}  {'-'*8}")
    for r in results:
        ci_str = f"[{r['ci_lower']:+.3%}, {r['ci_upper']:+.3%}]"
        above_zero = "YES" if r['ci_lower'] > 0 else ("NO" if r['ci_upper'] < 0 else "crosses")
        print(f"   {r['name']:<{col_w}} {r['delta']:>+9.4%}  {ci_str:>22}  {above_zero:>8}")
    print()

    # ── Effect sizes ──────────────────────────────────────────────────────────
    print("4. EFFECT SIZE")
    print()
    for r in results:
        print(f"   {r['name']}")
        print(f"   Relative lift: {r['relative_lift']:+.2%}")
        print(f"   MDE specified: {r['mde']:.4%}")
        clears = "YES" if r['sig_adjusted'] and r['ci_lower'] > 0 and r['practical'] else "NO"
        print(f"   Practical (clears MDE and CI > 0): {clears}")
        print()

    # ── Summary table ─────────────────────────────────────────────────────────
    print("5. SUMMARY TABLE")
    print()
    print(f"   {'Metric':<{col_w}} {'p-value':>10} {'p<0.05?':>8} {'p<adj?':>7} {'Ship?':>6}")
    print(f"   {'-'*col_w} {'-'*10} {'-'*8} {'-'*7} {'-'*6}")
    for r in results:
        unadj = "YES" if r['sig_unadjusted'] else "no"
        adj = "YES" if r['sig_adjusted'] else "no"
        ship = "YES" if r['sig_adjusted'] and r['ci_lower'] > 0 and r['practical'] else "no"
        print(f"   {r['name']:<{col_w}} {format_p(r['p_value']):>10} "
              f"{unadj:>8} {adj:>7} {ship:>6}")
    print()

    # ── False positive flags ──────────────────────────────────────────────────
    false_positives = [r for r in results if r['sig_unadjusted'] and not r['sig_adjusted']]
    if false_positives:
        print("   FALSE POSITIVE FLAGS")
        print("   The following metrics appear significant WITHOUT correction")
        print("   but do NOT clear the Bonferroni-adjusted threshold.")
        print("   Do NOT act on these results.")
        print()
        for r in false_positives:
            print(f"   - {r['name']}: p = {format_p(r['p_value'])}  "
                  f"(required p < {alpha_adjusted:.4f})")
        print()

    # ── Guardrail check ───────────────────────────────────────────────────────
    guardrails = [r for r in results if r['role'] == 'guardrail']
    print("   GUARDRAIL CHECK")
    any_guardrail_violated = False
    for r in guardrails:
        if r['sig_adjusted'] and r['delta'] < 0:
            print(f"   STOP: {r['name']} has degraded significantly.")
            print(f"   Delta: {r['delta']:+.4%}. Stop the experiment immediately.")
            any_guardrail_violated = True
        elif r['sig_unadjusted'] and r['delta'] < 0 and not r['sig_adjusted']:
            print(f"   WATCH: {r['name']} shows a negative trend (p = {format_p(r['p_value'])}).")
            print(f"   Not significant after correction but warrants monitoring.")
        else:
            print(f"   OK: {r['name']} — no significant degradation detected.")
    print()

    # ── Recommendation ────────────────────────────────────────────────────────
    print("6. RECOMMENDATION")
    print()

    primary = next((r for r in results if r['role'] == 'primary'), None)

    if any_guardrail_violated:
        print("   STOP THE EXPERIMENT. A guardrail metric has degraded significantly.")
        print("   Do not ship regardless of primary metric result.")
        print("   Investigate the root cause of guardrail degradation before proceeding.")
    elif primary and primary['sig_adjusted'] and primary['ci_lower'] > 0 and primary['practical']:
        print(f"   The primary metric ({primary['name']}) is significant after")
        print(f"   Bonferroni correction (p = {format_p(primary['p_value'])}, "
              f"adj. alpha = {alpha_adjusted:.4f})")
        print(f"   and the CI lower bound clears the MDE.")
        sig_secondaries = [r for r in results
                           if r['role'] == 'secondary' and r['sig_adjusted'] and r['ci_lower'] > 0]
        if sig_secondaries:
            names = ", ".join(r['name'] for r in sig_secondaries)
            print(f"   Supporting signals from: {names}.")
        print()
        print("   Ship the redesigned onboarding flow.")
        print("   Monitor guardrail metrics for 7 days post-launch.")
    elif primary and not primary['sig_adjusted']:
        print(f"   The primary metric ({primary['name']}) did not reach significance")
        print(f"   after Bonferroni correction (p = {format_p(primary['p_value'])}).")
        print()
        print("   Do not ship. Secondary metric wins do not substitute for")
        print("   a failed primary hypothesis. If secondary metrics are promising,")
        print("   consider a follow-up experiment with the secondary as the primary.")
    else:
        print("   Do not ship. Review results and consult the decision framework")
        print("   in SKILL.md Step 7 for the appropriate next step.")

    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    run_analysis()
