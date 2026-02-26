---
description: "Analyze A/B test experiment results from Mixpanel or Google Sheets data. Fetches data, runs statistical analysis via the stat-analysis agent, interprets results, and provides decision recommendations with scenario-based tradeoff analysis."
argument-hint: "<mixpanel-url-or-google-sheets-url>"
allowed-tools: Skill, Read, Write, Bash, Task, WebFetch, mcp__claude_ai_Mixpanel__Run-Segmentation-Query, mcp__claude_ai_Mixpanel__Run-Funnels-Query, mcp__claude_ai_Mixpanel__Run-Retention-Query, mcp__claude_ai_Mixpanel__Run-Frequency-Query, mcp__claude_ai_Mixpanel__Get-Events, mcp__claude_ai_Mixpanel__Get-Property-Names, mcp__claude_ai_Mixpanel__Get-Property-Values, mcp__claude_ai_Mixpanel__Get-Projects, AskUserQuestion
---

# /ab-analyze

Analyze A/B test experiment results.

**Load the `ab-test-statistical-methods` skill using the Skill tool before proceeding.**

## Phase 1: Data Source Identification
Determine data source from `<argument>`:

**If Mixpanel URL:**
- Extract project info from URL
- Ask user: "어떤 실험의 데이터인가요? 실험 이름과 control/variant 구분 기준을 알려주세요."
- Use Mixpanel MCP tools to query relevant data (segmentation, funnels, retention as needed)

**If Google Sheets URL:**
- Convert to CSV export URL: replace `/edit` with `/export?format=csv`
- If sheet has multiple tabs, ask which tab: `&gid=SHEET_ID`
- Fetch CSV data using WebFetch

**If no argument:**
- Ask: "Mixpanel 대시보드 링크 또는 Google Sheets 링크를 주세요."

**Gate:** "이 데이터가 맞나요?" Show a summary of what was fetched (row count, columns, date range, groups).

## Phase 2: Data Preparation
- Identify control and variant groups
- Identify metric columns
- Check for data quality issues:
  - Sample Ratio Mismatch (SRM): if the group size ratio differs by more than 1% from the expected allocation, STOP the analysis. State: "This data has a Sample Ratio Mismatch. The randomization mechanism is compromised. Statistical results from this data are invalid. Diagnose and fix the SRM before rerunning the analysis." Do NOT proceed to Phase 3 until the SRM is resolved or the user provides an explanation that accounts for it.
  - Missing data
  - Outliers in continuous metrics
- Ask user for context if needed: "이 실험의 primary metric은 뭔가요?"

Check if a metric spec file exists from /ab-design. If found, use it to validate metric alignment.

**Gate:** "데이터 준비가 완료되었습니다. 분석을 시작할까요?"

## Phase 3: Statistical Analysis
Run `scripts/setup-stats-env.sh` first if needed (check if scipy is available).

Launch the `stat-analysis` agent using the Task tool with the following. Instruct the agent: "All results MUST be returned using the six-element Output Format Contract from the ab-test-statistical-methods skill: (1) Test selected, (2) Test statistic and p-value, (3) 95% CI, (4) Effect size, (5) Practical significance check, (6) Written recommendation. No other format is acceptable." Provide:
- The prepared data (as CSV or structured format)
- List of metrics to test
- Control and variant group labels
- Whether metrics are binary or continuous

Wait for agent results.

## Phase 4: Interpretation & Scenarios
Based on statistical results, generate scenario-based tradeoff analysis:

**Scenario A: Ship Variant**
- What the data supports
- Risks (if any metrics are borderline)
- Expected impact (기대 매출 change if applicable)

**Scenario B: Ship Control (Don't ship)**
- What the data shows against shipping
- Opportunity cost

**Scenario C: Extend Experiment (if applicable)**
- How much longer needed (from remaining runtime calculation)
- What additional signal you'd get
- Risk of continued experimentation

**Recommendation:**
Provide a clear recommendation with reasoning. Use the format:
1. What the data shows
2. What it does NOT show
3. Concrete recommendation with reasoning

## Phase 5: Output
Present results in Qanda's Metric Review format:

```markdown
### 1. 결과 한 줄 요약
> [Goal 달성/미달]. [One sentence summary with key numbers]

### 2. 가설 검증
**📊 Expected vs. Actual Comparison**
| 항목 | 기대 | 실제 | Gap & Interpretation |
|---|---|---|---|
| ... | ... | ... | ... |

**통계 분석 결과**
| Metric | Test | p-value | 95% CI | Effect Size | Significant? |
|---|---|---|---|---|---|

**🤔 Gap Reasoning**
[Why did the gap occur?]

### 3. 기타 인사이트 (탐색적 분석 — 의사결정 근거 아님)
[Additional observations from segment analysis, unexpected patterns, or exploratory findings. Label clearly as exploratory.]

### 4. 시나리오별 트레이드오프 분석
[Scenarios A, B, C as above]

### 5. Action Item
- [ ] [Concrete next steps]
```

Ask: "분석 결과를 파일로 저장할까요?"
