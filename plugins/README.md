# Plugins & Tools

직접 만들거나 유용하게 사용 중인 플러그인과 도구를 모아둡니다.

## Claude Code Plugins

| Plugin | Description |
|--------|-------------|
| [`plugin-forge/`](./plugin-forge) | Claude Code 플러그인을 만들어주는 7단계 가이드 워크플로우 |
| [`translation-request/`](./translation-request) | Notion Global Translation DB에 번역 요청 카드를 자동 생성 |

## Installation

### 1. Clone

```bash
git clone https://github.com/yongbin-lab/garden.git ~/.claude-plugins/garden
```

### 2. Register in Claude Code settings

`~/.claude/settings.json`에 사용할 플러그인 경로를 추가합니다:

```json
{
  "plugins": [
    "~/.claude-plugins/garden/plugins/plugin-forge",
    "~/.claude-plugins/garden/plugins/translation-request"
  ]
}
```

필요한 플러그인만 골라서 등록하면 됩니다.

### 3. Restart Claude Code

설정 저장 후 Claude Code를 재시작하면 플러그인이 로드됩니다.

## Updating

```bash
cd ~/.claude-plugins/garden && git pull
```
