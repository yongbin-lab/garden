# Metric Selection Pitfalls and Anti-Patterns

Load this file when the user's experiment design shows signs of vanity metrics, correlated metrics, post-hoc selection, or other common measurement errors. Use these patterns to diagnose and correct the design before the experiment launches.

---

## Pitfall 1: Multiple Primary Metrics (Split Decision Authority)

**Definition:** Designating two or more metrics as co-equal primaries, typically framed as "우리는 X와 Y 둘 다 볼 거야" or "primary는 두 개 잡으면 안 돼요?" This pattern is extremely common because it feels inclusive — it seems to cover more risk — but it actually makes the experiment's decision criteria undefined.

**How to Detect:**
- The experiment design document lists more than one metric under "Primary" or "Goal Metric"
- The team plans to ship "if either metric improves"
- The team cannot answer the question: "If metric A improves and metric B declines, do we ship?"
- The experiment design uses language like "we'll look at both conversion and retention"

**How to Fix:**
Force a ranking. Ask: "If these two metrics move in opposite directions, which one wins?" The answer to that question IS your primary metric. The other becomes a sub metric. Document explicitly: "We ship if and only if [primary] shows statistically and practically significant improvement AND no guardrail metric regresses." The sub metric informs understanding of mechanism — it does not gate the decision.

If both metrics are genuinely co-equal and the team truly cannot choose, this is a sign that the experiment hypothesis is not sharp enough. Sharpen the hypothesis first, then the primary metric will follow.

**Qanda Example:**
A paywall redesign experiment listed both 프리미엄 결제 전환율 and D1 Retention as "co-primary." After two weeks, CVR was +12% (significant) and D1 Retention was -4% (marginal, not significant). The team spent three additional weeks debating whether to ship. The correct design would have named CVR as primary and D1 Retention as the guardrail with a defined floor, which would have resolved the decision on day 14.

---

## Pitfall 2: Aggregate Revenue Trap

**Definition:** Using total revenue, GMV, MRR, or any un-normalized aggregate revenue metric as the primary metric for an experiment. This appears rigorous because it is a direct business metric, but it is statistically and causally inappropriate for most A/B experiments.

**How to Detect:**
- The primary metric is stated as "revenue," "total subscriptions revenue," or "MRR"
- No per-user normalization is present in the metric formula
- The metric definition does not distinguish CVR from 객단가

**Why This Fails:**
Aggregate revenue has high variance driven by a small number of high-value users. A single 학부모 who purchases an annual family plan in variant B (but not variant A) can swing aggregate revenue by enough to appear significant when the underlying conversion behavior has not changed. Aggregate revenue also cannot distinguish between two very different scenarios: (a) more users converting at the same price, or (b) fewer users converting at a higher price. These require completely different product responses.

**How to Fix:**
Decompose revenue into its components:
```
기대 매출 = Σ [ segment_size × CVR(segment) × 객단가(segment) ]
```
This forces the team to state their hypothesis precisely: "We expect CVR to increase by X% for segment S at price P." It also makes the experiment auditable — you can verify which component of the formula drove the result.

**Qanda Example:**
A 가격 테스트 experiment used "월 구독 매출 합계" as the primary metric. The variant showed a statistically significant revenue increase. Post-experiment audit found that the result was driven entirely by two high-value 학부모 accounts who happened to be assigned to the variant group. When the team reanalyzed with 기대 매출 = CVR × 객단가 by segment, the variant showed a CVR decrease that was not offset by the price increase. The experiment should not have shipped.

---

## Pitfall 3: Segment Blindness

**Definition:** Conducting all analysis at the whole-population level and skipping pre-registered segment analysis. The whole-population average hides opposite-direction effects in different user segments, which can cause a net-zero or small-positive experiment to be shipped when it is actively harming one segment.

**How to Detect:**
- The experiment design document has no segment analysis plan
- Results are reported as a single overall number without segment breakdowns
- The team says "세그먼트까지 나눌 필요 있어? 전체 보면 되는 거 아니야?"
- The experiment involves any of the following: pricing, paywall design, onboarding for 신규 users, or any change that touches the 학생/학부모 distinction

**Why This Fails:**
Whole-population averages are a weighted average of segment-level effects. If 학생 CVR increases by +3pp and 학부모 CVR decreases by -3pp, and the two segments are roughly equal in size, the whole-population CVR change is approximately zero — and the experiment appears flat. But the product team is simultaneously making students more likely to subscribe and parents less likely. These are opposite business outcomes that require opposite responses, and the whole-population view hides both.

**How to Fix:**
Define all analysis segments before the experiment launches. At minimum, always pre-register:
- 학생 vs 학부모
- 신규 vs 기존
- Primary locale (ko_KR) vs other locales

Conduct the primary metric analysis for each pre-registered segment in addition to the whole population. If segments move in opposite directions, do not ship until the team has a resolution strategy (e.g., ship for one segment only, revise the design for the other segment).

