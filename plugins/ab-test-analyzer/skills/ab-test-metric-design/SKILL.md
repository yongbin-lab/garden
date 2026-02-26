---
name: ab-test-metric-design
description: "This skill should be used when the user asks about A/B test metric design, success criteria, metric selection, or experiment measurement planning."
---

# Skill: ab-test-metric-design

## Description (Layer 1)

This skill should be used when a PM or analyst needs to define, structure, or validate the metrics for an A/B experiment. Activate this skill when the user says things like "어떤 지표 봐야 해?", "what metrics should I track", "성공 기준 정해줘", "help me define success criteria", "PRD 보고 지표 설계해줘", "design metrics from my PRD", "primary metric 뭘로 잡아야 해?", "guardrail metric이 뭐야?", "이 실험 지표 어떻게 잡지?", "전환율 실험 지표 추천해줘", or "가격 테스트 성공 기준". The skill enforces Qanda's 3-tier metric hierarchy (Primary → Sub Metric → Guardrail) and produces a complete, actionable metric spec ready for experiment review.

---

## Body (Layer 2)

### Overview

Guide the PM through selecting the right metrics for A/B experiments at Qanda (콴다). Enforce the Primary → Sub Metric → Guardrail hierarchy at every step. Do not let the user proceed without a clearly named primary metric, at least one guardrail, and a defined segment plan. The output of this skill is a complete Metric Spec document that can be dropped directly into a Metric Review or PRD appendix.

---

### Step 1 — Understand Metric Hierarchy

Apply Qanda's 3-tier metric structure to every experiment without exception.

**Primary (Goal) Metric**

The ONE metric that determines the ship/no-ship decision. If the primary metric is positive and no guardrail is violated, the variant ships. If the primary metric is flat or negative, the variant does not ship regardless of other signals. The primary metric must be directly tied to the stated hypothesis — if the hypothesis changes, the primary metric must be re-evaluated.

Qanda-specific examples of valid primary metrics:
- 프리미엄 결제 전환율 (premium subscription conversion rate)
- 검색 리텐션 (search retention)
- Daily Retention (D1, D3, D7 — specify exactly which day)
- 기대 매출 (expected revenue = CVR × 객단가, aggregated by segment)

Reject vague primaries such as "engagement," "user satisfaction," or "overall revenue" without a precise calculation formula attached.

**Sub Metric**

Supporting metrics that explain HOW and WHY the primary moved. Sub metrics do not determine ship/no-ship on their own — they exist to diagnose the mechanism behind the primary metric's movement. If the primary goes up but all sub metrics are flat, investigate measurement error. If the primary goes up and the right sub metrics also move in the expected direction, the hypothesis is confirmed.

Qanda-specific examples of valid sub metrics:
- 클릭률 (CTR) on paywall entry points
- 에너지 소비량 (energy consumption, for feature usage experiments)
- 쿼리 수 (number of search queries per session)
- 기능 이용 유저 비율 (percentage of users who used the target feature)
- RPM (revenue per thousand impressions, for monetization experiments)

**Guardrail Metric**

Metrics that must NOT degrade beyond an acceptable threshold. If any guardrail is violated, stop the experiment immediately regardless of primary metric status. Guardrails protect the parts of the product not targeted by the experiment.

Default guardrail at Qanda: **D1 Retention 유지** (D1 retention must not drop).

Additional common guardrails:
- 프리미엄 전환율 유지 (for retention experiments that could cannibalize revenue)
- 매출 하락 없음 (for feature experiments running on paying users)
- CVR 하락폭 한도 (for price tests — define an explicit maximum acceptable CVR drop)

---

### Step 2 — Select by Experiment Type

Use this quick-reference table to map the experiment type to the recommended metric structure. Ask the user to identify their experiment type before proceeding. If they are unsure, ask: "이 실험이 궁극적으로 올리고 싶은 게 결제율이야, 리텐션이야, 아니면 매출이야?"

| Experiment Type | Recommended Primary | Common Sub Metrics | Default Guardrail |
|---|---|---|---|
| 전환율 개선 (CVR) | 프리미엄 결제 전환율 or 방문 대비 구독률 | 페이월 진입률, 클릭률, 결제 수 by segment | D1 Retention |
| 리텐션 실험 | Daily/Weekly Retention (specify exactly which) | D1, D3-6, Weekly, 검색 리텐션 | 프리미엄 전환율 |
| 결제/매출 실험 | 기대 매출 (CVR × 객단가) | CVR by segment, 1M Retention, ARPU | D1 Retention, CVR 하락폭 |
| 퍼널 개선 | 퍼널 완료율 or 쿼터 제한 도달 유저 비율 | 단계별 이탈률, 쿼리 수, 기능 이용 비율 | D1 Retention |
| 가격 테스트 | 기대 매출 (not just CVR!) | CVR by price tier, 1M Retention by segment, 객단가 | D1 Retention, CVR 하락폭 한도 |

