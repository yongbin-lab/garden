# Qanda-Specific Metric Patterns

Load this file when generating the full Metric Review template for a Qanda experiment, when Qanda-specific data sources or segment definitions are needed, or when the user references past experiment patterns at Qanda.

---

## 1. Metric Review Template Structure

Every Qanda experiment produces a Metric Review document after the experiment concludes. The document follows a fixed 4-section structure. Generate outputs in this format when the user requests a full Metric Review or a template for their experiment.

### Section 1: 결과 한 줄 요약 (One-Line Result Summary)

A single sentence stating the overall result and ship/no-ship decision.

Format:
```
[Experiment Name]: [Primary metric] [direction and magnitude]. [Ship / Do not ship / Extend].
```

Example:
```
페이월 리디자인 실험: 프리미엄 결제 전환율 +14% (4.2% → 4.8%, p=0.02). Ship variant.
```

If the guardrail was violated:
```
가격 인상 실험: 기대 매출 +9% (p=0.04), but D1 Retention -7% (below guardrail floor). Do not ship.
```

### Section 2: 가설 검증 (Hypothesis Validation)

The Expected vs Actual comparison table. This is the core of the Metric Review.

```markdown
| 항목 (Item) | 기대 (Expectation) | 실제 (Reality) | Gap & Interpretation |
|---|---|---|---|
| Primary: 프리미엄 결제 전환율 | +14% (4.2% → 4.8%) | +11% (4.2% → 4.66%) | Slightly below target but above MDE. Primary met. |
| Sub: 페이월 진입률 | Directionally positive | +8% (28% → 30.2%) | Positive. Confirms entry improved. |
| Sub: 클릭률 (CTA) | Directionally positive | +3% (not significant) | Neutral. Conversion gain was post-click, not pre-click. |
| Guardrail: D1 Retention | Must not drop below 36.1% | 37.8% (baseline 38%) | Within threshold. No guardrail violation. |
```

The Expectation column is filled before the experiment. The Reality and Gap columns are filled after results are available. Never alter the Expectation column after results are known.

### Section 3: 기타 인사이트 (Additional Insights)

Exploratory observations that were not part of the pre-registered metric plan. These are clearly labeled as non-decision-relevant. They are used to generate hypotheses for future experiments.

Format: Bullet points. Each bullet must include the label "(탐색적 분석 — 의사결정 근거 아님)" to distinguish exploratory findings from pre-registered results.

Example:
```
- (탐색적 분석) 학생 세그먼트에서의 CVR 상승폭 (+18%)이 학부모 세그먼트 (+4%)보다 유의미하게 높았음. 학생 타겟 페이월 최적화 실험 가설로 검토 필요.
- (탐색적 분석) iOS 유저의 CTA 클릭률이 Android 대비 6% 낮게 관찰됨. iOS 페이월 레이아웃 별도 테스트 검토 가능.
```

### Section 4: Action Item

Concrete next steps with an owner and a due date for each item.

Format:
```markdown
| Action | Owner | Due Date |
|---|---|---|
| Ship variant to 100% of ko_KR users | 개발팀 | [Date] |
| Design follow-up experiment for 학부모 segment | PM | [Date] |
| Update baseline CVR in experiment_assignment metadata | 데이터팀 | [Date] |
```

---

## 2. Common Qanda Metrics Dictionary

Use these definitions when the user asks about a specific metric name. Apply the exact calculation formula when generating metric specs.