**Qanda Example (confirmed):**
A 가격 테스트 experiment showed a slightly positive 기대 매출 result at the whole-population level. When broken down by user type, 학생 users showed fast-buy behavior (CVR largely maintained despite price increase) while 학부모 users showed comparison-buy behavior (CVR declined significantly). The whole-population positive result was driven entirely by the 학생 segment. If the experiment had shipped without segment analysis, the 학부모 CVR degradation would have been invisible until the next quarterly metric review.

---

## Pitfall 4: Post-Hoc Metric Addition (HARKing)

**Definition:** Adding, removing, or redefining metrics after seeing interim or final results. HARKing stands for "Hypothesizing After Results are Known." It is the most common source of false positives in A/B testing at product companies.

**How to Detect:**
- A metric appears in the results report that was not in the original experiment design document
- The team says "실험하다 보니까 이 지표도 보면 좋을 것 같아서 추가했어"
- The primary metric was swapped to a different metric that "happened to be more interesting"
- Success thresholds were adjusted after observing the distribution of results
- A guardrail was removed after it showed a negative signal

**Why This Fails:**
Pre-registering metrics is what gives statistical tests their claimed false positive rate. A p < 0.05 test has a 5% false positive rate only when the hypothesis was defined before seeing the data. When you add metrics after seeing results, you are effectively running many comparisons and cherry-picking the significant one. The true false positive rate of this process is unknown but much higher than 5% — in practice, it often exceeds 30–50% for experiments with 10+ post-hoc comparisons.

**How to Fix:**
Any metric not in the original experiment design document is automatically classified as "exploratory — not decision-relevant." Record it separately with an explicit label. Use it only to generate hypotheses for the next experiment. Never use a post-hoc metric to justify shipping the current change or to overrule a negative primary metric result.

The experiment design document must be timestamped and locked before data collection begins. At Qanda, this means the metric plan must be in the PRD appendix or BigQuery experiment_assignment table metadata before the experiment assignment starts.

---

## Pitfall 5: Guardrail-Primary Contradiction

**Definition:** Setting a guardrail metric that is expected to move in the opposite direction from the primary metric as a direct and intended consequence of the hypothesis. This creates a situation where the experiment triggers a guardrail violation every time it succeeds.

**How to Detect:**
- The hypothesis predicts that the treatment will cause users to spend less time in the product (faster conversion, less browsing), but session duration is set as a guardrail with a "no decrease" threshold
- The hypothesis predicts fewer, higher-quality sessions, but session count is a guardrail
- The guardrail and primary metric are measuring two sides of the same trade-off that the experiment is explicitly designed to make

**How to Fix:**
Ask: "If the primary metric moves in the expected direction, will this guardrail necessarily trigger?" If yes, the guardrail is contradictory — it is not protecting against unexpected harm; it is blocking the intended outcome. Move the metric to sub metric status. Replace "no decrease" with a directional expectation: "We expect this to decrease; this is acceptable and consistent with the hypothesis. Flag only if the decrease exceeds 2× our projected estimate." Guardrails must protect against unexpected harms, not planned trade-offs.

**Qanda Example:**
A 퍼널 개선 experiment simplified the subscription upgrade flow, reducing the number of steps from 5 to 3. The team set "average session duration" as a guardrail at "no decrease." By design, a shorter upgrade flow produces shorter sessions. The experiment successfully increased 퍼널 완료율 by 18% but simultaneously triggered the guardrail every week. The team spent two weeks debating a guardrail violation that was by definition: a success signal, not a harm signal. Session duration should have been reclassified as a sub metric with a directional expectation.

---

## Pitfall 6: Window Mismatch

**Definition:** Choosing a primary metric whose observation window does not match — and exceeds — the planned experiment duration. The result is that the experiment "ends" before the primary metric is observable for users exposed near the end of the experiment.

**How to Detect:**
- The experiment window is 2 weeks, but the primary metric is D30 Retention
- The primary metric is "1M subscription retention" but the experiment runs for 14 days
- The experiment measures "annual subscription renewal rate" within a 30-day window
- The team says "D30은 나중에 데이터 쌓이면 보자" — this is a window mismatch with delayed analysis, not a solution

**How to Fix (in order of preference):**

1. Extend the experiment window to match the full observation period. For D30 Retention as primary: run for at least 37 days (30 days of observation + 7 days ramp-up).

2. Use a validated leading indicator with documented historical proxy validity. D3 Retention can be a proxy for D7 if the product team has validated the correlation in past experiments. Document: "We are using D3 as a D7 proxy based on [specific analysis]; the proxy validity coefficient is [X]."

3. Use an intent signal as a proxy with explicit documentation that it is an approximation. "Plan selected" can approximate "subscription started" when billing cycle exceeds the experiment window — but document the gap.

