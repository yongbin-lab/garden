---
description: "This skill should be used when the user says \"번역 요청 만들어줘\", \"translation request 생성\", \"번역 카드 작성\", \"Lokalise 번역 요청\", \"create translation card\", \"번역 요청 노션 카드\", \"노션에 번역 요청 올려줘\", or \"새 번역 배치 요청\". It provides the Global Translation Notion DB schema, locale-to-assignee mappings, card body template, and deadline calculation rules needed to create a properly formatted translation request task card."
---

# Translation Request Knowledge

## Purpose

Provide all team-specific knowledge required to create translation request task cards in the Mathpresso Global Translation Notion database.

## Core Workflow

Accept exactly two inputs from the user:
1. **Project Notion URL** — the source project page to extract context from
2. **Lokalise URL** — the link to the Lokalise translation project/filter

Generate a fully-formed Notion task card in the Global Translation DB with correct English description, locale-based assignees, auto-calculated deadline, and proper card body following the team template.

## DB Target

- **Database:** Task Global Translation
- **Data source ID:** `24d178ca-a2a8-80e1-b0ff-000b1da2d4f9`

## Invariant Properties

These values MUST NOT be changed regardless of user input:
- `Priority` → ALWAYS `High`
- `Status` → ALWAYS `To-do`

## Variable Properties

| Property | How to Determine |
|----------|-----------------|
| `Project name` | Extract from project page title or context. ALWAYS translate to concise, professional English if the title is in Korean. |
| `Locale` | Determine from project page. ALWAYS confirm with user. Only use `ALL` if project explicitly targets all locales. |
| `Assignee` | Map from locale. See `references/locale-assignee-mapping.md` for full mapping with User IDs. |
| `deadline` | Calculate from sentence count. See `references/notion-db-schema.md` for rules and DB creation format. |

## Card Body Structure

Follow the exact template in `references/card-template.md`. The card body has four sections:

1. **Guideline** — Fixed boilerplate. MUST include verbatim. Do NOT skip or abbreviate.
2. **About project** — English description. Generate from Korean project context.
3. **Action items** — Lokalise URL as checkbox items.
4. **Documents** — Mention the source project Notion page + any Figma links found.

## English Description Rules

Write the "About project" section in clear, professional English. Follow these rules absolutely:
- Describe what the project/feature does and why translation is needed.
- Explain the user flow so translators understand UI context.
- Use numbered steps for sequential flows.
- Keep concise: 3-8 sentences typically.
- Base the description on the Korean project context from the Notion page.
- Do NOT paraphrase loosely — translators depend on precision.

## Figma Integration

Check the project Notion page for Figma links in properties or body content:
- If found, use Figma MCP `get_screenshot` to capture design screenshots.
- Include screenshots in the "About project" section using column layout.
- Include Figma links in the "Documents" section.

## Red Flags — Do Not Rationalize

| Rationalization | Required Action |
|-----------------|-----------------|
| "The English description looks close enough" | STOP. You MUST show the exact description to the user and get explicit approval before proceeding. |
| "I'll skip the assignees, the PM can add them" | You MUST set Assignee. Cards without Assignee WILL NOT trigger Slack notifications. This is not optional. |
| "ALL locale is fine, I don't need to check" | You MUST check the project page for locale information. Only use ALL if the project explicitly targets all locales. Ask the user if unclear. |
| "The Guideline section is boilerplate, I'll skip it" | You MUST include the Guideline section verbatim. It is required by the translation team. No exceptions. |

Load `references/locale-assignee-mapping.md` for full locale details and User IDs.
Load `references/notion-db-schema.md` for complete DB schema, creation format, and deadline rules.
Load `references/card-template.md` for the exact card body template.
