# Python Templates — Ready-to-Run Statistical Functions

All functions below are self-contained and print output matching the Output Format Contract defined in `SKILL.md`. Copy the relevant function, supply the data, and run directly.

Dependencies: scipy, numpy, pandas, statsmodels. Run `scripts/setup-stats-env.sh` if any are missing.

---

## Template 1: Two-Proportion Z-Test with CI and Relative Lift

```python
import numpy as np
from scipy import stats


def two_proportion_ztest(n_control, conversions_control, n_treatment, conversions_treatment,
                         alpha=0.05, mde=None):
    """
    Two-proportion z-test for binary metrics (conversion rate, click-through rate, etc.).

    Parameters
    ----------
    n_control : int
        Number of users in control group.
    conversions_control : int
        Number of conversions (successes) in control group.
    n_treatment : int
        Number of users in treatment group.
    conversions_treatment : int
        Number of conversions (successes) in treatment group.
    alpha : float
        Significance level. Default 0.05 (two-tailed).
    mde : float or None
        Minimum detectable effect as absolute percentage points (e.g., 0.01 = 1pp).
        If provided, compares observed effect to MDE for practical significance check.
    """
    p_c = conversions_control / n_control
    p_t = conversions_treatment / n_treatment
    delta = p_t - p_c
    relative_lift = delta / p_c

    # Pooled proportion for z-test
    p_pooled = (conversions_control + conversions_treatment) / (n_control + n_treatment)
    se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_control + 1 / n_treatment))

    # Unpooled SE for confidence interval
    se_unpooled = np.sqrt(p_c * (1 - p_c) / n_control + p_t * (1 - p_t) / n_treatment)

    z_stat = delta / se_pooled
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = delta - z_crit * se_unpooled
    ci_upper = delta + z_crit * se_unpooled

    # Practical significance check
    practical = None
    if mde is not None:
        practical = abs(delta) >= mde

    print("=" * 60)
    print("TEST SELECTED: Two-proportion z-test")
    print("  Reason: Metric is binary (conversion per user).")
    print()
    print(f"  Control:   {conversions_control:,} / {n_control:,} = {p_c:.4%}")
    print(f"  Treatment: {conversions_treatment:,} / {n_treatment:,} = {p_t:.4%}")
    print()
    print(f"TEST STATISTIC AND P-VALUE")
    print(f"  z = {z_stat:.4f}")
    print(f"  p = {p_value:.4f}" + (" (< 0.0001)" if p_value < 0.0001 else ""))
    print(f"  Significant at alpha={alpha}: {'YES' if p_value < alpha else 'NO'}")
    print()
    print(f"95% CONFIDENCE INTERVAL ON EFFECT")
    print(f"  Absolute delta:  [{ci_lower:+.4%}, {ci_upper:+.4%}]")
    print(f"  CI crosses zero: {'YES — result inconclusive' if ci_lower < 0 < ci_upper else 'NO'}")
    print()
    print(f"EFFECT SIZE")
    print(f"  Relative lift: {relative_lift:+.2%}")
    print()
    if mde is not None:
        print(f"PRACTICAL SIGNIFICANCE CHECK")
        print(f"  MDE specified: {mde:.4%} absolute")
        print(f"  Observed delta: {abs(delta):.4%} absolute")
        print(f"  Clears MDE: {'YES' if practical else 'NO'}")
        print()
    print("RECOMMENDATION")
    if p_value < alpha and ci_lower > 0 and (mde is None or practical):
        print("  Ship. The result is statistically and practically significant.")
    elif p_value < alpha and ci_lower > 0 and not practical:
        print("  Do not ship. Effect is statistically significant but below MDE.")
        print("  The effect is too small to justify implementation cost.")
    elif ci_lower < 0 < ci_upper:
        print("  Do not ship. The confidence interval crosses zero.")
        print("  There is insufficient evidence of a positive effect.")
    else:
        print("  Do not ship. The result is not statistically significant.")
    print("=" * 60)


# Example usage
if __name__ == "__main__":
    two_proportion_ztest(
        n_control=4820, conversions_control=241,
        n_treatment=4956, conversions_treatment=297,
        alpha=0.05, mde=0.005
    )
```

---

## Template 2: Welch's T-Test with Cohen's d

