# Metric Templates by Experiment Type

Load this file when the user needs detailed metric definitions, calculation formulas, baseline values, or MDE guidance for a specific experiment type at Qanda (콴다).

---

## Template 1: 전환율 개선 (CVR — Conversion Rate Optimization)

**Experiment context:** Changes to UI, copy, paywall design, onboarding flows, or CTA placement that affect whether a user subscribes to Qanda premium. The hypothesis predicts a direct change in conversion behavior.

### Primary Metric

**프리미엄 결제 전환율** (preferred) or **방문 대비 구독률**

- Definition (프리미엄 결제 전환율): (Users who completed a premium subscription purchase) / (Users who were exposed to the experiment)
- Definition (방문 대비 구독률): (Premium subscriptions started) / (Total app visits during window)
- Calculation unit: Per unique user within the experiment window (not per session — a user visiting twice counts once)
- Aggregation: Cumulative rate over the full experiment window; also report daily rate to detect novelty effects
- Formula: `전환율 = (구독 완료 유저 수) / (실험 노출 유저 수)`

**When to prefer 방문 대비 구독률:** Use when the change affects the entire entry surface (e.g., home screen). Use 프리미엄 결제 전환율 when the change is downstream of entry (e.g., paywall design).

### Sub Metrics (3-5)

1. **페이월 진입률** — Rate at which exposed users reached the paywall
   - Formula: `(페이월 진입 유저 수) / (실험 노출 유저 수)`
   - Purpose: Isolates whether CVR change originates from paywall entry or from paywall-to-purchase conversion

2. **클릭률 (CTR)** — Rate at which users clicked the primary CTA
   - Formula: `(CTA 클릭 유저 수) / (CTA 노출 유저 수)`
   - Purpose: Detects friction at the specific element changed

3. **결제 수 by segment** — Absolute count of purchases broken down by 학생/학부모 and 신규/기존
   - Purpose: Reveals whether CVR improvement is concentrated in one segment or distributed

4. **구독 플랜 분포** — Proportion of converters choosing each plan tier (월간/연간)
   - Purpose: Guards against CVR increase driven by downgrades to lower-value plans

5. **구독 완료까지 소요 시간** — Median time from experiment exposure to subscription completion
   - Purpose: Detects whether the variant accelerates or delays the decision cycle

### Guardrail Metrics

1. **D1 Retention** — Must not drop below baseline
   - Threshold: No more than 5% relative decrease from baseline (e.g., if baseline is 38%, floor is 36.1%)
   - Rationale: A CVR experiment that improves conversion by attracting low-intent users who churn on day 1 is harmful

2. **프리미엄 구독 취소율 (30일 이내)** — Cancellations within 30 days of subscription start
   - Threshold: No more than 10% relative increase
   - Rationale: Guardrail against dark patterns that coerce purchase without genuine intent

### Recommended Segments

- Primary split: 학생 vs 학부모 (behavioral patterns differ significantly)
- Status split: 신규 vs 기존 non-premium users
- Locale: ko_KR first; expand to ja_JP, th_TH, vi_VN after ko_KR validation

### MDE Guidance

- Typical Qanda premium CVR baseline: 3–6%
- Recommended MDE: +0.5pp absolute (~10–15% relative lift)
- At 10,000 weekly exposed users and 4% baseline CVR, detecting 0.5pp lift requires approximately 2–3 weeks at p < 0.05, 80% power
- If weekly exposed users are below 3,000, set MDE at 1pp absolute minimum

### Example Baseline → Target Format

| Metric | Baseline | Target | MDE |
|---|---|---|---|
| 프리미엄 결제 전환율 | 4.2% | 4.8% | +0.5pp |
| 페이월 진입률 | 28% | 32% | Directional |
| D1 Retention (guardrail) | 38% | ≥ 36.1% | N/A |

---

## Template 2: 리텐션 실험 (Retention Experiments)

