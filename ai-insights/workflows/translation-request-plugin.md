# Workflow: Claude Code Plugin 만들기 (Plugin Forge)

> 번역 요청 자동화 플러그인을 만들면서 정리한 Plugin Forge 7-Phase 워크플로우

## 배경

PM이 Lokalise 번역 요청을 할 때마다 Notion에 영문 카드를 수동으로 만드는 반복 작업이 있었다.
이걸 Claude Code 플러그인으로 자동화하기로 했다.

**입력:** 프로젝트 Notion 링크 + Lokalise URL
**출력:** Global Translation DB에 완성된 번역 요청 카드 자동 생성

---

## 7-Phase 워크플로우

### Phase 1: Concept Discovery

**목표:** 플러그인이 해결할 문제와 대상 사용자 파악

- 어떤 반복 작업을 없애고 싶은지 정의
- 플러그인 유형 분류: workflow automation / knowledge injection / quality gate / integration toolkit
- **2문장으로 플러그인 목적 요약** → 유저 확인

우리 케이스:
> "번역 요청 Notion 카드 생성을 자동화하는 플러그인. PM이 프로젝트 컨텍스트를 한글로 간단히 설명하면, 고품질 영문 번역과 함께 Notion 양식에 맞춘 번역 요청 카드를 자동 생성하고 담당자 태그 및 property를 채워준다."

**Gate:** 목적 요약 확인받고 다음으로.

---

### Phase 2: Component Architecture

**목표:** 필요한 컴포넌트 종류와 개수를 정확히 결정

`needs-analyzer` 에이전트가 컨셉을 분석해서 컴포넌트 플랜을 제안한다.

| 컴포넌트 | 언제 쓰나 |
|----------|-----------|
| **Skill** | Claude에게 팀 고유 지식을 주입할 때 (DB 스키마, 담당자 매핑 등) |
| **Command** | 유저가 시작하는 구조화된 멀티스텝 액션 |
| **Agent** | 특화된 서브태스크를 분리 실행할 때 |
| **Hook** | Claude Code 이벤트에 자동 반응할 때 |

우리 결과:
- Skill 1개: DB 스키마 + 담당자 매핑 + 카드 템플릿 + 데드라인 규칙
- Command 1개: `/translation-request` (3단계 워크플로우)
- Agent 1개: `notion-card-writer` (Notion MCP 호출 전담)
- Hook: 없음 (PM이 직접 시작하는 워크플로우라 자동 트리거 불필요)

**Gate:** 컴포넌트 테이블 확인받고 다음으로.

---

### Phase 3: Detailed Design & Clarifying Questions

**목표:** 각 컴포넌트를 정확하게 명세. 모든 애매한 점 해소.

**이 단계가 가장 중요하다. 절대 건너뛰지 말 것.**

확인해야 할 것들:
- Command의 입력값과 각 Phase의 구체적 동작
- Skill에 들어갈 팀 고유 지식 (Notion DB 스키마, 담당자 User ID 등)
- Agent의 역할 범위와 출력 형식

우리가 한 것:
1. **Notion MCP로 실제 DB 스키마 읽기** → property 목록, 타입, 옵션값 파악
2. **예시 카드 읽기** → 본문 양식(Guideline, About project, Action items, Documents) 파악
3. **담당자 User ID 조회** → Notion 검색으로 6명의 실제 User ID 확보
4. **Notion Enhanced Markdown 스펙 확인** → 카드 본문 포맷팅 규칙 파악

핵심 결정사항:
- Priority는 항상 High
- Locale는 프로젝트 Notion 페이지에서 추출
- Deadline은 문장 수 기반 자동 계산 + PM 확인 가능
- Figma 링크도 프로젝트 페이지에서 추출하여 카드에 포함

**Gate:** 전체 명세 확인받고 다음으로.

---

### Phase 4: Skill Design Sprint

**목표:** SKILL.md를 Progressive Disclosure 원칙에 따라 설계