**Qanda Example:**
A 리텐션 실험 testing a new 학습 streak mechanic used "D30 Retention" as the primary metric but ran for only 3 weeks. The team could only observe D30 for users exposed in the first week of the experiment (approximately 33% of the cohort). The remaining 67% of users had not yet reached day 30 when results were read. The reported D30 Retention figure was not representative of the full experiment cohort. The experiment should have used D7 Retention as primary (with D30 as a longer-term follow-up analysis run separately after the window closed).

---

## Pitfall 7: Vanity Metrics

**Definition:** A vanity metric is one that tends to increase regardless of whether the product is genuinely improving. It looks positive in a report but does not reflect user value, behavior change, or business outcome. Vanity metrics are especially dangerous as primary metrics because they provide false confidence in experiment results.

**How to Detect:**
Ask this diagnostic question: "Could this metric increase while the user experience is actively getting worse?" If yes, it is a vanity metric.

Common vanity metrics at product companies:
- Total page views or screen views (inflated by confusion, rage-clicking, repeated loading)
- Total registrations or sign-ups (does not measure whether users find value)
- Raw session count (inflated by bugs and disengaged browsing)
- Total push notifications sent (supply-side, not demand-side)
- App store ratings average (highly gameable; lagging by months)

**Qanda-specific vanity metric risks:**
- "쿼리 수 총합" (total queries) without normalization — inflated by confused users running repeated failed searches
- "앱 실행 수" (total app launches) — inflated by crashes and accidental opens
- "페이지 뷰" on any content page — inflated by users paging through content without engaging

**How to Fix:**
Replace vanity metrics with rate metrics or value-aligned metrics:
- Total registrations → D7 Retention among registrants
- Total queries → Successful query rate (queries that led to content engagement)
- App launches → Sessions with at least one meaningful action (search, content view, payment flow entry)

The test for a non-vanity metric: "If this metric improves, does it mean users are getting more value?" must be answerable with "yes."

---

## Pitfall 8: Correlated Metrics (Double-Counting)

**Definition:** Including two metrics in the same layer that are mathematically or causally correlated, creating the illusion of independent validation when the two signals are actually derived from the same underlying movement.

**How to Detect:**
Ask: "If metric A improves, is metric B almost certain to improve too, by mathematical derivation or causal structure?" If yes, they are correlated. Also check: "Is metric B a component of metric A's formula?"

Common correlated pairs:
- CVR AND 결제 수 (결제 수 = CVR × cohort size; cohort size is constant in an experiment → they move together)
- D1 Retention AND D3 Retention placed in the same layer (D3 retainers are a subset of D1 retainers; they are not independent)
- 기대 매출 AND ARPU when 객단가 is held constant (ARPU = 기대 매출 / cohort size; same signal, different scaling)
- 페이월 진입률 AND 결제 전환율 when the change is entirely at the paywall entry point (both move for the same reason)

**Why This Fails:**
Treating two correlated metrics as independent validation inflates confidence in the result. If both metrics improve, it feels like two independent pieces of evidence, but they are actually one piece of evidence counted twice. This leads to overconfident ship decisions and, in multiple-comparison contexts, increased false positive rates.

**How to Fix:**
Keep the metric that is more directly causally tied to the hypothesis. Move the correlated metric to exploratory analysis, or remove it. In the sub metric layer, correlated metrics are acceptable if they serve different diagnostic purposes (e.g., 페이월 진입률 explains WHERE in the funnel the CVR change occurred, even though it moves with CVR). But do not treat them as independent confirmation — acknowledge the correlation explicitly in the Metric Review.

**Qanda Example:**
A paywall experiment reported both "프리미엄 결제 전환율" and "결제 완료 수" as sub metrics. Both improved. The team cited this as "two positive signals." But 결제 완료 수 = 전환율 × cohort size, and cohort size is held constant by experiment design. The two metrics contain identical information. The Metric Review document should have flagged this as double-counting and reported only the rate metric.

---

## Quick Diagnosis Checklist

When reviewing a metric plan, run through these questions before approving the design:

1. Is there exactly ONE primary metric? (Multiple primaries → Pitfall 1)
2. Is the primary metric a per-user rate or decomposed revenue, not an aggregate? (Aggregate → Pitfall 2)
3. Is there a pre-registered segment analysis plan for 학생/학부모 and 신규/기존? (Missing → Pitfall 3)
4. Were all metrics defined before the experiment launched? (Post-hoc → Pitfall 4)
5. Does any guardrail directly contradict the hypothesis direction? (Contradiction → Pitfall 5)
6. Can all metrics be fully observed within the experiment window? (Mismatch → Pitfall 6)
7. Does the primary metric increase when user experience degrades? (Vanity → Pitfall 7)
8. Are any two metrics in the same layer mathematically derived from each other? (Correlated → Pitfall 8)

Flag any "no" answer as a required fix before the experiment design is approved for launch.
