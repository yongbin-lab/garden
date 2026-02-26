# ab-test-analyzer

A/B 테스트 지표 설계 및 결과 분석 플러그인. 기획 문서에서 실험 지표를 설계하고, Mixpanel이나 Google Sheets 데이터를 통계 분석하여 의사결정을 돕습니다.

## Installation

```bash
claude plugin install /path/to/ab-test-analyzer --scope user
```

Or test locally:

```bash
claude --plugin-dir /path/to/ab-test-analyzer
```

### Prerequisites

- Python 3.x (통계 계산용)
- scipy, numpy, pandas는 첫 분석 시 자동 설치됨
- Mixpanel MCP 연결 (Mixpanel 데이터 조회용)
- Notion MCP 연결 (기획 문서 읽기용)

## Usage

### `/ab-design` — 지표 설계

기획 문서(Notion)를 입력하면 실험 지표를 설계합니다.

```
/ab-design https://notion.so/your-experiment-epic-page
```

**What it does:**
1. Notion 문서에서 가설, 타겟 유저, 기대 행동 변화 추출
2. 실험 유형 식별 (전환율/리텐션/결제/퍼널/가격)
3. Primary / Sub / Guardrail 지표 제안
4. 세그먼트 분석 계획 (학생/학부모, 신규/기존, 로케일)
5. Qanda Metric Review 템플릿 형식으로 지표 스펙 출력

### `/ab-analyze` — 결과 분석

실험 데이터를 입력하면 통계 분석 + 의사결정 권고를 제공합니다.

```
/ab-analyze https://mixpanel.com/project/xxx/view/xxx/app/boards#id=xxx
/ab-analyze https://docs.google.com/spreadsheets/d/xxx/edit
```

**What it does:**
1. Mixpanel 또는 Google Sheets에서 데이터 fetch
2. SRM(Sample Ratio Mismatch) 등 데이터 품질 검증
3. Python으로 통계 검정 실행 (카이제곱/t-test/Mann-Whitney)
4. p-value, 신뢰구간, 효과크기 계산
5. 시나리오별 트레이드오프 분석 (Ship / Don't ship / 더 돌려)
6. Qanda Metric Review 형식으로 결과 출력

### Skills (자동 트리거)

지표 설계나 통계 분석 관련 질문을 하면 자동으로 관련 지식이 주입됩니다:

- **ab-test-metric-design**: "어떤 지표 봐야 해?", "성공 기준 정해줘" 등
- **ab-test-statistical-methods**: "이 결과 유의미해?", "p-value 해석해줘" 등

## Components

| Type | Name | Purpose |
|---|---|---|
| Command | `/ab-design` | Notion 기획 문서 → 지표 스펙 |
| Command | `/ab-analyze` | 실험 데이터 → 통계 분석 + 의사결정 |
| Agent | `stat-analysis` | Python 통계 계산 전담 |
| Skill | `ab-test-metric-design` | 지표 설계 프레임워크 (콴다 특화) |
| Skill | `ab-test-statistical-methods` | 통계 검정 방법론 + discipline 강화 |

## File Structure

```
ab-test-analyzer/
├── plugin.json
├── README.md
├── commands/
│   ├── ab-design.md
│   └── ab-analyze.md
├── agents/
│   └── stat-analysis.json
└── skills/
    ├── ab-test-metric-design/
    │   ├── SKILL.md
    │   └── references/
    │       ├── metric-templates.md
    │       ├── metric-pitfalls.md
    │       └── qanda-metric-patterns.md
    └── ab-test-statistical-methods/
        ├── SKILL.md
        ├── references/
        │   ├── test-selection-guide.md
        │   └── python-templates.md
        ├── scripts/
        │   └── setup-stats-env.sh
        └── examples/
            ├── proportion_test.py
            └── multi_metric_bonferroni.py
```