```python
import numpy as np
from scipy import stats


def welch_ttest(control_data, treatment_data, alpha=0.05, mde=None):
    """
    Welch's independent t-test for continuous metrics.
    Does NOT assume equal variance (correct default for A/B tests).

    Parameters
    ----------
    control_data : array-like
        Raw observations for the control group.
    treatment_data : array-like
        Raw observations for the treatment group.
    alpha : float
        Significance level. Default 0.05 (two-tailed).
    mde : float or None
        Minimum detectable effect as an absolute difference in the same units as the data.
    """
    control = np.array(control_data)
    treatment = np.array(treatment_data)

    n_c, n_t = len(control), len(treatment)
    mean_c, mean_t = np.mean(control), np.mean(treatment)
    std_c, std_t = np.std(control, ddof=1), np.std(treatment, ddof=1)

    t_stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)

    # Welch-Satterthwaite degrees of freedom for CI
    df = (std_c**2/n_c + std_t**2/n_t)**2 / (
        (std_c**2/n_c)**2/(n_c-1) + (std_t**2/n_t)**2/(n_t-1)
    )
    t_crit = stats.t.ppf(1 - alpha/2, df=df)
    se_diff = np.sqrt(std_c**2/n_c + std_t**2/n_t)
    delta = mean_t - mean_c
    ci_lower = delta - t_crit * se_diff
    ci_upper = delta + t_crit * se_diff

    # Cohen's d (pooled standard deviation)
    pooled_std = np.sqrt(((n_c - 1)*std_c**2 + (n_t - 1)*std_t**2) / (n_c + n_t - 2))
    cohens_d = delta / pooled_std

    d_label = (
        "negligible" if abs(cohens_d) < 0.2 else
        "small" if abs(cohens_d) < 0.5 else
        "medium" if abs(cohens_d) < 0.8 else
        "large"
    )

    practical = None
    if mde is not None:
        practical = abs(delta) >= mde

    print("=" * 60)
    print("TEST SELECTED: Welch's independent t-test")
    print("  Reason: Continuous metric, n >= 30 in both groups,")
    print("  equal variance NOT assumed.")
    print()
    print(f"  Control:   n={n_c:,}, mean={mean_c:.4f}, std={std_c:.4f}")
    print(f"  Treatment: n={n_t:,}, mean={mean_t:.4f}, std={std_t:.4f}")
    print()
    print("TEST STATISTIC AND P-VALUE")
    print(f"  t = {t_stat:.4f}  (df = {df:.1f})")
    p_str = "< 0.0001" if p_value < 0.0001 else f"{p_value:.4f}"
    print(f"  p = {p_str}")
    print(f"  Significant at alpha={alpha}: {'YES' if p_value < alpha else 'NO'}")
    print()
    print("95% CONFIDENCE INTERVAL ON EFFECT")
    print(f"  Absolute delta: [{ci_lower:+.4f}, {ci_upper:+.4f}]")
    print(f"  CI crosses zero: {'YES — result inconclusive' if ci_lower < 0 < ci_upper else 'NO'}")
    print()
    print("EFFECT SIZE")
    print(f"  Cohen's d = {cohens_d:.4f}  ({d_label})")
    print()
    if mde is not None:
        print("PRACTICAL SIGNIFICANCE CHECK")
        print(f"  MDE specified: {mde:.4f}")
        print(f"  Observed delta: {abs(delta):.4f}")
        print(f"  Clears MDE: {'YES' if practical else 'NO'}")
        print()
    print("RECOMMENDATION")
    if p_value < alpha and ci_lower > 0 and (mde is None or practical):
        print("  Ship. Statistically and practically significant positive effect.")
    elif p_value < alpha and ci_lower > 0 and not practical:
        print("  Do not ship. Significant but below MDE. Effect too small to justify cost.")
    elif ci_lower < 0 < ci_upper:
        print("  Do not ship. CI crosses zero — inconclusive.")
    else:
        print("  Do not ship. Result not statistically significant.")
    print("=" * 60)
```

---

## Template 3: Mann-Whitney U with Rank-Biserial Effect Size

