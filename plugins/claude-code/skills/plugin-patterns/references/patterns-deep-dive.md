# Plugin Patterns: Deep Dive Reference

Detailed examples and explanations for each pattern in the plugin-patterns skill.

---

## Phase Structure: Full Example

From Anthropic's official `feature-dev` plugin:

```markdown
## Phase 1: Discovery
Read the repository structure and understand the codebase.
Launch 2 parallel agents to explore different areas...

**Gate:** Present understanding of the codebase to the user. Confirm you have enough context before proceeding.

## Phase 2: Clarifying Questions
**CRITICAL: This phase must not be skipped.**

Present specific questions about requirements, constraints, and edge cases...

**Gate:** Present all questions. Wait for answers. Summarize understanding. Confirm before Phase 3.

## Phase 3: Architecture Design
Launch 3 parallel architect agents, each proposing a different approach...

**Gate:** Present all 3 approaches with tradeoffs. Let user choose or ask for refinement. Do not proceed until choice is made.
```

Key observations:
- Gates use bold formatting to stand out
- Each gate specifies exactly what to present
- Phase 2 (clarifying questions) always has the CRITICAL marker
- User choice is required before architecture moves forward

---

## Progressive Disclosure: Before & After

### Before (common mistake — too much in SKILL.md)

```markdown
# Database Query Skill

Use this when writing queries...

## PostgreSQL Syntax
SELECT syntax...
INSERT syntax...
UPDATE syntax...
[500 lines of SQL reference]

## Index Optimization
Explain plans...
Query hints...
[300 lines of optimization guide]

## Connection Pooling
Pool configuration...
[200 lines]
```

Problems:
- 1,000+ words loaded every time skill is invoked
- Most content is irrelevant to any given query
- Wastes context window on rarely-needed details

### After (progressive disclosure done right)

SKILL.md body (~300 words):
```markdown
# Database Query Skill

Apply these patterns for all database operations in this project.

## Quick Reference

| Task | Pattern | Reference |
|------|---------|-----------|
| Complex SELECT | Use CTEs, not subqueries | references/query-patterns.md |
| Index optimization | Check EXPLAIN ANALYZE first | references/optimization-guide.md |
| Connection setup | Use the pool singleton | examples/db-connection.ts |

## Critical Rules

Always: Use parameterized queries. Never string-concatenate user input.
Always: Include LIMIT on queries without known cardinality.
Always: Check references/schema.md before assuming table structure.

Load `references/schema.md` when you need table structure.
Load `references/query-patterns.md` for complex query construction.
```

references/query-patterns.md (~800 words):
```markdown
# Query Patterns Reference

Detailed patterns for complex scenarios...
[All the detailed SQL syntax and patterns]
```

Result: Claude loads 300 words when the skill triggers, then fetches additional detail only when actually needed.

---

## Enforcement Language: Strength Comparison

### Weak enforcement (easily rationalized around)

```markdown
When working on new features, you should consider using test-driven development.
It's recommended to write tests before implementation when possible.
Try to follow the red-green-refactor cycle.
```

Claude will skip this whenever it "seems" unnecessary.

### Strong enforcement (closes loopholes)

```markdown
## The Iron Law

Write no production code before a failing test exists. This is not a preference.

**Red Flags — These thoughts mean you are rationalizing. Stop.**

| Thought | Reality |
|---------|---------|
| "This is just a simple fix" | Simple fixes caused 73% of production regressions in studies. Apply TDD. |
| "Tests would be hard to write here" | Hard-to-test code is a design problem. Write the test first — it will reveal the design issue. |
| "The user just wants this done fast" | The user wants it done correctly. TDD is faster than debugging. |
| "I'll add tests after" | "After" never comes. Write the test now. |

If you find yourself writing implementation code without a failing test, stop. Delete what you wrote. Write the test first.
```

The difference: weak enforcement leaves Claude free to judge whether the rule applies. Strong enforcement removes that judgment.

---

## Agent Persona: Before & After

### Weak persona (just a task list)

```markdown
You are a helpful code reviewer. Your job is to:
- Check code correctness
- Look for potential bugs
- Suggest improvements
- Review code style
```

This produces generic, mediocre reviews.

### Strong persona (specialized focus)

```markdown
You are a defensive code auditor. Your primary lens is: "what can go wrong at runtime, and what's the blast radius?"

For every function you examine, ask:
1. What are all possible inputs? (not just the happy path)
2. What happens at the boundaries? (null, empty, overflow, timeout)
3. If this fails, what breaks downstream?
4. What's the worst-case performance with real data volumes?

You are NOT looking for style issues, refactoring opportunities, or architectural improvements. Your only job is runtime correctness and failure modes.

Format your findings as:
**[CRITICAL/MAJOR/MINOR] Function name — Risk description**
Scenario: [exact input or condition that triggers this]
Failure: [what breaks when it triggers]
Fix: [specific change needed]
```

The strong version will consistently find real bugs. The weak version will produce a mix of style notes and vague suggestions.

---

## Trigger Phrase Catalog

### Structure patterns that work

"create a [component]" → "create a hook", "create an agent", "create a skill"
"add [feature] to [target]" → "add rate limiting to the API", "add a PreToolUse hook"
"set up [workflow]" → "set up TDD", "set up automated testing"
"write a [specific thing]" → "write a retention query", "write a migration"
"prevent Claude from [action]" → "prevent Claude from running destructive commands"
"enforce [rule]" → "enforce security review before deployment"
"[action] without [constraint]" → "deploy without tests" (for Red Flags triggers)

### Anti-patterns to avoid

"working with [tool]" → too vague, matches everything
"[noun] tasks" → "database tasks" — what kind? When?
"help with [domain]" → not a specific phrase users say
"when [condition]" → "when you need to think about X" — not a trigger phrase

### Testing your triggers

For each trigger phrase, ask:
1. Would a user say exactly this in a work context? (If not, rewrite it)
2. Does this phrase uniquely identify this skill vs others? (If ambiguous, add specificity)
3. Would Claude recognize this phrase as matching the description? (Test it)

---

## Session Bootstrap: Full Pattern

The session-start hook pattern from obra/superpowers:

```json
{
  "name": "load-project-skills",
  "description": "Loads project skill context at session start",
  "event": "SessionStart",
  "type": "prompt",
  "config": {
    "prompt": "<EXTREMELY_IMPORTANT>\nThis project uses a skill system that defines required behaviors. Before responding to the user's first message:\n\n1. Use the Skill tool to check available skills\n2. Load any skills relevant to what the user is asking\n3. Apply the skill's instructions as mandatory requirements, not suggestions\n\nSkipping skill invocation when a relevant skill exists is a quality failure. Skills are loaded automatically to prevent this — but you must still apply them.\n</EXTREMELY_IMPORTANT>"
  }
}
```

Why `<EXTREMELY_IMPORTANT>` works:
- Creates a clear visual anchor in the injected context
- Signals to Claude that this content has elevated priority
- The angle-bracket tag structure is familiar from training data
- Makes the enforcement intent unambiguous

The result: every session starts with Claude already primed to use skills, rather than needing to be reminded mid-conversation.
