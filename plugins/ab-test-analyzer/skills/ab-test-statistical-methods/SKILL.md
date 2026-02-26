---
name: ab-test-statistical-methods
description: "This skill should be used when the user asks about A/B test statistical interpretation, significance testing, p-value meaning, confidence intervals, effect size, test selection, runtime estimation, or ambiguous results."
---

# Skill: ab-test-statistical-methods

## Description

This skill should be used when a user asks about A/B test statistical interpretation, significance testing, p-value meaning, confidence intervals, effect size, test selection, runtime estimation, or ambiguous results. Trigger phrases include: "이 결과 유의미해?", "is this result statistically significant", "p-value 해석해줘", "what does the p-value mean", "신뢰구간 계산해줘", "calculate confidence interval", "효과크기 어때?", "what's the effect size", "카이제곱 써야 해 t-test 써야 해?", "should I use chi-square or t-test", "얼마나 더 돌려야 유의미해져?", "how much longer to reach significance", "실험 결과 분석해줘", "analyze my experiment results", "결과가 애매한데 어떻게 해?", "results are ambiguous what do I do". Enforce statistical discipline and prevent decisions based on misread evidence.

---

## Overview

Apply this skill when analyzing A/B test data or interpreting experimental results. The goal is to enforce statistical discipline and prevent decisions based on misread evidence. Do not allow users to ship based on direction alone, p-value alone, or gut feel. Every analysis must produce a structured output that includes a test selection rationale, all three core statistics (p-value, CI, effect size), a practical significance check, and a plain-language recommendation.

---

## Step 1 — Select the Right Statistical Test

Before computing anything, identify the metric type. The wrong test produces invalid results even if the arithmetic is correct.

Use the following table to select the test:

