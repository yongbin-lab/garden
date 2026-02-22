tags: git, github, onboarding

# Git & GitHub 온보딩 정리

PM으로서 GitHub를 처음 세팅하며 정리한 핵심 개념과 설치 과정.

## Git vs GitHub

- **Git**: 코드의 변경 이력을 추적하는 도구. "코드의 타임머신". 내 컴퓨터에서 혼자 사용 가능.
- **GitHub**: Git으로 관리하는 코드를 인터넷에 올려두는 저장소. 협업, 백업, 공유 가능.

## 핵심 개념 4가지

- **Repository (레포)**: 프로젝트 폴더. 코드 + 변경 이력이 들어있음.
- **Commit (커밋)**: "지금 이 상태를 저장해둔다"는 행위. 게임의 세이브 포인트.
- **Branch (브랜치)**: 메인 코드를 건드리지 않고 실험할 수 있는 복사본.
- **Pull Request (PR)**: "내가 만든 브랜치를 메인에 합쳐도 될까요?" 요청하는 과정.

## PM 입장에서 GitHub가 필요한 이유

LLM이 짜준 코드를 잃어버리지 않고 버전 관리하기 위해서.
기능 추가 후 망가졌을 때 "이전 버전으로 돌아가기"가 가능하다.

## 설치 과정 (Mac)

```bash
# 1. Homebrew 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. GitHub CLI 설치
brew install gh

# 3. GitHub 로그인
gh auth login
# → GitHub.com → HTTPS → 브라우저 인증
```

## 배운 점

- gh CLI가 있으면 Claude Code에서 "깃헙에 올려줘"만으로 push까지 자동 처리된다
- 비개발자도 GitHub를 쓸 수 있고, 오히려 AI 시대에 PM이 직접 버전 관리를 하면 강력하다