```python
import numpy as np
from scipy import stats


def mann_whitney_test(control_data, treatment_data, alpha=0.05):
    """
    Mann-Whitney U test for non-parametric comparison.
    Use when data is non-normal and n < 30, or when distribution is severely skewed.

    Parameters
    ----------
    control_data : array-like
    treatment_data : array-like
    alpha : float
    """
    control = np.array(control_data)
    treatment = np.array(treatment_data)
    n_c, n_t = len(control), len(treatment)

    u_stat, p_value = stats.mannwhitneyu(control, treatment, alternative='two-sided')

    # Rank-biserial correlation as effect size
    r = 1 - (2 * u_stat) / (n_c * n_t)

    r_label = (
        "negligible" if abs(r) < 0.1 else
        "small" if abs(r) < 0.3 else
        "medium" if abs(r) < 0.5 else
        "large"
    )

    print("=" * 60)
    print("TEST SELECTED: Mann-Whitney U test (non-parametric)")
    print("  Reason: Data is non-normal or sample size is small.")
    print("  Tests whether treatment distribution is stochastically")
    print("  greater than control distribution.")
    print()
    print(f"  Control:   n={n_c}, median={np.median(control):.4f}")
    print(f"  Treatment: n={n_t}, median={np.median(treatment):.4f}")
    print()
    print("TEST STATISTIC AND P-VALUE")
    print(f"  U = {u_stat:.1f}")
    p_str = "< 0.0001" if p_value < 0.0001 else f"{p_value:.4f}"
    print(f"  p = {p_str}")
    print(f"  Significant at alpha={alpha}: {'YES' if p_value < alpha else 'NO'}")
    print()
    print("NOTE: Mann-Whitney U does not produce a CI on the mean difference.")
    print("  Consider bootstrap CI for effect magnitude. See Template 6.")
    print()
    print("EFFECT SIZE")
    print(f"  Rank-biserial r = {r:.4f}  ({r_label})")
    print(f"  Interpretation: treatment observation is larger than a random")
    print(f"  control observation {(r + 1)/2:.1%} of the time.")
    print()
    print("RECOMMENDATION")
    if p_value < alpha and r > 0:
        print("  Treatment shows a statistically significant positive shift.")
        print("  Verify practical significance via bootstrap CI before shipping.")
    elif p_value < alpha and r < 0:
        print("  Treatment shows a statistically significant NEGATIVE shift.")
        print("  Do not ship. Investigate degradation.")
    else:
        print("  No statistically significant difference detected.")
    print("=" * 60)
```

---

## Template 4: Sample Size Calculator

```python
import numpy as np
from scipy import stats


def sample_size_proportion(p_baseline, mde, alpha=0.05, power=0.80):
    """
    Required sample size per variant for a two-proportion z-test.

    Parameters
    ----------
    p_baseline : float   Baseline conversion rate (e.g., 0.05 for 5%)
    mde : float          Minimum detectable effect, absolute pp (e.g., 0.005 for 0.5pp)
    alpha : float        Significance level (default 0.05)
    power : float        Desired power (default 0.80)
    """
    p_treatment = p_baseline + mde
    p_avg = (p_baseline + p_treatment) / 2
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    n = (z_alpha * np.sqrt(2 * p_avg * (1 - p_avg)) +
         z_beta * np.sqrt(p_baseline*(1-p_baseline) + p_treatment*(1-p_treatment)))**2 / mde**2
    return int(np.ceil(n))


def sample_size_continuous(mean_control, std_control, mde, alpha=0.05, power=0.80):
    """
    Required sample size per variant for Welch's t-test.

    Parameters
    ----------
    mean_control : float   Control group mean
    std_control : float    Control group standard deviation (use treatment std if known)
    mde : float            Minimum detectable effect in same units as mean
    alpha : float
    power : float
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    n = 2 * ((z_alpha + z_beta) * std_control / mde)**2
    return int(np.ceil(n))


def print_sample_size_report(current_n, daily_traffic_per_variant,
                              n_required, metric_type):
    days_run = current_n / daily_traffic_per_variant
    days_needed = n_required / daily_traffic_per_variant
    days_remaining = max(0, days_needed - days_run)

    print("=" * 60)
    print("SAMPLE SIZE AND RUNTIME ESTIMATE")
    print(f"  Metric type:              {metric_type}")
    print(f"  Required n per variant:   {n_required:,}")
    print(f"  Current n per variant:    {current_n:,}")
    print(f"  Days run so far:          {days_run:.1f}")
    print(f"  Days needed total:        {days_needed:.1f}")
    print(f"  Estimated days remaining: {days_remaining:.1f}")
    if days_remaining > days_run * 2:
        print()
        print("  WARNING: Required additional runtime is more than 2x")
        print("  what has already run. Consider redesigning the experiment")
        print("  with a larger MDE or reducing the number of variants.")
    print("=" * 60)
```

---

## Template 5: Bonferroni-Corrected Multi-Metric Analysis Loop