**Experiment context:** Feature additions, onboarding redesigns, notification experiments, streak mechanics, or engagement nudges designed to improve return rates at Qanda.

### Primary Metric

**Daily Retention** — specify the exact day (D1, D3, D7). Do not use "retention" without the day attached.

- Definition (D1): (Users who returned to the app within 24 hours of their first session in the experiment cohort) / (Total users in the experiment cohort)
- Definition (D7): (Users who returned on day 7 after cohort entry) / (Total users in the experiment cohort)
- Calculation: Use calendar-day windows, not rolling windows, for cross-experiment comparability
- Cohort boundary: Define cohort entry as experiment assignment date, not account creation date

**검색 리텐션** (search-specific retention): Use when the experiment directly modifies search behavior
- Definition: (Users who performed a search on day N) / (Users who performed a search on day 1 of cohort)

**When to use D1 vs D7:** Use D1 when the experiment window is under 2 weeks or when the product has a daily-use expectation (homework help). Use D7 when measuring habit formation for features with a weekly natural frequency.

### Sub Metrics (3-5)

1. **D3 Retention** — Leading indicator bridging D1 and D7
   - Formula: Same as D1 but measured at day 3
   - Purpose: Early signal for D7 direction when experiment window is short

2. **Weekly Retention** — (Users active in week N) / (Users active in week 1 of cohort)
   - Purpose: Captures weekly usage patterns for students with homework cycles

3. **쿼리 수 per session** — Average number of search queries per active session
   - Purpose: Measures engagement depth among retained users; retention without engagement is weak signal

4. **기능 이용 유저 비율** — (Users who used the target feature at least once during window) / (Total cohort)
   - Purpose: Confirms feature adoption when the experiment introduces a new engagement mechanic

5. **세션 빈도** — Average sessions per user per week during experiment window
   - Purpose: Distinguishes "came back once" retention from habitual usage

### Guardrail Metrics

1. **프리미엄 전환율 유지** — Premium subscription CVR must not drop
   - Threshold: No more than 5% relative decrease
   - Rationale: Retention improvements that replace premium intent with free engagement harm revenue

2. **푸시 알림 수신 거부율** — Push notification opt-out rate (critical for notification experiments)
   - Threshold: No more than 5% relative increase
   - Rationale: Aggressive retention nudges that drive notification opt-outs create long-term re-engagement problems

### Recommended Segments

- Primary split: 학생 vs 학부모 (학생: daily homework driver; 학부모: periodic monitoring)
- Status split: 신규 (first 7 days) vs 기존 (8+ days)
- Locale: ko_KR first; Korean academic calendar (시험 기간) affects baseline — control for exam season timing

### MDE Guidance

- Typical Qanda D1 baseline: 30–45% depending on user cohort
- Recommended MDE for D1: +2pp absolute (~5–7% relative lift)
- D7 baseline: 15–25%; recommended MDE: +1.5pp absolute
- Required window: Minimum 2 weeks to observe D7 for all exposed users; 3 weeks preferred for clean cohort analysis
- Required sample: 3,000–5,000 users per variant for 5% relative lift at 80% power

### Example Baseline → Target Format

| Metric | Baseline | Target | MDE |
|---|---|---|---|
| D1 Retention (primary) | 38% | 41% | +2pp |
| D7 Retention (sub) | 20% | 22% | Directional |
| 프리미엄 전환율 (guardrail) | 4.2% | ≥ 3.99% | N/A |

---

## Template 3: 결제/매출 실험 (Payment and Revenue Experiments)

**Experiment context:** Changes to payment flow UX, payment method options, subscription plan structure, or billing presentation that affect whether a user completes a premium purchase.

### Primary Metric

**기대 매출** (Expected Revenue)

- Definition: The sum of expected revenue across all segments, calculated as CVR × 객단가 per segment
- Formula:
  ```
  기대 매출 = Σ [ segment_size × CVR(segment) × 객단가(segment) ]
  ```
