# 로컬 Claude Code 플러그인 설치 가이드

플러그인을 만든 후 실제로 사용 가능하게 만들기까지의 과정.

---

## 전제 조건

- 로컬 마켓플레이스가 이미 등록되어 있어야 함
- 마켓플레이스 경로: `/Users/mlt359/Desktop/local-marketplace`
- 플러그인 소스 보관 경로: `/Users/mlt359/garden/plugins/`

---

## Step 1: 플러그인 파일 구조 맞추기

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 필수! 간소화된 메타 (name, version, description만)
├── plugin.json              # 전체 매니페스트 (commands, agents, skills 등)
├── commands/
│   └── my-command.md
├── agents/
│   └── my-agent.md          # .md (YAML frontmatter), .json 아님!
├── skills/
│   └── my-skill/
│       └── SKILL.md
└── README.md
```

### 주의사항

| 항목 | 올바른 형식 | 잘못된 형식 |
|------|------------|------------|
| `.claude-plugin/plugin.json` | 반드시 존재해야 함 | 없으면 플러그인 인식 안 됨 |
| Agent 파일 확장자 | `.md` (YAML frontmatter) | `.json` |
| plugin.json 컴포넌트 경로 키 | `"file"` | `"path"` |
| Command frontmatter `allowed-tools` | 인라인 콤마: `Read, Write, Bash` | YAML 리스트: `- Read` |
| Skill 경로 | `skills/my-skill/SKILL.md` | `skills/my-skill` (디렉토리) |

### `.claude-plugin/plugin.json` (간소화 버전)

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "플러그인 설명"
}
```

### `plugin.json` (전체 매니페스트)

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "플러그인 설명",
  "author": { "name": "Author Name" },
  "commands": [
    {
      "name": "my-command",
      "description": "커맨드 설명",
      "file": "commands/my-command.md"
    }
  ],
  "agents": [
    {
      "name": "my-agent",
      "description": "에이전트 설명",
      "file": "agents/my-agent.md"
    }
  ],
  "skills": [
    {
      "name": "my-skill",
      "description": "스킬 설명",
      "file": "skills/my-skill/SKILL.md"
    }
  ]
}
```

### Command frontmatter 형식

```yaml
---
description: "커맨드 설명"
argument-hint: "<argument>"
allowed-tools: Skill, Read, Write, Bash, AskUserQuestion
---
```

### Agent `.md` 형식

```yaml
---
name: my-agent
description: "에이전트 설명"
whenToUse:
  - "구체적인 사용 시점 1"
  - "구체적인 사용 시점 2"
tools:
  - Bash
  - Read
  - Write
---

시스템 프롬프트 내용...
```

---

## Step 2: 소스를 garden/plugins에 배치

```bash
cp -r /path/to/my-plugin /Users/mlt359/garden/plugins/my-plugin
```

---

## Step 3: 로컬 마켓플레이스에 등록

### 3-1. 심볼릭 링크 생성

```bash
ln -s /Users/mlt359/garden/plugins/my-plugin /Users/mlt359/Desktop/local-marketplace/plugins/my-plugin
```

### 3-2. marketplace.json에 추가

`/Users/mlt359/Desktop/local-marketplace/.claude-plugin/marketplace.json`의 `plugins` 배열에 추가:

```json
{
  "name": "my-plugin",
  "description": "플러그인 설명",
  "source": "./plugins/my-plugin",
  "category": "development"
}
```

---

## Step 4: 마켓플레이스 업데이트 & 설치

```bash
claude plugin marketplace update local-plugins
claude plugin install my-plugin@local-plugins --scope user
```

이게 자동으로 해주는 것들:
- `~/.claude/plugins/cache/local-plugins/my-plugin/1.0.0/`에 파일 복사
- `~/.claude/plugins/installed_plugins.json`에 엔트리 추가
- `~/.claude/settings.json`의 `enabledPlugins`에 `true` 추가

---

## Step 5: 검증

```bash
# 구조 검증
claude plugin validate /Users/mlt359/garden/plugins/my-plugin

# 새 세션에서 /my-command 실행해보기
```

---

## 플러그인 수정 후 업데이트

소스 수정 후:

```bash
claude plugin update my-plugin@local-plugins
```

또는 캐시 직접 수정:

```bash
# 캐시 위치
/Users/mlt359/.claude/plugins/cache/local-plugins/my-plugin/1.0.0/
```

---

## 절대 하지 말 것

- `installed_plugins.json` 수동 편집 — `claude plugin install`이 해줌
- `settings.json`의 `enabledPlugins` 수동 편집 — `claude plugin install`이 해줌
- `~/.claude/plugins/cache/`에 직접 파일 복사 — 마켓플레이스 통해야 함
- Agent 파일을 `.json`으로 만들기 — 반드시 `.md` (YAML frontmatter)
- `plugin.json`에서 `"path"` 키 사용 — 반드시 `"file"`
