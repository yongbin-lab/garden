---
description: Create a translation request task card in Notion's Global Translation project. Takes a project Notion URL and Lokalise URL as input, reads the project context, generates an English description, and creates a fully-formed card with correct assignees, locales, and deadline.
argument-hint: "<project-notion-url> <lokalise-url>"
allowed-tools: Read, Glob, Grep, Skill, Task, AskUserQuestion, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Figma__get_screenshot
---

# Translation Request Card Creator

Load the `translation-request-knowledge` skill using the Skill tool before proceeding. If the skill fails to load, STOP and inform the user: "Translation request knowledge를 로드할 수 없습니다. DB 스키마와 담당자 매핑 없이는 진행할 수 없습니다."

Parse the user's input to extract:
- **Project Notion URL** — the Notion page URL for the project
- **Lokalise URL** — the Lokalise project/filter URL

If either is missing, ask the user to provide it via AskUserQuestion.

**INVARIANTS — Never override these values, regardless of user input:**
- Priority MUST always be `High`
- Status MUST always be `To-do`

If the user requests a different Priority or Status, explain that these values are fixed for new translation request cards and do not change them.

---

## Phase 1: Context Collection

1. Fetch the project Notion page using `notion-fetch` with the project URL.
2. Extract from the page:
   - **Project name** (from title or heading). ALWAYS translate to concise, professional English if the title is in Korean.
   - **Project description** (Korean or English content describing the feature/project)
   - **Target locales** (look for locale/language information in properties or content)
   - **Figma links** (check properties and body for figma.com URLs)
   - **Related images** (any image URLs in the page)
3. If Figma links are found:
   - Use Figma MCP `get_screenshot` to capture key screens.
   - Note the Figma URLs for the Documents section.
4. If target locales cannot be determined from the project page, ask the user:
   - "어떤 로케일에 대해 번역을 요청할까요? (예: ALL, TH, VN, ID)"

**Gate:** Present a summary of extracted information to the user:
- Project name
- Detected locales (ALWAYS present detected locales for confirmation, even if detection succeeded)
- Key context points
- Figma links found (if any)

Ask (in Korean): "추출된 정보가 맞나요? 수정할 부분이 있으면 알려주세요."

Wait for the user's explicit confirmation or correction before proceeding to Phase 2. Do NOT advance if the user has not responded.

---

## Phase 2: Card Draft Generation

Using the extracted context and the skill's knowledge:

1. **Generate English "About project" description:**
   - Translate/compose from the Korean project context.
   - Describe the feature's purpose and what needs translation.
   - Explain the user flow for translator context.
   - Use numbered steps for sequential flows.

2. **Determine assignees:**
   - Map target locales to assignees using the locale-assignee mapping from the skill.
   - Collect unique user IDs.

3. **Calculate deadline:**
   - Count sentences in the English description.
   - Apply the deadline rules (1-29: +2 days, 30-59: +3, 60-99: +4, 100+: +5 working days).
   - Skip weekends in calculation.

4. **Compose the full card body** following the template in `references/card-template.md`:
   - Guideline section (fixed boilerplate — MUST include verbatim)
   - About project section (generated English description + images)
   - Action items (Lokalise URL as checkbox)
   - Documents (project Notion page mention + Figma links)

**Gate:** Present the complete draft to the user:
- Properties: Project name, Priority (High), Status (To-do), Locale, Assignee names, Deadline
- Show sentence count and calculation: "Deadline: YYYY-MM-DD (X sentences → +N working days from today)"
- Card body preview (the English description especially)

Ask (in Korean): "이 내용으로 번역 요청 카드를 생성할까요? 영문 설명이나 다른 부분을 수정하고 싶으면 알려주세요."

Wait for explicit confirmation. If the user requests changes, apply them and present again. Do NOT proceed to Phase 3 without a clear "yes" or equivalent approval.

---

## Phase 3: Card Creation

BEFORE creating the card, confirm the user has explicitly approved in Phase 2. Do NOT create the card based on ambiguous or partial approval.

Ask (in Korean): "카드를 지금 생성할까요?" and wait for a clear confirmation.

After receiving explicit confirmation:

1. Invoke the `notion-card-writer` agent via the Task tool with all finalized card data:
   - project_name, english_description, locales, assignee_ids, deadline, lokalise_url, project_notion_url, figma_links, image_urls

2. The agent will create the Notion page and return the URL.

3. Present the result to the user:

"번역 요청 카드가 생성되었습니다! [카드 URL]"