For price tests specifically: never accept CVR alone as the primary metric. A price increase will almost always reduce CVR — the question is whether the revenue gain from higher ARPU outweighs the CVR loss. 기대 매출 captures this trade-off; raw CVR does not.

For retention experiments: always specify the exact retention window. "Retention" is not a metric. "D1 Retention measured as the proportion of users who return within 24 hours of first session" is a metric.

---

### Step 3 — Define Segment Analysis Plan

Segment analysis is MANDATORY at Qanda. Define all segments before the experiment begins. Post-hoc segmentation is a form of p-hacking and will not be accepted in Metric Review.

**User Type Segments**
- 학생 (student)
- 학부모 (parent)
- 선생님 (teacher)

**User Status Segments**
- 신규 (new users, typically first 7 days)
- 기존 (existing non-premium users)
- 프리미엄 (active premium subscribers)

**Locale Segments**
- ko_KR (Korean — primary market, always run first)
- ja_JP (Japanese)
- th_TH (Thai)
- vi_VN (Vietnamese)

For experiments with global rollout, always run ko_KR first. If the experiment produces unexpected results in ko_KR, pause before expanding to other locales.

Issue a warning whenever the user proposes whole-population analysis only:

> "학생과 학부모 패턴이 정반대인 경우가 실제로 있었음 (가격 테스트 실험). 전체 평균으로 보면 이 차이가 숨겨짐. 세그먼트 분석 계획을 먼저 정의해야 함."

Student users tend to be fast-buy decision makers. Parent users tend to be comparison-buy decision makers with longer consideration cycles. An experiment that improves student CVR may simultaneously decrease parent CVR. A whole-population average will show a small positive effect and mask the parent degradation entirely.

---

### Step 4 — Set Quantitative Expectations

For each metric in the spec, require the user to define the following before the experiment runs. If they cannot supply a baseline, check `references/metric-templates.md` for typical Qanda baselines.

- **Baseline value**: Current observed value from production data (cite the data source and measurement window)
- **Target value**: The value the team expects to achieve with the variant, expressed as an absolute or relative change
- **Minimum Detectable Effect (MDE)**: The smallest change the experiment is designed to reliably detect
- **Success threshold**: The value at which the team will call the experiment a success (may differ from the target)

For revenue-related experiments, calculate 기대 매출 using the following framework:

```
기대 매출 (per variant) = Σ [ segment_size × CVR(segment) × 객단가(segment) ]

where the sum is taken over all user segments included in the experiment.
```

This decomposition forces the PM to specify CVR and price assumptions separately per segment, which prevents the Aggregate Revenue Trap (see `references/metric-pitfalls.md` Pitfall 2).

Example format for quantitative expectations:

| Metric | Type | Baseline | Target | MDE | Success Threshold |
|---|---|---|---|---|---|
| 프리미엄 결제 전환율 | Primary | 4.2% | 4.8% (+14%) | +0.5pp | ≥ 4.7% with p < 0.05 |
| 페이월 진입률 | Sub | 31% | 35% | — | Directionally positive |
| D1 Retention | Guardrail | 38% | Maintain | — | Must not drop below 36.5% |

---

### Step 5 — Output Format

Generate the metric spec as a markdown document with the following structure. This matches Qanda's Metric Review template format.