- Measurement window: Must span at least one billing cycle (monthly subscriptions: 30+ days)
- Critical: Decompose by segment. Do not use aggregate revenue — it obscures segment-level CVR and price trade-offs.

### Sub Metrics (3-5)

1. **CVR by segment** — Conversion rate broken down by 학생/학부모 and 신규/기존
   - Purpose: Reveals which segment drives the 기대 매출 change

2. **1M Retention (1-Month Retention)** — Rate at which new subscribers remain subscribed at day 30
   - Formula: `(Subscribers still active at day 30) / (Subscribers acquired during experiment)`
   - Purpose: High CVR with low 1M Retention indicates low-quality acquisitions

3. **ARPU (Average Revenue Per User)** — Total revenue / Total experiment cohort users
   - Purpose: Normalizes revenue across cohort sizes for cross-variant comparison

4. **결제 수단 분포** — Distribution of payment methods used (카드, 인앱결제, etc.)
   - Purpose: Changes in payment method distribution can signal UX friction or platform-specific effects

5. **RPM (Revenue per Mille)** — Revenue per 1,000 users exposed
   - Formula: `(Total revenue / Total exposed users) × 1,000`
   - Purpose: Comparable across cohorts of different sizes; useful for cross-experiment benchmarking

### Guardrail Metrics

1. **D1 Retention** — Must not drop
   - Threshold: No more than 5% relative decrease
   - Rationale: A payment UX change should not disrupt the core product loop

2. **CVR 하락폭 한도** — If the experiment raises prices, CVR may drop — but must stay above the floor
   - Threshold: Pre-define the acceptable CVR drop floor (e.g., "CVR must not drop below 3.0%")
   - Rationale: Forces the team to articulate the revenue-conversion trade-off explicitly

### Recommended Segments

- Primary split: 학생 (fast-buy) vs 학부모 (comparison-buy) — these segments respond differently to payment flow changes
- Status split: 신규 (first-time purchasers) vs 기존 (returning purchasers / re-subscribers)
- Locale: ko_KR first; pricing and payment norms differ by market

### MDE Guidance

- 기대 매출 has higher variance than CVR — apply CUPED if available
- Minimum window: 30 days to capture one billing cycle
- Minimum viable volume: 500 purchases per variant to detect a 5% 기대 매출 lift at 80% power
- For experiments where 객단가 is also changing: model the revenue distribution before setting MDE — the variance changes with the price point

### Example Baseline → Target Format

| Metric | Baseline | Target | MDE |
|---|---|---|---|
| 기대 매출 (primary) | ₩12,500 / user | ₩13,500 / user (+8%) | +₩500 / user |
| CVR — 학생 (신규) | 5.1% | 5.8% | Directional |
| CVR — 학부모 (기존) | 3.2% | 3.5% | Directional |
| D1 Retention (guardrail) | 38% | ≥ 36.1% | N/A |
| CVR floor (guardrail) | — | Must not drop below 3.0% | N/A |

---

## Template 4: 퍼널 개선 (Funnel Optimization)

**Experiment context:** Changes to a specific step within a multi-step flow (onboarding, subscription upgrade flow, content discovery funnel) where the goal is to improve progression through that step.

### Primary Metric

**퍼널 완료율** or **쿼터 제한 도달 유저 비율**

- Definition (퍼널 완료율): (Users who completed the entire funnel end-to-end) / (Users who entered the funnel)
- Definition (쿼터 제한 도달 유저 비율): (Users who reached the quota limit, indicating deep engagement) / (Users in experiment cohort)
- Critical: Define the exact event name for each funnel step in BigQuery before the experiment launches. Ambiguous step definitions cause measurement errors that cannot be corrected post-hoc.
- Formula: `퍼널 완료율 = (funnel_complete 이벤트 발생 유저) / (funnel_enter 이벤트 발생 유저)`

### Sub Metrics (3-5)

