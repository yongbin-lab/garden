# Translation Request Plugin

Notion Global Translation 프로젝트에 번역 요청 Task 카드를 자동 생성하는 Claude Code 플러그인.

## 해결하는 문제

PM이 번역 요청 시 수동으로 해야 하는 작업을 자동화합니다:
- 프로젝트 설명을 영어로 번역/작성
- Notion 카드 생성 및 property 채우기 (Priority, Status, Locale, Deadline)
- 로케일별 담당자 자동 태그
- 문장 수 기반 데드라인 자동 계산
- Figma 디자인 스크린샷 자동 첨부

## 설치

```bash
# 유저 스코프에 설치
claude plugin install ~/.claude/plugins/translation-request --scope user

# 또는 테스트용으로 실행
claude --plugin-dir ~/.claude/plugins/translation-request
```

## 사용법

### 커맨드: `/translation-request`

```
/translation-request <프로젝트-Notion-URL> <Lokalise-URL>
```

**예시:**
```
/translation-request https://www.notion.so/mathpresso/MyProject-abc123 https://app.lokalise.com/project/123456/?view=multi
```

**워크플로우 (3단계):**

1. **컨텍스트 수집** — 프로젝트 Notion 페이지에서 이름, 설명, 로케일, Figma 링크 자동 추출. PM이 확인.
2. **카드 초안 생성** — 영문 설명 자동 생성, 담당자 매핑, 데드라인 계산. PM이 영문 설명과 전체 내용 확인/수정.
3. **카드 생성** — PM 최종 확인 후 Global Translation DB에 카드 생성. URL 반환.

### 스킬: 번역 요청 관련 대화

다음과 같은 말에 자동으로 활성화됩니다:
- "번역 요청 만들어줘"
- "번역 카드 작성"
- "Lokalise 번역 요청"
- "create translation card"

## 컴포넌트

| 타입 | 이름 | 설명 |
|------|------|------|
| Skill | `translation-request-knowledge` | DB 스키마, 담당자 매핑, 카드 템플릿, 데드라인 규칙 주입 |
| Command | `/translation-request` | 3단계 카드 생성 워크플로우 (Gate 체크포인트 포함) |
| Agent | `notion-card-writer` | 확정된 데이터로 Notion MCP 호출하여 카드 생성 (자동 호출) |

## 요구사항

- **필수:** Notion MCP 서버 연결
- **선택:** Figma MCP 서버 연결 (디자인 스크린샷 자동 첨부용)

## 파일 구조

```
translation-request/
├── plugin.json
├── README.md
├── skills/
│   └── translation-request-knowledge/
│       ├── SKILL.md
│       └── references/
│           ├── locale-assignee-mapping.md
│           ├── notion-db-schema.md
│           └── card-template.md
├── commands/
│   └── translation-request.md
└── agents/
    └── notion-card-writer.md
```
