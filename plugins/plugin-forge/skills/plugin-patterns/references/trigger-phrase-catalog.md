# Trigger Phrase Catalog

A library of proven trigger phrase structures for SKILL.md descriptions. Use these as templates when designing skill triggers.

---

## By Component Type

### For Plugin Development Skills
- "create a plugin"
- "build a Claude Code plugin"
- "write a SKILL.md"
- "design a command"
- "add an agent to my plugin"
- "create a hook"
- "add a PreToolUse hook" / "add a PostToolUse hook" / "add a SessionStart hook"
- "prevent Claude from [action]"
- "enforce [rule] automatically"
- "build a plugin that [does X]"

### For Workflow/Process Skills
- "start a new feature"
- "set up [workflow name]"
- "follow [process name]"
- "write a [test/spec/PR/design doc]"
- "review [code/PR/design]"
- "plan [task/project/sprint]"
- "write tests first" / "use TDD"
- "create a pull request"

### For Data/Analytics Skills
- "write a [Mixpanel/BigQuery/SQL] query"
- "analyze [metric/funnel/retention]"
- "build a dashboard"
- "run an A/B test analysis"
- "calculate [specific metric]"
- "query [specific table/dataset]"

### For Integration Skills
- "connect to [service]"
- "call the [API name] API"
- "set up [service name]"
- "send a message to Slack"
- "create a Notion page"
- "sync [data] with [service]"

### For Security/Quality Skills
- "review for security issues"
- "check for vulnerabilities"
- "deploy to production"
- "merge to main"
- "release [version]"
- "run a security audit"

---

## By Trigger Structure

### Action + Object (most common)
"[verb] a [specific noun]"
Examples: "create a hook", "write a migration", "build a dashboard"

### Action + Object + Target
"[verb] [object] to [target]"
Examples: "add rate limiting to the API", "connect the app to Stripe"

### Process Initiation
"set up [process]" / "start [workflow]"
Examples: "set up CI/CD", "start a code review", "begin a release"

### Enforcement Trigger
"prevent [action]" / "enforce [rule]" / "require [behavior]"
Examples: "prevent direct DB writes", "enforce branch naming", "require PR review"

### Negative Action (for Red Flags)
"[action] without [safeguard]"
Examples: "deploy without tests", "merge without review"
These are excellent Red Flags triggers — the skill should load and stop the unsafe action.

---

## Testing Your Triggers

Use this checklist for each trigger phrase:

1. **Specificity test**: Does this phrase narrow down to exactly this skill, or could it match multiple skills?
   - "write code" → too broad (fails)
   - "write a Mixpanel retention query" → specific enough (passes)

2. **Naturalness test**: Would a real user say this exact phrase while working?
   - "database operations management" → sounds like documentation (fails)
   - "query the BigQuery events table" → natural user speech (passes)

3. **Coverage test**: Do your 6-8 phrases cover the main ways users would request this?
   - Think about: different phrasings, different levels of specificity, different contexts
   - "create a hook", "add a hook", "new hook", "PreToolUse hook", "I need a hook" → good coverage

4. **Conflict test**: Is any trigger phrase shared with another skill you have?
   - If yes: add more specificity to disambiguate
   - "create a query" could be SQL or Mixpanel → "create a Mixpanel query" is unambiguous

---

## Full Example: Mixpanel Analytics Skill

Triggers for a Mixpanel-specific analytics skill:

```yaml
description: This skill should be used when the user asks to "write a Mixpanel query", 
  "analyze retention in Mixpanel", "build a Mixpanel funnel", "run a segmentation query", 
  "check event counts in Mixpanel", "query Mixpanel data", "create a Mixpanel dashboard", 
  or "look at user behavior in Mixpanel". Provides the project's Mixpanel event taxonomy, 
  property names, query patterns, and API authentication setup.
```

What makes these good:
- All include "Mixpanel" → no ambiguity with other analytics tools
- Cover different query types (retention, funnel, segmentation)
- Include "look at user behavior" → catches natural language requests
- End sentence states exactly what the skill provides

---

## Anti-Pattern Reference

Avoid these description patterns:

| Anti-Pattern | Why It Fails | Better Alternative |
|-------------|-------------|-------------------|
| "working with [tool]" | Too vague, no verb | "create a [tool] component", "query [tool] data" |
| "when you need help with X" | Not a user phrase | "write an X", "build an X", "review an X" |
| "provides guidance for" | Describes documentation, not a behavior | "use when [specific scenario]" |
| "assists with [domain] tasks" | Generic, matches everything | Specific actions in the domain |
| "can help when..." | Optional-sounding | "should be used when..." (mandatory) |
| Missing trigger phrases | Description relies on paraphrase | Always include quoted phrases |
