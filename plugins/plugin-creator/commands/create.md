---
description: 새로운 Claude Code 플러그인을 대화형으로 만들어줍니다
---

# Plugin Creator

사용자가 만들고 싶은 플러그인에 대해 설명했습니다: $ARGUMENTS

아래 워크플로우를 따라 플러그인을 만들어주세요.

## 1단계: 요구사항 정리

사용자의 설명을 분석해서 다음을 파악하세요:

- **플러그인 이름**: 소문자, 하이픈 허용 (예: `my-awesome-plugin`)
- **설명**: 플러그인이 하는 일 (1-2문장)
- **필요한 컴포넌트**:
  - `commands/` — 사용자가 `/이름:명령`으로 직접 호출하는 슬래시 커맨드
  - `skills/` — Claude가 맥락에 따라 자동으로 사용하는 Agent Skill
  - `agents/` — 특정 작업에 특화된 서브에이전트
  - `hooks/` — 이벤트(파일 저장, 도구 사용 등)에 반응하는 자동화
  - `.mcp.json` — 외부 도구/API 통합
  - `.lsp.json` — 코드 인텔리전스 (언어 서버)

정보가 부족하면 사용자에게 질문하세요. 충분하면 바로 2단계로 진행합니다.

## 2단계: 구조 확인

만들 플러그인의 구조를 사용자에게 보여주고 확인받으세요:

```
<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── commands/          (해당시)
├── skills/            (해당시)
├── agents/            (해당시)
├── hooks/             (해당시)
├── .mcp.json          (해당시)
└── .lsp.json          (해당시)
```

## 3단계: 파일 생성

사용자가 확인하면, 현재 작업 디렉토리에 플러그인을 생성하세요.

### plugin.json
```json
{
  "name": "<플러그인-이름>",
  "description": "<설명>",
  "version": "1.0.0",
  "author": {
    "name": "<작성자>"
  }
}
```

### Command 파일 (commands/<이름>.md)
```markdown
---
description: <이 커맨드가 하는 일>
---

<Claude에게 주는 지시사항>

사용자 입력: $ARGUMENTS
```

### Skill 파일 (skills/<이름>/SKILL.md)
```markdown
---
name: <skill-이름>
description: <Claude가 이 skill을 언제 사용해야 하는지>
---

<상세한 지시사항>
```

### Agent 파일 (agents/<이름>.md)
```markdown
---
name: <agent-이름>
description: <이 에이전트의 전문 분야>
model: sonnet
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

<에이전트 지시사항>
```

### Hooks 파일 (hooks/hooks.json)
```json
{
  "hooks": {
    "<이벤트명>": [
      {
        "matcher": "<도구 패턴>",
        "hooks": [{ "type": "command", "command": "<셸 명령>" }]
      }
    ]
  }
}
```
사용 가능한 이벤트: PreToolUse, PostToolUse, Notification, Stop, SubagentStop

## 4단계: 테스트 안내

생성 완료 후 사용자에게 알려주세요:

```bash
claude --plugin-dir ./<플러그인-이름>
```

그리고 각 커맨드와 기능을 어떻게 테스트하는지 구체적으로 안내하세요.

## 중요 규칙

- commands/, skills/, agents/, hooks/를 절대 `.claude-plugin/` 안에 넣지 마세요
- 플러그인 이름은 소문자 + 하이픈만 사용
- Skills는 `SKILL.md` (대문자), Commands는 소문자 `.md`
- 각 skill은 skills/ 아래 자체 하위 디렉토리 필요
- 빈 템플릿이 아닌 실제 동작하는 내용을 작성하세요
- 사용자의 언어에 맞춰 설명을 작성하세요