1. **단계별 이탈률** — Drop-off rate at each individual funnel step
   - Formula: `(funnel_step_N_exit 유저) / (funnel_step_N_enter 유저)` for each step N
   - Purpose: Pinpoints exactly which step the experiment changes

2. **쿼리 수** — Number of search queries per session during funnel exposure
   - Purpose: High query count before funnel completion may indicate confusion (negative) or engagement (positive) — interpret directionally

3. **기능 이용 비율** — (Users who engaged with the specific feature being changed) / (Users who entered the funnel step)
   - Purpose: Measures feature adoption within the funnel; required when the experiment adds a new element

4. **퍼널 완료까지 소요 시간** — Median time from funnel entry to completion
   - Purpose: Detects whether the variant reduces friction (time decreases) or adds decision overhead (time increases)

5. **업스트림 진입률** — Rate at which users from the wider cohort enter the funnel at all
   - Purpose: Confirms the experiment did not suppress funnel entry from earlier in the user journey

### Guardrail Metrics

1. **D1 Retention** — Must not drop
   - Threshold: No more than 5% relative decrease
   - Rationale: Funnel changes that rush users through steps may reduce retention if comprehension suffers

2. **에러율 at target step** — (Users who hit a system error at the changed step) / (Users who attempted that step)
   - Threshold: Zero regression — any statistically significant increase is a hard veto
   - Rationale: Funnel changes often touch the same code paths as error-prone UX components

### Recommended Segments

- Primary split: 신규 vs 기존 users (new users encounter onboarding funnels for the first time; existing users may skip familiar steps)
- User type: 학생 vs 학부모 (parental purchase funnels differ from student self-purchase funnels)
- Locale: ko_KR first; funnel text and legal copy differ by locale

### MDE Guidance

- Funnel completion rates at Qanda vary by funnel complexity: 20–70%
- At 70% baseline completion, a 5pp absolute improvement requires ~1,500 users per variant
- At 20% baseline completion, detecting 3pp absolute improvement requires ~3,000 users per variant
- Minimum weekly funnel entries per variant: 1,000 to detect meaningful effects within 2 weeks

### Example Baseline → Target Format

| Metric | Baseline | Target | MDE |
|---|---|---|---|
| 퍼널 완료율 (primary) | 42% | 48% | +4pp |
| 단계 3 이탈률 (sub) | 35% | 28% | Directional |
| 쿼터 도달 유저 비율 (sub) | 18% | 22% | Directional |
| D1 Retention (guardrail) | 38% | ≥ 36.1% | N/A |

---

## Template 5: 가격 테스트 (Pricing Tests)

**Experiment context:** Changes to subscription price points, pricing display, plan structure, discount offers, or trial length. At Qanda, pricing tests are among the highest-stakes experiment types because they directly affect revenue and user trust.

### Primary Metric

**기대 매출** (Expected Revenue) — not CVR alone

- Definition: Projected total revenue calculated by decomposing CVR × 객단가 per segment
- Formula:
  ```
  기대 매출 (variant) = Σ [ segment_size × CVR_variant(segment) × 객단가_variant(segment) ]
  기대 매출 (control) = Σ [ segment_size × CVR_control(segment) × 객단가_control(segment) ]
  Primary metric = 기대 매출 (variant) - 기대 매출 (control)
  ```
- Critical: A price increase WILL reduce CVR in most cases. Using CVR alone as the primary metric will cause you to reject a price increase that is revenue-positive. 기대 매출 captures the CVR-price trade-off in a single number.
- Measurement window: 30+ days minimum to capture at least one billing cycle

### Sub Metrics (3-5)

1. **CVR by price tier** — Conversion rate broken down by the specific price point offered to each variant group
   - Purpose: Shows the price elasticity curve — how much CVR drops per unit price increase

2. **1M Retention by segment** — 1-month subscription retention broken down by 학생/학부모 and 신규/기존
   - Formula: `(Active subscribers at day 30) / (Subscribers acquired during experiment window)`
   - Purpose: A price increase that acquires fewer but more committed subscribers may be net-positive; 1M Retention captures commitment

