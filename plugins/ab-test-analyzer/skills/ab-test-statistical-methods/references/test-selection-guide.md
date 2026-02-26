# Test Selection Guide — Full Decision Tree

Use this reference when `SKILL.md` Step 1 directs you here. Follow the decision tree to select the correct statistical test, then use the worked examples to verify the setup before running code.

---

## Decision Tree

Start at the top and answer each question in order. Stop at the first matching leaf.

```
Q1: Is the metric binary (yes/no per user)?
  YES → Q2
  NO  → Q3

Q2: Are you testing exactly two groups (control vs. one treatment)?
  YES → Two-proportion z-test  [or equivalently: chi-square with 2x2 contingency table]
  NO  → Chi-square goodness-of-fit or multi-group chi-square

Q3: Is the metric a ratio of two aggregated quantities (e.g., revenue per session
    where a user can have multiple sessions)?
  YES → Delta method or bootstrap CI  [see "Ratio Metrics" section below]
  NO  → Q4

Q4: Is the sample size per variant >= 30?
  YES → Q5
  NO  → Q6

Q5: Is the distribution approximately normal OR is the central limit theorem
    reliable at this sample size?
  YES → Welch's independent t-test  (do NOT use equal-variance t-test)
  NO  → Q6

Q6: Is the data clearly non-normal (heavy skew, bounded at zero, or count data)?
  COUNT data (integers, events per user) → Poisson regression or negative binomial regression
  CONTINUOUS but non-normal, small n  → Mann-Whitney U test
  CONTINUOUS, very heavy right skew    → Log-transform and apply Welch's t-test,
                                          OR bootstrap CI

Q7 (applies after any of the above): Are you testing more than one metric simultaneously?
  YES → Apply Bonferroni correction: alpha_adjusted = 0.05 / k
        where k = total number of metrics being tested
  NO  → Proceed with unadjusted alpha = 0.05
```

---

## Worked Example 1: Proportion Test (Signup Conversion Rate)

**Setup**

- Metric: Did the user sign up? (binary: 1 = yes, 0 = no)
- Control: 4,820 users, 241 conversions (rate = 0.0500)
- Treatment: 4,956 users, 272 conversions (rate = 0.0549)

**Decision tree path**

Q1: Binary? Yes. Q2: Two groups? Yes. → Two-proportion z-test.

**Calculation**

```
p_c = 241 / 4820 = 0.05000
p_t = 272 / 4956 = 0.05487

delta = p_t - p_c = 0.00487

p_pooled = (241 + 272) / (4820 + 4956) = 0.05247

SE = sqrt( p_pooled * (1 - p_pooled) * (1/4820 + 1/4956) )
   = sqrt( 0.05247 * 0.94753 * 0.000406 )
   = sqrt( 0.00002018 )
   = 0.004492

z = delta / SE = 0.00487 / 0.004492 = 1.084

p-value (two-tailed) = 2 * (1 - Phi(|z|)) = 2 * (1 - Phi(1.084)) ≈ 0.2784

95% CI on delta = (0.00487 - 1.96*0.004492, 0.00487 + 1.96*0.004492)
               = (-0.00394, +0.01368)
```

**Interpretation**

The CI crosses zero. The result is not statistically significant at alpha=0.05. Do not ship on this data alone. The relative lift is +9.7% but the confidence interval ranges from -7.9% to +27.4% relative — far too wide to act on.

---

## Worked Example 2: Continuous Metric with Right Skew (Revenue per User)

**Setup**

- Metric: Revenue per user in USD (continuous, right-skewed — many users at $0, a few large spenders)
- Control: n=2,400 users, mean=$14.22, std=$41.80
- Treatment: n=2,389 users, mean=$16.05, std=$45.33

**Decision tree path**

Q1: Binary? No. Q3: Ratio metric? No. Q4: n >= 30? Yes. Q5: CLT reliable at n=2400? Yes (n is large enough for CLT despite skew). → Welch's t-test.

Note: With revenue data, always check whether the skew is so extreme that even at n=2,400 the sampling distribution of the mean is non-normal. A rough check: if max_value > 20 * mean, consider bootstrap CI as a robustness check alongside the t-test.

**Calculation**

```python
from scipy import stats
t_stat, p_value = stats.ttest_ind(control_revenue, treatment_revenue, equal_var=False)
# Also compute 95% CI using the t-distribution with Welch-Satterthwaite df
```

Cohen's d:

```
pooled_std = sqrt( ((2399)*41.80^2 + (2388)*45.33^2) / (2400 + 2389 - 2) )
           = sqrt( (4,188,843 + 4,904,018) / 4787 )
           = sqrt( 1899.5 )
           = 43.58

d = (16.05 - 14.22) / 43.58 = 1.83 / 43.58 = 0.042
```

Cohen's d = 0.042 is negligible (d < 0.2). Even if the p-value is significant, the effect is practically tiny. Compare against the pre-specified MDE before recommending a ship.

---

## Edge Case: Ratio Metrics (Delta Method)

When the metric is a ratio of two aggregated quantities — for example, revenue per session where users have variable numbers of sessions — do NOT treat it as a simple continuous metric. The numerator and denominator are correlated, making the standard t-test invalid.

**Use the delta method:**

```
Var(ratio) ≈ (1/n) * [ Var(numerator) / mean(denominator)^2
                        - 2 * mean(numerator)/mean(denominator)^3 * Cov(num, denom)
                        + mean(numerator)^2 / mean(denominator)^4 * Var(denominator) ]
```

In practice, use a bootstrap CI for ratio metrics. It is robust, easy to explain, and does not require deriving the delta method formula manually. See `python-templates.md` for the bootstrap CI function.

---

## Edge Case: One-Tailed vs. Two-Tailed Tests

Almost always use a two-tailed test. Here is why:

- A two-tailed test asks: "Is the treatment different from control in either direction?"
- A one-tailed test asks: "Is the treatment specifically better than control?"

The statistical case for one-tailed: it has more power to detect an effect in the specified direction, because the entire alpha is allocated to one tail.

The practical problem with one-tailed: if the treatment turns out to be worse, a one-tailed test will not detect the harm. This is dangerous when the treatment could plausibly degrade key metrics. In product experiments, degradation is always possible, so one-tailed tests create unacceptable blind spots.

**Use one-tailed only when:** (a) it is physically impossible for the treatment to be worse (extremely rare), AND (b) it was pre-specified before the experiment started.

If a user asks to switch to a one-tailed test after seeing their p-value is 0.07, refuse. This is alpha inflation, not a legitimate design choice.

---

## Edge Case: Bootstrap CI for Non-Standard Metrics

Use bootstrap confidence intervals when:
- The metric is a ratio (as described above)
- The distribution is extremely heavy-tailed and n < 500
- The metric is a percentile or median (the t-test CI does not apply)
- You want a robustness check alongside a parametric test

Bootstrap procedure:

```
1. Pool control and treatment samples
2. Repeat 10,000 times:
   a. Resample n_c observations with replacement → bootstrap_control
   b. Resample n_t observations with replacement → bootstrap_treatment
   c. Compute the statistic of interest (e.g., mean difference, ratio difference)
   d. Store the result
3. The 2.5th and 97.5th percentiles of the 10,000 stored values form the 95% CI
```

Bootstrap CI does not require any distributional assumptions. It is slower but more reliable for non-standard metrics. See `python-templates.md` for the implementation.
