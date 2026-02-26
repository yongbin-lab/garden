---
description: "Guide A/B test metric design from a Notion planning document. Reads the experiment brief, proposes primary/sub/guardrail metrics, and outputs a structured metric spec matching Qanda's Metric Review template."
argument-hint: "<notion-url>"
allowed-tools: Skill, Read, Write, Glob, Grep, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, AskUserQuestion
---

# /ab-design

Design A/B test metrics from a planning document.

**Load the `ab-test-metric-design` skill using the Skill tool before proceeding.**

## Phase 1: Document Ingestion
If `<argument>` is a Notion URL:
- Fetch the document using `mcp__claude_ai_Notion__notion-fetch`
- Extract: experiment name, hypothesis, target user segment, expected behavior change

If no argument provided:
- Ask user for the Notion URL or ask them to paste the experiment brief

Summarize the extracted information:
- Experiment name
- Qualitative hypothesis (정성적 가설)
- Target users
- Expected behavior change

**Gate:** Confirm understanding with user. "이 가설이 맞나요?"

## Phase 2: Metric Selection
Apply the metric-design skill framework:

1. Identify experiment type (전환율/리텐션/결제/퍼널/가격)
2. Propose Primary Metric with rationale
3. Propose 3-5 Sub Metrics
4. Propose Guardrail Metrics (D1 Retention as default + others)
5. Define segments for analysis (학생/학부모, 신규/기존, 로케일)

Present as a table:

| Category | Metric | Definition | Baseline | Target | MDE |
|---|---|---|---|---|---|
| Primary | ... | ... | ... | ... | ... |
| Sub | ... | ... | ... | ... | ... |
| Guardrail | ... | ... | ... | ... | ... |

**Gate:** "이 지표 구성이 맞나요? 수정할 부분 있으면 말씀해주세요."

## Phase 3: Quantitative Expectations
For revenue-related experiments, calculate 기대 매출:
```
기대 매출 = Σ (segment_size × CVR × 객단가)
```

Set success criteria:
- Primary metric: specific threshold (e.g., "전환율 20% 상승")
- Guardrail: acceptable range (e.g., "D1 Retention 변화 없음")

**Gate:** "기대 매출 계산과 성공 기준이 맞나요? Baseline 수치나 기대치를 수정할 부분이 있으면 말씀해주세요."

## Phase 4: Output Generation
Generate the complete metric spec in Qanda's Metric Review Expected vs Actual template format:

```markdown
### 가설 검증

**🧪 Original Hypothesis (출시 전 가설)**
- 정성적 가설: [from document]
- 정량 기대치:
  - [Primary]: baseline → target
  - [Guardrail]: 유지
- 근거: [from document]

**📊 Expected vs. Actual Comparison**
| 항목 | 기대(Expectation) | 실제(Reality) | Gap & Interpretation |
|---|---|---|---|
| [Primary] | [target] | _실험 후 기입_ | |
| [Sub metrics...] | ... | _실험 후 기입_ | |
| [Guardrail] | 유지 | _실험 후 기입_ | |

**세그먼트 분석 계획**
- 학생 / 학부모
- 신규 / 기존
- 로케일: ko_KR, ja_JP, th_TH, vi_VN
```

Ask user: "이 지표 스펙을 파일로 저장할까요, 아니면 Notion에 작성할까요?"
