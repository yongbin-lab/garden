# Translation Request Card Body Template

## Structure

The card body follows this exact structure in Notion-flavored Markdown:

```
### ⭐️ Guideline {color="blue_bg"}
- Assignee 와 Deadline 을 모두 넣어주시면 슬랙에 발송됩니다.
	<details>
	<summary>Assignee</summary>
		- ID : Yenny
		- TH : Cher
		- EN : Gina
		- ES : Jafet
		- VN : Nataly
		- JP : Alis
		- BR : Gina
		- DE, FR, IT, MY, RU, TR, TW : Gina
	</details>
	<details>
	<summary>Deadline</summary>
		- 1-29 sentences : 2 Working Days
		- 30-59 sentences : 3 Working Days
		- +60 sentences : 4 Working days
		- +100 sentences : 5 Working days
		**For each language, one person is in charge of translations.**
		**The schedule above also considers possible days off or leave. Depending on resources, the work might be finished sooner than the set deadline.**
	</details>
- 정확한 번역을 위해 영어 버전을 넣어주세요.
---
<empty-block/>
### About project
{ENGLISH_PROJECT_DESCRIPTION}
{FIGMA_SCREENSHOTS_OR_PROJECT_IMAGES}
<empty-block/>
### Action items
- [ ] [{LOKALISE_LINK_TEXT}]({LOKALISE_URL})
<empty-block/>
### Documents
<mention-page url="{{PROJECT_NOTION_URL}}"/>
{ADDITIONAL_FIGMA_OR_DOCUMENT_LINKS}
```

## Content Guidelines

### About project section
- Write in clear, professional English.
- Describe the project's purpose and what needs translation.
- Explain the user flow or feature context so translators understand the UI.
- Use numbered steps for sequential flows.
- Keep it concise but informative (3-8 sentences typically).

### Images
- Include Figma screenshots if Figma links are available in the project page.
- Use column layout for multiple images:
```
<columns>
	<column>
		![](image_url_1)
	</column>
	<column>
		![](image_url_2)
	</column>
</columns>
```

### Action items
- Each Lokalise URL becomes a checkbox item.
- Link text should be "app.lokalise.com" or a descriptive label.

### Documents
- Use `<mention-page>` to link the source project Notion page.
- Include Figma links as regular markdown links if present.
