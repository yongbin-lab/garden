"""
proportion_test.py
==================
Complete worked example: two-proportion z-test on signup conversion data.

Scenario
--------
An e-commerce product team ran an A/B test on their signup flow.
- Control: original signup page
- Treatment: simplified signup page with fewer required fields
- Primary metric: signup conversion rate (binary: did the user sign up?)
- Pre-specified MDE: 0.5 percentage points absolute (0.005)
- Pre-specified alpha: 0.05 (two-tailed)
- Pre-specified power: 80%

The experiment ran for 14 days and collected the following data.
"""

import numpy as np
from scipy import stats


# ── Sample data ───────────────────────────────────────────────────────────────

CONTROL = {
    "name": "Control (original signup)",
    "n": 8_412,
    "conversions": 421,
}

TREATMENT = {
    "name": "Treatment (simplified signup)",
    "n": 8_389,
    "conversions": 487,
}

MDE = 0.005       # 0.5 percentage points absolute
ALPHA = 0.05      # Two-tailed significance level
POWER_TARGET = 0.80


# ── Core computations ─────────────────────────────────────────────────────────

def run_two_proportion_ztest(control, treatment, alpha, mde, power_target):
    n_c = control["n"]
    conv_c = control["conversions"]
    n_t = treatment["n"]
    conv_t = treatment["conversions"]

    p_c = conv_c / n_c
    p_t = conv_t / n_t
    delta = p_t - p_c
    relative_lift = delta / p_c

    # Pooled proportion for test statistic
    p_pooled = (conv_c + conv_t) / (n_c + n_t)
    se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_c + 1 / n_t))

    # Unpooled SE for confidence interval
    se_unpooled = np.sqrt(p_c * (1 - p_c) / n_c + p_t * (1 - p_t) / n_t)

    z_stat = delta / se_pooled
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = delta - z_crit * se_unpooled
    ci_upper = delta + z_crit * se_unpooled

    # Practical significance: does the CI lower bound clear the MDE?
    practical_significant = ci_lower >= mde

    # Observed power (post-hoc, for reference only — do not use to justify stopping)
    z_beta = (abs(delta) / se_pooled) - z_crit
    observed_power = stats.norm.cdf(z_beta)

    # Required sample size for pre-specified MDE
    p_treatment_target = p_c + mde
    p_avg = (p_c + p_treatment_target) / 2
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power_target)
    n_required = int(np.ceil(
        (z_alpha * np.sqrt(2 * p_avg * (1 - p_avg)) +
         z_power * np.sqrt(p_c*(1-p_c) + p_treatment_target*(1-p_treatment_target)))**2
        / mde**2
    ))

    # ── Output: matches Output Format Contract ────────────────────────────────

    print()
    print("=" * 65)
    print("A/B TEST ANALYSIS — SIGNUP CONVERSION RATE")
    print("=" * 65)
    print()
    print("1. TEST SELECTED")
    print("   Two-proportion z-test.")
    print("   Reason: metric is binary (user signed up: yes/no).")
    print()
    print("2. TEST STATISTIC AND P-VALUE")
    print(f"   Control rate:    {p_c:.4%}  ({conv_c:,} / {n_c:,})")
    print(f"   Treatment rate:  {p_t:.4%}  ({conv_t:,} / {n_t:,})")
    print(f"   z = {z_stat:.4f}")
    p_str = "< 0.0001" if p_value < 0.0001 else f"{p_value:.4f}"
    print(f"   p = {p_str}")
    print(f"   Significant at alpha={alpha} (two-tailed): {'YES' if p_value < alpha else 'NO'}")
    print()
    print("3. 95% CONFIDENCE INTERVAL ON EFFECT")
    print(f"   Absolute delta: {delta:+.4%}")
    print(f"   95% CI:         [{ci_lower:+.4%}, {ci_upper:+.4%}]")
    if ci_lower < 0 < ci_upper:
        print("   CI crosses zero: YES — result is inconclusive.")
    else:
        print("   CI does not cross zero.")
    print()
    print("4. EFFECT SIZE")
    print(f"   Relative lift: {relative_lift:+.2%}")
    print(f"   (Treatment conversion rate is {relative_lift:+.2%} relative to control.)")
    print()
    print("5. PRACTICAL SIGNIFICANCE CHECK vs MDE")
    print(f"   Pre-specified MDE: {mde:.4%} absolute ({mde/p_c:.1%} relative)")
    print(f"   Observed delta:    {abs(delta):.4%} absolute")
    print(f"   CI lower bound:    {ci_lower:.4%}")
    if practical_significant:
        print(f"   Clears MDE: YES — even the lower bound of the CI exceeds MDE.")
    else:
        print(f"   Clears MDE: NO — CI lower bound is below MDE.")
        print(f"   The effect may be real but smaller than what was deemed worth shipping.")
    print()
    print("6. RECOMMENDATION")
    if p_value < alpha and ci_lower > 0 and practical_significant:
        print("   Ship the simplified signup page. The improvement is statistically")
        print(f"   significant (p={p_str}) and the entire 95% CI is above the")
        print(f"   pre-specified MDE of {mde:.4%}. The relative lift of {relative_lift:+.2%}")
        print("   is meaningful at this traffic volume.")
    elif p_value < alpha and ci_lower > 0 and not practical_significant:
        print("   Caution. The result is statistically significant but the lower bound")
        print("   of the CI is below the pre-specified MDE. The true effect may be")
        print("   smaller than required to justify implementation cost. Discuss with")
        print("   the team whether the observed lift is sufficient before shipping.")
    elif ci_lower < 0 < ci_upper:
        print("   Do not ship. The CI crosses zero. There is not enough evidence")
        print("   of a positive effect. Extend the experiment or reconsider the design.")
    else:
        print("   Do not ship. The result is not statistically significant.")
    print()
    print("─" * 65)
    print("SUPPLEMENTARY INFORMATION (for context, not decision-making)")
    print(f"   Observed power:          {observed_power:.1%}")
    print(f"   Required n per variant   ")
    print(f"   (for 80% power at MDE):  {n_required:,}")
    print(f"   Actual n per variant:    {n_c:,} control, {n_t:,} treatment")
    if n_c >= n_required and n_t >= n_required:
        print("   Sample size was adequate for the pre-specified MDE.")
    else:
        print("   WARNING: Sample size was below the required n for 80% power at MDE.")
    print("=" * 65)
    print()


if __name__ == "__main__":
    run_two_proportion_ztest(CONTROL, TREATMENT, ALPHA, MDE, POWER_TARGET)