```python
import numpy as np
from scipy import stats


def bonferroni_multi_metric(metrics, alpha_family=0.05):
    """
    Run multiple two-proportion z-tests with Bonferroni correction.

    Parameters
    ----------
    metrics : list of dict, each with keys:
        'name'                  : str
        'n_control'             : int
        'conversions_control'   : int
        'n_treatment'           : int
        'conversions_treatment' : int
    alpha_family : float
        Family-wise error rate to control. Default 0.05.
    """
    k = len(metrics)
    alpha_adjusted = alpha_family / k

    print("=" * 60)
    print(f"BONFERRONI-CORRECTED MULTI-METRIC ANALYSIS")
    print(f"  Metrics tested:       {k}")
    print(f"  Family alpha:         {alpha_family}")
    print(f"  Adjusted alpha each:  {alpha_adjusted:.4f}  (= {alpha_family} / {k})")
    print()

    results = []
    for m in metrics:
        p_c = m['conversions_control'] / m['n_control']
        p_t = m['conversions_treatment'] / m['n_treatment']
        delta = p_t - p_c
        p_pooled = (m['conversions_control'] + m['conversions_treatment']) / (
            m['n_control'] + m['n_treatment'])
        se = np.sqrt(p_pooled * (1 - p_pooled) * (1/m['n_control'] + 1/m['n_treatment']))
        z = delta / se if se > 0 else 0.0
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        significant = p_value < alpha_adjusted
        results.append({
            'name': m['name'],
            'delta': delta,
            'p_value': p_value,
            'significant': significant
        })

    # Header
    print(f"  {'Metric':<30} {'Delta':>10} {'p-value':>10} {'Clears adj. alpha':>20}")
    print(f"  {'-'*30} {'-'*10} {'-'*10} {'-'*20}")

    significant_count = 0
    for r in results:
        sig_str = "YES" if r['significant'] else "no"
        p_str = "< 0.0001" if r['p_value'] < 0.0001 else f"{r['p_value']:.4f}"
        print(f"  {r['name']:<30} {r['delta']:>+10.4%} {p_str:>10} {sig_str:>20}")
        if r['significant']:
            significant_count += 1

    print()
    print(f"  {significant_count} of {k} metrics cleared the adjusted threshold "
          f"(alpha = {alpha_adjusted:.4f}).")
    print()
    print("  NOTE: Metrics that cleared the unadjusted threshold (p < 0.05)")
    print("  but NOT the adjusted threshold are NOT significant. Do not act on them.")

    unadj_false_positives = [r for r in results
                             if r['p_value'] < alpha_family and not r['significant']]
    if unadj_false_positives:
        print()
        print("  POTENTIAL FALSE POSITIVES (significant without correction,")
        print("  NOT significant after Bonferroni):")
        for r in unadj_false_positives:
            print(f"    - {r['name']}: p = {r['p_value']:.4f}")

    print("=" * 60)
    return results
```

---

## Template 6: Bootstrap CI

```python
import numpy as np


def bootstrap_ci(control_data, treatment_data, statistic_fn=None,
                 n_bootstrap=10000, alpha=0.05, seed=42):
    """
    Non-parametric bootstrap confidence interval for any statistic.

    Parameters
    ----------
    control_data : array-like
    treatment_data : array-like
    statistic_fn : callable or None
        Function that takes (control_array, treatment_array) and returns a scalar.
        Default: mean difference (treatment - control).
    n_bootstrap : int
        Number of bootstrap resamples. Default 10,000.
    alpha : float
        Significance level for CI. Default 0.05 (produces 95% CI).
    seed : int
        Random seed for reproducibility.
    """
    rng = np.random.default_rng(seed)
    control = np.array(control_data)
    treatment = np.array(treatment_data)

    if statistic_fn is None:
        statistic_fn = lambda c, t: np.mean(t) - np.mean(c)

    observed_stat = statistic_fn(control, treatment)

    bootstrap_stats = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        boot_c = rng.choice(control, size=len(control), replace=True)
        boot_t = rng.choice(treatment, size=len(treatment), replace=True)
        bootstrap_stats[i] = statistic_fn(boot_c, boot_t)

    ci_lower = np.percentile(bootstrap_stats, 100 * alpha / 2)
    ci_upper = np.percentile(bootstrap_stats, 100 * (1 - alpha / 2))

    p_value_approx = 2 * min(
        np.mean(bootstrap_stats <= 0),
        np.mean(bootstrap_stats >= 0)
    )

    print("=" * 60)
    print("TEST SELECTED: Bootstrap CI (non-parametric)")
    print("  Reason: Non-standard metric or robustness check for skewed data.")
    print()
    print(f"  Bootstrap resamples: {n_bootstrap:,}")
    print(f"  Observed statistic:  {observed_stat:+.4f}")
    print()
    print(f"TEST STATISTIC AND P-VALUE")
    print(f"  Approximate p (two-tailed): {p_value_approx:.4f}")
    print()
    print(f"{int((1-alpha)*100)}% BOOTSTRAP CONFIDENCE INTERVAL")
    print(f"  [{ci_lower:+.4f}, {ci_upper:+.4f}]")
    print(f"  CI crosses zero: {'YES — result inconclusive' if ci_lower < 0 < ci_upper else 'NO'}")
    print()
    print("EFFECT SIZE")
    print("  Effect size depends on metric. Compute Cohen's d or relative lift")
    print("  separately using the observed group means and standard deviations.")
    print("=" * 60)

    return observed_stat, ci_lower, ci_upper
```