| Metric Name | Korean Name | Definition | Formula |
|---|---|---|---|
| 프리미엄 결제 전환율 | Premium Subscription CVR | Rate at which exposed users complete a premium subscription | (구독 완료 유저) / (실험 노출 유저) |
| 방문 대비 구독률 | Visit-to-Subscribe Rate | Rate at which app visits result in subscription | (신규 구독 시작) / (총 앱 방문 수) |
| 기대 매출 | Expected Revenue | Projected revenue decomposed by segment | Σ [segment_size × CVR(segment) × 객단가(segment)] |
| RPM | Revenue Per Mille | Revenue generated per 1,000 exposed users | (Total revenue / Total exposed users) × 1,000 |
| 에너지 소비량 | Energy Consumption | Number of energy units consumed per user per session (Qanda's feature-usage currency) | (Total energy used) / (Active users in window) |
| 쿼리 수 | Query Count | Number of search queries submitted per user per session | (Total queries) / (Sessions or users — specify denominator) |
| 기능 이용 유저 비율 | Feature Usage Rate | Proportion of cohort users who used a specific feature at least once | (Users who triggered feature event) / (Total cohort users) |
| 검색 리텐션 | Search Retention | Rate at which users who searched on day 1 return to search on day N | (Users who searched on day N) / (Users who searched on day 1) |
| D1 Retention | D1 Retention | Rate at which users return within 24 hours of their first session | (Users with session on day 1 who returned on day 2) / (Users with session on day 1) |
| 1M Retention | 1-Month Retention | Rate at which subscribers remain active 30 days after subscription start | (Active subscribers at day 30) / (Subscribers acquired during window) |
| 객단가 | Average Order Value (Subscription) | Average revenue per subscribing user | (Total subscription revenue) / (Total subscribers) |
| ARPU | Average Revenue Per User | Average revenue per user in the experiment cohort | (Total revenue) / (Total cohort users) |
| 페이월 진입률 | Paywall Entry Rate | Rate at which exposed users reach the paywall screen | (Users who viewed paywall) / (Total exposed users) |
| 클릭률 (CTR) | Click-Through Rate | Rate at which users who saw a CTA clicked it | (CTA clicks) / (CTA impressions) |
| 퍼널 완료율 | Funnel Completion Rate | Rate at which users who entered a funnel completed it end-to-end | (funnel_complete events) / (funnel_enter events) |
| 쿼터 제한 도달 유저 비율 | Quota Limit Reached Rate | Proportion of users who reached the daily/weekly usage quota limit | (Users who hit quota limit) / (Total cohort users) |

---

## 3. Segment Standards

Apply these standard segment definitions to all experiments. Use the exact identifiers listed here when writing BigQuery queries or defining experiment_assignment filters.

### User Type Segments

| Segment | Identifier | Definition |
|---|---|---|
| 학생 | `user_type = 'student'` | Users who registered as students; primary homework-help use case |
| 학부모 | `user_type = 'parent'` | Users who registered as parents; typically managing a student's account |
| 선생님 | `user_type = 'teacher'` | Users who registered as teachers; smaller population, different use patterns |

Note: 학생 and 학부모 exhibit proven behavioral pattern differences. 학생 users are fast-buy decision makers. 학부모 users are comparison-buy decision makers. Never aggregate these two segments without first checking that their treatment effects are directionally consistent.

### User Status Segments

| Segment | Identifier | Definition |
|---|---|---|
| 신규 | `user_status = 'new'` | Users with account age ≤ 7 days at time of experiment exposure |
| 기존 | `user_status = 'existing'` | Users with account age > 7 days, no active premium subscription |
| 프리미엄 | `user_status = 'premium'` | Users with an active premium subscription at time of exposure |

For experiments targeting non-premium users only: filter `user_status IN ('new', 'existing')` and exclude `premium` from the primary analysis (but monitor premium users separately if the experiment could affect them).

### Locale Segments

| Locale | Code | Notes |
|---|---|---|
| Korean | `ko_KR` | Primary market. Always validate here first before expanding. |
| Japanese | `ja_JP` | Second largest market. Different academic calendar and payment norms. |
| Thai | `th_TH` | Growing market. Mobile-first; payment method distribution differs from ko_KR. |
| Vietnamese | `vi_VN` | Emerging market. Lower 객단가 baseline; pricing test MDEs differ. |

For any multi-locale experiment: run ko_KR first for at least one full experiment window. If results are directionally consistent with expectations, expand to secondary locales. If ko_KR results are unexpected, pause and investigate before expanding.

---

## 4. Data Sources

Use these sources when querying experiment data or validating metric calculations.

### BigQuery: qanda_data_mart

Primary data warehouse for all experiment analysis.

Key tables:

| Table | Contents | Primary Use |
|---|---|---|
| `experiment_assignment` | User-level experiment group assignments, timestamps, and experiment metadata | Cohort definition; join base for all experiment analysis |
| `events` | Raw event stream (session start, query submitted, paywall viewed, subscription completed, etc.) | Metric calculation |
| `user_profiles` | User type, status, locale, account age, subscription history | Segment filters |
| `subscription_transactions` | Subscription start, renewal, cancellation, plan tier, revenue | 기대 매출, CVR, 1M Retention |
| `daily_retention` | Pre-computed D1, D3, D7, D14, D30 retention by cohort | Retention metric queries |

Standard experiment query pattern:
```sql
SELECT
  ea.experiment_id,
  ea.variant,
  ea.user_id,
  up.user_type,
  up.user_status,
  up.locale,
  -- metric columns joined from events or subscription_transactions
FROM qanda_data_mart.experiment_assignment ea
JOIN qanda_data_mart.user_profiles up ON ea.user_id = up.user_id
WHERE ea.experiment_id = '[your_experiment_id]'
  AND ea.assignment_date BETWEEN '[start_date]' AND '[end_date]'
```

### Mixpanel

Used for funnel analysis, event flow visualization, and real-time experiment monitoring during the experiment window.

Key dashboards:
- 실험 모니터링 대시보드: Daily metric tracking for active experiments
- 퍼널 분석: Step-by-step funnel completion rates
- 세그먼트 비교: Side-by-side metric comparison by user type and status

Note: Mixpanel numbers and BigQuery numbers may differ by 1–3% due to event deduplication differences. BigQuery (qanda_data_mart) is the source of truth for all official Metric Review results.

### AdPost Report

Used specifically for monetization and pricing experiments to track subscription revenue from ad-supported to paid conversion flows. Contains IAP (in-app purchase) data at the transaction level.

Use when: The experiment involves the paywall, pricing page, subscription plan selection, or payment completion flow.

---

## 5. Decision Framework

Apply this framework at the end of every experiment to produce the ship/no-ship decision. Do not deviate from this framework — it is the basis of Metric Review approval.

### Step 1: Check Guardrails First

Before evaluating the primary metric, check all guardrail metrics.

- If any guardrail metric has regressed beyond its pre-defined threshold: **STOP. Do not ship. Investigate the guardrail violation.** The primary metric result is irrelevant until the guardrail violation is explained.
- If all guardrail metrics are within their thresholds: proceed to Step 2.

### Step 2: Evaluate the Primary Metric

| Primary Metric Result | Decision |
|---|---|
| Statistically significant improvement (p < 0.05) AND practically significant (above MDE) | **Ship variant** |
| Statistically significant improvement but below MDE (practically insignificant) | **Ship control** (or extend if close to MDE and sample size can increase) |
| Not statistically significant (flat) | **Ship control** |
| Statistically significant decline | **Ship control** |

### Step 3: Interpret Sub Metrics

After making the ship/no-ship decision based on the primary metric and guardrails, document sub metric results in the Metric Review:
- If sub metrics moved in the expected direction alongside the primary: hypothesis mechanism confirmed.
- If sub metrics did not move as expected despite primary metric improvement: document unexplained mechanism in "기타 인사이트" and propose a follow-up diagnostic experiment.
- If sub metrics moved in the opposite direction from the primary: flag as a potential measurement issue or complex interaction effect. Do not override the primary metric decision — but schedule a follow-up review.

### Step 4: Document and Close

Complete all four sections of the Metric Review document. Update the experiment_assignment table metadata with the final decision and date. Notify stakeholders of the result and next steps via the Action Item section.

### Summary Decision Table

| Condition | Decision |
|---|---|
| Goal 달성 (primary positive, all guardrails pass) | Ship variant |
| Goal 미달 (primary flat or negative, guardrails pass) | Ship control or extend experiment |
| Guardrail 위반 (any guardrail exceeds threshold) | Stop immediately — do not ship, investigate |
| Goal 달성 + Guardrail 위반 (primary positive but guardrail violated) | Do not ship — guardrail violation vetoes positive primary |
| Inconclusive (experiment ended early, insufficient sample) | Extend experiment window; do not make a decision on underpowered data |
