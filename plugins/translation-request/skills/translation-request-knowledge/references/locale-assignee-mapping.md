# Locale-to-Assignee Mapping

## Notion User IDs by Locale

| Locale | Assignee | Notion User ID |
|--------|----------|----------------|
| ID | Yenny Anwar | `d2ade224-da3f-48d6-9705-8bb977500bea` |
| TH | Cher Waran | `f1f467b8-cbe2-4933-83dd-725d9c408c0f` |
| EN | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |
| ES | Jafet Velasquez | `3aa0b776-64d7-407f-abb4-0b247292fdc3` |
| VN | Nataly | `eeefdd24-fe95-4c61-a6ce-9aa1a085fa55` |
| JP | Alis Saefurrachman | `08d45fb7-62ee-43f8-96f3-cee4f2c31026` |
| BR | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |
| TW | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |
| DE | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |
| FR | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |
| IT | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |
| MY | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |
| RU | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |
| TR | Gina | `df31f2cd-1cf5-4671-bc11-ac1cf5456b55` |

## How to Use

When creating a translation request card:
1. Determine which locales the project targets.
2. Look up the assignee for each target locale.
3. Deduplicate user IDs (Gina covers multiple locales).
4. Set the `Assignee` property as a JSON array of unique user IDs.

## Locale Property Values

The `Locale` multi_select property uses these exact values:
- `ALL` — all locales
- Individual locales: `BR`, `ES`, `TH`, `ID`, `EN`, `VN`, `JP`, `TW`
- Checked variants (translation complete): `BR ☑️`, `ES ☑️`, `TH ☑️`, `ID ☑️`, `EN ☑️`, `VN☑️`, `JP ☑️`, `TW ☑️`, `ALL✅`

When creating a new card, use the unchecked locale names (e.g., `TH`, `VN`, `ID`), or `ALL` if all locales are targeted.