| Metric type | Distribution | Recommended test |
|---|---|---|
| Binary (conversion rate, click-through) | — | Two-proportion z-test or chi-square |
| Continuous (revenue, session duration) | Normal or n >= 30 | Independent t-test (Welch's — do not assume equal variance) |
| Continuous | Non-normal and small n | Mann-Whitney U (non-parametric) |
| Count data (events per user) | — | Poisson regression or negative binomial |
| Multiple metrics simultaneously | Any | Apply Bonferroni correction to each individual test |

Ask the user for the following if not already provided:
- What is the metric? (binary yes/no, or continuous number?)
- What is the sample size per variant?
- What is the minimum detectable effect (MDE) they pre-specified?

Load `references/test-selection-guide.md` for the full decision tree with edge cases including ratio metrics and one-tailed vs two-tailed decisions.

---

## Step 2 — Interpret p-value Correctly

State this explicitly to the user before reporting any p-value:

The p-value is NOT the probability that the null hypothesis is true. It is NOT the probability that the result occurred by chance. It is the probability of observing results at least as extreme as the data, assuming the null hypothesis is true.

Standard threshold: p < 0.05 (two-tailed) unless the user has pre-specified a different alpha level. Never change the threshold after seeing the data.

Reporting rules:
- Never report p-value alone.
- Always report all three together: p-value, confidence interval, and effect size.
- Round p-value to 4 decimal places (e.g., p = 0.0312 not p = 0.03).
- If p = 0.0000 after rounding, report as p < 0.0001.

If the user provides only a p-value and asks for an interpretation, ask them for the CI and effect size before drawing any conclusion.

---

## Step 3 — Calculate and Interpret Confidence Intervals

For proportion metrics (e.g., conversion rate):

```
SE = sqrt( p_c*(1-p_c)/n_c + p_t*(1-p_t)/n_t )
delta = p_treatment - p_control
CI = (delta - 1.96 * SE, delta + 1.96 * SE)
```

For continuous metrics (e.g., revenue per user), use the CI returned directly from `scipy.stats.ttest_ind` with `equal_var=False`.

Interpret the CI using this logic:
- If the entire CI is above zero: the effect is positive and statistically significant.
- If the entire CI is below zero: the effect is negative and statistically significant.
- If the CI crosses zero: the result is inconclusive. Do not ship based on direction alone.
- Compare the lower bound of the CI to the user's MDE. If the lower bound is below MDE, the effect may be practically insignificant even if statistically significant.

Load `references/python-templates.md` for ready-to-run scipy code for CI calculation.

---

## Step 4 — Compute Effect Size

Effect size answers the question "is this difference meaningful in practice, not just mathematically detectable?"

For proportion metrics, compute relative lift:

```
relative_lift = (p_treatment - p_control) / p_control
```

Report as a percentage (e.g., +4.2% relative lift on conversion rate).

For continuous metrics, compute Cohen's d:

```
pooled_std = sqrt( ((n_c - 1)*std_c^2 + (n_t - 1)*std_t^2) / (n_c + n_t - 2) )
cohens_d = (mean_treatment - mean_control) / pooled_std
```

Cohen's d interpretation:
- d < 0.2: negligible
- 0.2 <= d < 0.5: small
- 0.5 <= d < 0.8: medium
- d >= 0.8: large

Practical significance check: compare the effect size to the user's pre-specified MDE. If the observed effect is below MDE, state clearly that the result may not be worth shipping even if p < 0.05.

---

## Step 5 — Estimate Remaining Runtime

When the user asks "how much longer do I need to run this?" or "얼마나 더 돌려야 유의미해져?", execute this sequence:

1. Compute current observed power using the current sample sizes and observed effect.
2. Compute the required sample size per variant for 80% power at alpha=0.05 using the user's pre-specified MDE (not the observed effect — using the observed effect to compute required n is circular and inflates power estimates).
3. Estimate remaining days: `days_remaining = (required_n - current_n) / daily_traffic_per_variant`.
4. If `required_runtime > 2x current_runtime`, STOP. Do not recommend simply running longer. State explicitly: "This experiment was underpowered at launch. Extending the runtime will not salvage it because the required additional time exceeds the experiment's original duration. The correct action is to stop the experiment, recalculate the required sample size, and redesign with adequate power before restarting."

Do not use the observed effect size as the target MDE when computing required sample size. Use only the MDE the user specified before the experiment started.

Load `references/python-templates.md` for the sample size calculator function.

---

## Step 6 — Multiple Comparison Correction

When the user reports results for more than one metric simultaneously, Bonferroni correction is mandatory unless the user has pre-specified a different correction method (e.g., Benjamini-Hochberg for FDR control).

Compute the adjusted alpha:

```
alpha_adjusted = 0.05 / number_of_metrics
```

Apply this adjusted threshold to each individual test. Report which metrics cleared the adjusted threshold and which did not. State explicitly in the output that Bonferroni correction was applied and how many metrics were tested.

Do not allow the user to selectively apply correction only to metrics that failed at the unadjusted level. Apply correction to all metrics in the family uniformly.

Load `references/python-templates.md` for the Bonferroni-corrected multi-metric analysis loop.

---

## Step 7 — Decision Framework for Inconclusive Results

When the result does not yield a clear ship or no-ship recommendation, apply this decision table:

| Situation | Diagnosis | Action |
|---|---|---|
| p > 0.05 and CI crosses zero, experiment ran less than pre-planned duration | Underpowered: ran too short | Calculate required runtime. Extend the experiment. Do not make a decision yet. |
| p > 0.05 and experiment ran full pre-planned duration | True null or effect smaller than MDE | The experiment has run to completion and produced no statistically significant result. The correct recommendation is DO NOT SHIP. If the team wishes to pursue the hypothesis, they must redesign the experiment with a revised MDE or collect new prior evidence before rerunning. |
| p < 0.05 but effect size below MDE | Statistically significant, practically insignificant | Ship only if implementation cost is near-zero. Otherwise, do not ship — the effect is too small to matter. |
| CI crosses zero but lower bound is near zero (near-miss) | Insufficient evidence | Do NOT ship. The result is not a near-miss; p=0.06 is not p=0.05. Rerun with larger sample. |
| A guardrail metric (e.g., retention, error rate) has degraded | Guardrail violated | Stop the experiment immediately regardless of primary metric result. Flag for investigation. |

---

## Red Flags — Recognize and Correct These Reasoning Errors

When the user expresses any of the following, stop and correct the reasoning before proceeding:

| What the user might say | What is actually happening | Correct response |
|---|---|---|
| "방향은 맞으니까 출시하자" / "The trend looks right, let's ship" | Seeking confirmation from direction alone without statistical evidence | Direction without CI entirely above zero is not evidence. Do not ship. |
| "좀 더 돌리면 유의미해질 거야" / "Let's run a bit longer until it becomes significant" | Optional stopping / peeking inflation | Stopping when you first see p < 0.05 inflates the true Type I error rate well above 5%. Pre-calculate required sample size and commit to it before the experiment starts. When a user presents data that was collected under optional stopping (stopped upon first reaching significance), flag this BEFORE computing any statistics. Include a Type I error inflation warning prominently in the output. Do NOT produce a clean "ship" recommendation from data collected under optional stopping without this explicit flag. |
| "Primary metric didn't move but secondary is looking great" | Post-hoc metric switching | Secondary metrics are diagnostic, not decisional. If the primary hypothesis failed, the experiment failed. Do not substitute secondary wins. |
| "샘플 사이즈가 크니까 유의성 안 봐도 돼" / "Sample size is huge so I don't need to worry about significance" | Misunderstanding of large-N behavior | Large N makes the test more sensitive to tiny effects that may be practically meaningless. Effect size is MORE important with large N, not less. |
| "95% 살짝 아래인데 거의 유의미하잖아" / "It's just below 95% CI, it's basically significant" | Threshold is arbitrary but binary | p=0.06 is not a near-miss. The threshold exists because decisions must be binary. If you want to use a different alpha, pre-specify it before the experiment. |
| "연휴 기간 데이터지만 그냥 쓰자" / "It's holiday traffic but let's use it anyway" | External validity violation | Holiday traffic has fundamentally different behavior. Exclude the affected period or analyze it separately. Do not mix it into the main analysis without explicit justification. |

---

## Output Format Contract

Every analysis produced by this skill must follow this exact structure, in this order:

1. **Test selected** — state the name of the test and one sentence explaining why it was chosen for this metric type.
2. **Test statistic and p-value** — report the z-statistic or t-statistic, and p-value to 4 decimal places.
3. **95% CI on the effect** — report as an interval on the absolute difference (e.g., 95% CI: [+0.8pp, +3.2pp]).
4. **Effect size** — report Cohen's d or relative lift percentage, with the qualitative label (negligible / small / medium / large).
5. **Practical significance check** — compare effect size to the user's MDE. State whether the observed effect clears the MDE threshold.
6. **Written recommendation** — one to three sentences in plain language stating a concrete action: ship, do not ship, extend the experiment, or stop and investigate. No other recommendation form is permitted. Phrases such as "promising results," "leaning toward shipping," "probably fine to proceed," or any hedged language are not valid conclusions. The recommendation MUST name one of the four actions above, with no hedging.

Do not omit any of these six elements. If data is missing to compute one of them, ask for it rather than skipping.

---

## References

- Load `references/test-selection-guide.md` for the full decision tree with edge cases, ratio metrics, and bootstrap CI guidance.
- Load `references/python-templates.md` for ready-to-run scipy/numpy Python code for all tests and sample size calculations.
- Run `scripts/setup-stats-env.sh` if scipy, numpy, pandas, or statsmodels are not installed in the user's environment.
- See `examples/proportion_test.py` for a complete worked example of a two-proportion z-test.
- See `examples/multi_metric_bonferroni.py` for a complete worked example of Bonferroni-corrected multi-metric analysis.
