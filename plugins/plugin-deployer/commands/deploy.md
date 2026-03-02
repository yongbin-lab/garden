---
description: 플러그인을 GitHub 마켓플레이스에 배포합니다. 사용법 — /plugin-deployer:deploy <플러그인 경로>
---

# Plugin Deployer

사용자가 배포하려는 플러그인: $ARGUMENTS

아래 워크플로우를 순서대로 따르세요. 각 단계에서 문제가 생기면 멈추고 사용자에게 알려주세요.

---

## 1단계: 플러그인 검증

주어진 경로에서 플러그인 구조를 확인합니다:

1. `.claude-plugin/plugin.json`이 존재하는지 확인
2. `plugin.json`에서 `name`, `description`, `version` 필드 확인
3. 컴포넌트 디렉토리(commands/, skills/, agents/, hooks/)가 `.claude-plugin/` 바깥 플러그인 루트에 있는지 확인
4. 문제가 있으면 사용자에게 알리고 수정 제안

검증 통과 시 플러그인 정보를 요약해서 보여주세요:
- 이름, 설명, 버전
- 포함된 컴포넌트 목록

---

## 2단계: 기존 마켓플레이스 확인 및 배포 정보 수집

### 2-A: 기존 마켓플레이스 레포 탐색

기존 마켓플레이스가 있는지 **순서대로** 확인합니다:

1. `~/.claude/plugins/marketplaces/` 아래에 이미 등록된 마켓플레이스 디렉토리가 있는지 확인
2. 각 디렉토리에서 `.claude-plugin/marketplace.json`을 읽어 마켓플레이스 목록 파악
3. `git remote -v`로 해당 마켓플레이스의 GitHub 레포 URL 확인

**기존 마켓플레이스가 있으면:**
- 해당 마켓플레이스에 플러그인을 추가할지 물어보세요
- 기본값은 기존 마켓플레이스에 추가하는 것

**기존 마켓플레이스가 없으면:**
- 새 마켓플레이스 레포를 생성하는 흐름으로 진행

### 2-B: 배포 정보 수집

**기존 마켓플레이스에 추가하는 경우:**

| 항목 | 값 |
|------|-----|
| **마켓플레이스** | (탐색된 마켓플레이스 이름) |
| **레포** | (탐색된 GitHub URL) |

이 정보를 보여주고 "이 마켓플레이스에 추가할까요?" 한 번만 물어보세요.

**새 마켓플레이스를 만드는 경우:**

1. **GitHub 유저네임** — `gh api user --jq '.login'`으로 자동 감지. 실패하면 질문
2. **레포 이름** — 기본값: `<유저네임>-plugins`
3. **마켓플레이스 이름** — 기본값: `<유저네임>-plugins`
4. **공개/비공개** — 기본값: public
5. **라이선스** — 기본값: MIT

간단히 기본값을 보여주고 "이대로 진행할까요?" 한 번만 물어보세요.

---

## 3단계: 플러그인 배포

### 3-A: 기존 마켓플레이스에 추가

1. 마켓플레이스 디렉토리(`~/.claude/plugins/marketplaces/<마켓플레이스>/`)에서 작업
2. `plugins/<플러그인-이름>/` 디렉토리에 플러그인 복사
3. `.claude-plugin/marketplace.json`의 `plugins` 배열에 새 항목 추가
4. `README.md`에 새 플러그인 섹션 추가
5. git add, commit, push

**같은 이름의 플러그인이 이미 있으면:**
- 사용자에게 덮어쓸지 확인
- 덮어쓰는 경우 version을 비교해서 보여주기

### 3-B: 새 마켓플레이스 생성

1. `/tmp/<레포-이름>/` 에 마켓플레이스 구조 생성:

```
<레포-이름>/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── <플러그인-이름>/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       ├── skills/
│       └── ...
└── README.md
```

2. marketplace.json 생성:
```json
{
  "name": "<마켓플레이스-이름>",
  "owner": { "name": "<GitHub 유저네임>" },
  "metadata": {
    "description": "Claude Code plugins by <유저네임>",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "<플러그인-이름>",
      "source": "./<플러그인-이름>",
      "description": "<플러그인 설명>",
      "version": "<플러그인 버전>"
    }
  ]
}
```

3. README.md 생성 (마켓플레이스 이름, 플러그인 목록, 설치 방법 포함)
4. `gh auth status` 확인
5. `git init` + 초기 커밋
6. `gh repo create <레포-이름> --public --source=. --push`

---

## 4단계: 완료 안내

**기존 마켓플레이스에 추가한 경우:**
```
✅ 배포 완료!

📦 마켓플레이스: https://github.com/<유저네임>/<레포-이름>
📌 추가된 플러그인: <플러그인-이름> v<버전>

🔧 설치 방법:
  /plugin marketplace add <유저네임>/<레포-이름>
  /plugin install <플러그인-이름>@<마켓플레이스-이름>
```

**새 마켓플레이스를 생성한 경우:**
```
✅ 배포 완료!

📦 레포: https://github.com/<유저네임>/<레포-이름>

🔧 설치 방법:
  /plugin marketplace add <유저네임>/<레포-이름>
  /plugin install <플러그인-이름>@<마켓플레이스-이름>

📝 다음에 새 플러그인을 배포하면 이 마켓플레이스에 자동으로 추가됩니다.
```

---

## 중요 규칙

- `gh` CLI가 없으면 설치 방법을 안내하세요 (brew install gh)
- git config가 안 되어 있으면 설정을 도와주세요
- 절대 `--force` 푸시하지 마세요
- 민감한 파일(.env, credentials 등)이 있으면 경고하세요
- 기존 플러그인을 덮어쓰기 전에 반드시 사용자 확인
- 하나의 마켓플레이스 레포에 여러 플러그인을 관리하는 것이 기본 패턴