```markdown
## Metric Spec: [Experiment Name]

**Experiment Type:** [전환율 / 리텐션 / 결제·매출 / 퍼널 / 가격]
**Hypothesis:** [One sentence]
**Primary Locale:** [ko_KR / ja_JP / ...]
**Segments Defined:** [학생/학부모, 신규/기존/프리미엄, 로케일]

---

### Metric Hierarchy

| 항목 | Metric | 기대(Expectation) | 실제(Reality) | Gap & Interpretation |
|---|---|---|---|---|
| Primary | 프리미엄 결제 전환율 | +14% (4.2% → 4.8%) | — | — |
| Sub | 페이월 진입률 | Directionally positive | — | — |
| Sub | 클릭률 (CTA) | Directionally positive | — | — |
| Guardrail | D1 Retention | Must not drop below 36.5% | — | — |

---

### 기대 매출 Calculation (if applicable)

| Segment | Size | CVR (Control) | CVR (Variant) | 객단가 | 기대 매출 Delta |
|---|---|---|---|---|---|
| 학생 (신규) | — | — | — | — | — |
| 학부모 (기존) | — | — | — | — | — |
| **Total** | | | | | — |

---

### Segment Analysis Plan

- [ ] 학생 vs 학부모 split defined
- [ ] 신규 vs 기존 split defined
- [ ] Locale: primary ko_KR, secondary [...]
```

Leave the Reality column and Gap & Interpretation column blank. These are filled during and after the experiment in the Metric Review document.

---

### Step 6 — Final Checklist

Before presenting the completed metric spec to the user, verify every item:

- [ ] Exactly ONE primary metric is named with a precise calculation formula?
- [ ] The primary metric is directly tied to the hypothesis (not a proxy or vanity metric)?
- [ ] At least one guardrail metric is defined, and it includes D1 Retention?
- [ ] Acceptable degradation thresholds are set for all guardrail metrics?
- [ ] Segments defined: at minimum 학생/학부모 and 신규/기존, plus relevant locales?
- [ ] Quantitative expectations set with baseline value, target value, and MDE?
- [ ] 기대 매출 formula applied for all revenue-related experiments?
- [ ] No metrics were selected post-hoc (all metrics defined before experiment starts)?

If any item remains unchecked after asking, MUST NOT produce the metric spec. Output only: "The metric spec cannot be completed until the following items are resolved: [list unchecked items]. Provide the required information to proceed."

---

### Red Flags — Do Not Rationalize

When the user pushes back on metric discipline, do not accommodate the rationalization. Use the table below to respond directly.

| Rationalization | Reality |
|---|---|
| "Primary metric 2개 잡으면 안 돼?" | 2개면 사실상 0개. Ship/no-ship 결정 기준이 모호해짐. 두 지표가 반대 방향으로 움직이면 어떻게 결정할 것인가? 하나만 정하라. |
| "전체 유저로 보면 되지, 세그먼트까지 나눌 필요 있어?" | 학생/학부모 패턴이 정반대인 경우가 실제로 있었음 (가격 테스트 실험). 전체 평균은 반대 방향의 세그먼트 효과를 숨긴다. 세그먼트 분석은 필수다. |
| "매출 지표는 revenue로 퉁치면 되지" | Aggregate revenue는 노이즈가 크고 CVR 변화와 객단가 변화를 구분하지 못한다. CVR × 객단가로 분해하라. |
| "통계적 유의성은 결과 나오면 그때 보자" | 지표 설계 시점에 MDE와 필요 샘플 사이즈를 정해야 p-hacking과 early stopping bias를 방지할 수 있다. 나중에 정하는 건 설계가 아니라 사후 합리화다. |
| "Guardrail은 안 봐도 되지, primary만 보면 돼" | Guardrail 없이 primary만 올리면 다른 핵심 지표가 무너져도 모른다. Primary를 올리기 위해 리텐션을 희생하는 variant는 장기적으로 손해다. |
| "실험 기간 중에 지표 하나 더 추가하자" | 결과를 본 후 지표를 추가하는 것은 다중비교(multiple comparison) 문제를 발생시킨다. 처음부터 정하라. 실험 중 지표 추가는 Metric Review에서 거부된다. |
| "이 실험은 작은 실험이라서 대충 봐도 돼" | 작은 실험이라도 primary metric과 guardrail은 필수다. 예외 없이 적용한다. |

---

## References (Layer 3)

Load `references/metric-templates.md` when:
- Detailed metric definitions and calculation formulas are needed for a specific experiment type
- The user asks for a baseline value or MDE guidance for a specific metric
- The user needs the full sub-metric list for a given experiment category

Load `references/metric-pitfalls.md` when:
- The user's proposed metric selection shows signs of a known anti-pattern
- The user pushes back on any item in the Red Flags table
- A guardrail is missing, a second primary is being proposed, or segment analysis is being skipped

Load `references/qanda-metric-patterns.md` when:
- Generating the full Metric Review template for a specific experiment
- Qanda-specific context is needed (data sources, segment definitions, decision framework)
- The user references a specific past experiment at Qanda and needs the established metric patterns for that experiment type
