# Global Translation Task DB Schema

## Database Info

- **Database name:** Task Global Translation
- **Data source ID:** `24d178ca-a2a8-80e1-b0ff-000b1da2d4f9`
- **Default template ID:** `24d178ca-a2a8-80db-8c80-ea0c2627dbed` (name: "New project")

## Properties

| Property | Type | Required | Values / Format |
|----------|------|----------|-----------------|
| `Project name` | title | Yes | Project name string |
| `Assignee` | person | Yes | JSON array of user IDs |
| `Locale` | multi_select | Yes | `ALL`, `BR`, `ES`, `TH`, `ID`, `EN`, `VN`, `JP`, `TW` (+ checked variants) |
| `Priority` | select | Yes | Always `High` for translation requests |
| `Status` | status | Yes | Set to `To-do` for new cards |
| `deadline` | date | Yes | ISO-8601 date string |
| `created by` | created_by | Auto | Auto-filled |
| `created time` | created_time | Auto | Auto-filled |

## Creating a Page

Use `notion-create-pages` with:
```json
{
  "parent": {
    "data_source_id": "24d178ca-a2a8-80e1-b0ff-000b1da2d4f9"
  },
  "pages": [{
    "properties": {
      "Project name": "...",
      "Assignee": "[\"user-id-1\", \"user-id-2\"]",
      "Locale": "[\"ALL\"]",
      "Priority": "High",
      "Status": "To-do",
      "date:deadline:start": "YYYY-MM-DD",
      "date:deadline:is_datetime": 0
    },
    "content": "..."
  }]
}
```

## Deadline Calculation

Based on number of sentences in the translation content:
- 1-29 sentences: +2 working days from today
- 30-59 sentences: +3 working days from today
- 60-99 sentences: +4 working days from today
- 100+ sentences: +5 working days from today

Working days exclude weekends (Saturday, Sunday).