3. **객단가 realized** — Actual average revenue per subscribing user in each variant
   - Formula: `(Total subscription revenue) / (Total subscribers in variant)`
   - Purpose: Confirms that the price charged matches the price shown (implementation validation) and measures plan tier selection

4. **플랜 선택 분포** — Distribution of plan selections (monthly vs annual; individual vs family)
   - Purpose: Price changes may shift users between plans in ways that affect LTV beyond the first billing cycle

5. **구독 취소율 (30일 이내)** — Cancellation rate within 30 days of subscription start
   - Purpose: Leading indicator of whether the new price creates buyer's remorse

### Guardrail Metrics

1. **D1 Retention** — Must not drop
   - Threshold: No more than 5% relative decrease
   - Rationale: A pricing experiment that affects the subscriber pool composition may change D1 Retention for the overall cohort

2. **CVR 하락폭 한도** — Pre-defined maximum acceptable CVR drop
   - Threshold: Set BEFORE the experiment based on the team's revenue model (e.g., "CVR may drop by no more than 1.5pp absolute from baseline of 4.2%")
   - Rationale: Prevents shipping a price increase that is technically revenue-positive but destroys the subscriber base at an unacceptable rate
   - This threshold must be documented in the experiment design, not set after seeing results

### Recommended Segments

- MANDATORY split: 학생 vs 학부모 — proven to have opposite price sensitivity patterns at Qanda (학생: fast-buy, less price-sensitive to absolute price; 학부모: comparison-buy, more price-sensitive, longer consideration)
- Status split: 신규 vs 기존 vs 프리미엄 (re-subscription behavior differs significantly)
- Locale: ko_KR first and ONLY until results are validated — pricing norms and regulatory requirements differ across ja_JP, th_TH, vi_VN

### MDE Guidance

- Revenue metrics have variance 3–5x higher than conversion rate metrics — plan for longer windows
- Minimum window: 30 days; 45 days preferred
- Minimum sample: 500 purchases per variant to detect 5% 기대 매출 lift at 80% power
- Apply CUPED (variance reduction) if the Qanda data platform supports it — it can reduce required sample size by 30–50% for revenue metrics
- For large price increases (>20%): expect CVR to drop significantly; model the expected 기대 매출 delta before running to confirm the hypothesis is plausible

### Example Baseline → Target Format

| Metric | Baseline | Target | MDE |
|---|---|---|---|
| 기대 매출 (primary) | ₩12,500 / user | ₩14,000 / user (+12%) | +₩800 / user |
| CVR — 학생 전체 | 5.1% | 4.6% (expected drop) | Directional |
| CVR — 학부모 전체 | 3.2% | 2.7% (expected drop) | Directional |
| 1M Retention — 학생 | 62% | ≥ 60% | Directional |
| D1 Retention (guardrail) | 38% | ≥ 36.1% | N/A |
| CVR floor (guardrail) | — | Must not drop below 3.0% (학생), 2.0% (학부모) | N/A |

---

## Segmentation Reference (All Experiment Types)

Pre-register all segment analyses before the experiment launches. Segment analysis conducted after seeing results is post-hoc and will be rejected in Metric Review.

| Segment Dimension | Values | When to Always Apply |
|---|---|---|
| User Type | 학생 / 학부모 / 선생님 | CVR, 가격, 매출 experiments |
| User Status | 신규 / 기존 / 프리미엄 | All experiment types |
| Locale | ko_KR / ja_JP / th_TH / vi_VN | Any experiment with multi-locale rollout |
| Plan Type | 월간 / 연간 | 가격, 매출, 결제 experiments |
| Device | iOS / Android | Experiments touching payment UI (platform billing differences) |

For any segment analysis to be decision-relevant (rather than exploratory), it must appear in the pre-registered experiment design document in BigQuery or the PRD appendix before data collection begins.