Skill은 3-Layer 모델을 따른다:
1. **Description** (~100 words) — Claude가 스킬을 호출할지 판단하는 라우팅 정보
2. **SKILL.md body** (1,500~2,000 words) — 핵심 개념과 의사결정 포인트
3. **references/** — 상세 데이터 (DB 스키마, 담당자 매핑 전체, 카드 템플릿)

중요 원칙:
- Description은 **3인칭** + **구체적 트리거 문구** 포함
- Body는 **명령형** ("Load X. Run Y. Validate Z.")
- 상세 데이터는 references/에 분리 (유지보수 용이)
- 규율 강제 스킬이면 **Red Flags 섹션** 포함

```
references/
├── locale-assignee-mapping.md  # 로케일→담당자 User ID 전체 매핑
├── notion-db-schema.md         # DB 스키마 + 페이지 생성 JSON 포맷
└── card-template.md            # 카드 본문 Notion Markdown 템플릿
```

**Gate:** Skill 설계 확인받고 다음으로.

---

### Phase 5: Full Implementation

**목표:** 모든 컴포넌트를 패턴에 맞게 구현

구현 순서:
1. `plugin.json` — 플러그인 메타데이터 + 컴포넌트 경로
2. Skill 파일 (SKILL.md + references/)
3. Command 파일 — Phase 구조 + Gate 체크포인트
4. Agent 파일 — whenToUse 예시 + 전문화된 시스템 프롬프트
5. README.md

Command 설계 핵심:
- 번호 매긴 Phase + 각 Phase 끝에 **Gate** (유저 확인 후 진행)
- `allowed-tools`는 **실제 사용하는 것만** (최소화)
- Phase 3(카드 생성)에서는 Agent에게 위임

Agent 설계 핵심:
- `whenToUse`에 3개 이상 **구체적 시나리오** 기술
- Pre-flight validation으로 필수 필드 누락 방지
- 도구 목록 최소화

**Gate:** 전체 파일 트리 확인.

---

### Phase 6: Quality Review

**목표:** 프로덕션 수준 검증

3개 리뷰어를 **병렬 실행**:

| 리뷰어 | 관점 |
|--------|------|
| **Design Quality** | 트리거 문구, Phase 구조, Progressive Disclosure |
| **Enforcement Strength** | Red Flags, 절대적 규칙, 합리화 차단 |
| **Structural Correctness** | plugin.json 유효성, 파일 참조, README 완성도 |

우리가 발견하고 수정한 것들:
- Phase 3에 명시적 Gate 없었음 → 카드 생성 전 확인 추가
- Red Flags가 설명적이었음 → "STOP", "MUST" 등 절대적 지시문으로 강화
- Command가 Agent 역할을 중복하고 있었음 → Agent에게 위임하도록 분리
- SKILL.md에 references/ 내용이 중복되어 있었음 → 삭제하고 포인터만 유지

**Gate:** Critical 이슈 0개 확인.

---

### Phase 7: Documentation & Delivery

**목표:** 즉시 사용 가능하도록 패키징

- README에 설치 방법, 사용 예시, 컴포넌트 설명 포함
- 테스트 방법 안내
- settings.json에 플러그인 등록

---

## 최종 결과물

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

## 핵심 교훈

1. **Phase 3(상세 설계)이 가장 중요하다** — 실제 데이터(DB 스키마, User ID)를 확보하지 않으면 플러그인이 제대로 동작하지 않는다.
2. **Progressive Disclosure를 지켜라** — SKILL.md에 모든 걸 넣으면 유지보수가 어렵다. 상세 데이터는 references/로 분리.
3. **Gate는 반드시 명시적으로** — "Wait for explicit confirmation"을 빠뜨리면 Claude가 확인 없이 진행할 수 있다.
4. **Red Flags는 설명이 아니라 명령** — "이렇게 하면 안 좋아요" 대신 "STOP. MUST. DO NOT."
5. **Agent와 Command의 역할을 분리하라** — 둘 다 같은 도구를 쓰면 누가 실행할지 모호해진다.
6. **Quality Review는 병렬로** — 3개 관점(Design, Enforcement, Structure)을 동시에 돌리면 빠르고 포괄적.
