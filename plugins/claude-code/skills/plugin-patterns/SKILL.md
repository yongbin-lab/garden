---
name: plugin-patterns
description: This skill should be used when the user asks to "create a plugin", "build a skill", "write a command", "create an agent", "add a hook", "design a SKILL.md", "make a plugin component", or whenever any Claude Code plugin component is being created or reviewed. Provides the architectural patterns, quality standards, and design principles distilled from Anthropic's official plugin-dev and obra/superpowers.
version: 1.0.0
---

# Plugin Patterns

Apply these patterns whenever creating or reviewing any Claude Code plugin component. These are not suggestions — they are the standards that separate production-quality plugins from disposable ones.

## The Core Insight

High-quality plugins succeed because of three things, not one:

1. **Phase structure** — explicit checkpoints that gate progress and keep users in control
2. **Enforcement language** — absolute rules that close rationalization loopholes
3. **Progressive disclosure** — lean SKILL.md bodies with depth available on demand

A technically correct plugin that skips these has lower quality than one that applies them consistently.

---

## Skill Design

### The 3-Layer Model

Layer 1 — **Description** (always loaded, ~100 words max):
- Claude reads this to decide whether to invoke the skill
- Must use third-person: "This skill should be used when..."
- Must list specific trigger phrases in quotes
- Must end with one sentence explaining what the skill provides

Layer 2 — **SKILL.md body** (loaded when triggered, 1,500–2,000 words):
- Core concepts and essential decision points
- Quick reference tables
- Red Flags section if discipline-enforcing
- Explicit pointers to Layer 3 files

Layer 3 — **references/ examples/ scripts/** (loaded on demand, unlimited):
- Detailed API documentation → `references/`
- Working code templates → `examples/`
- Executable utilities → `scripts/`

### Trigger Phrase Design

Triggers must match words users actually say. Test each trigger phrase with: "Would a real user say this exact phrase while doing this task?"

Good triggers: "create a PreToolUse hook", "write a retention query", "set up TDD"
Bad triggers: "when working with hooks", "for analytics tasks", "database operations"

Provide 6-8 trigger phrases minimum. Include both short forms ("add a hook") and longer forms ("prevent Claude from running destructive commands").

### Imperative Form

Write skill bodies in imperative/infinitive form — verb first, no subject:
- ✅ "Load the schema before writing any configuration."
- ✅ "Validate output against the checklist before declaring done."
- ❌ "You should load the schema..."
- ❌ "Claude needs to validate..."

### Red Flags Section

Include in any discipline-enforcing skill. Name the specific rationalizations Claude will use to skip the behavior, and counter them directly.

Format:
```markdown
## Red Flags — Do Not Rationalize

| Rationalization | Reality |
|-----------------|---------|
| "This case is too simple" | Simple cases build bad habits. Apply it anyway. |
| "The user didn't ask for this" | The user asked for quality. |
| "I'll do it properly next time" | Apply it now. |
```

The Red Flags section works because it removes the middle ground — Claude can't skip the behavior without explicitly recognizing it's doing the thing the skill warned against.

---

## Command Design

### Phase Structure

Multi-step commands must use numbered phases with explicit Gate checkpoints:

```markdown
## Phase 1: Discovery
[Instructions for this phase]

**Gate:** [What to summarize and confirm before proceeding to Phase 2.]

## Phase 2: Design
...
```

Gates serve two purposes:
1. Keep the user informed and in control
2. Prevent Claude from rushing to implementation before requirements are clear

**Phase 3 (clarifying questions) is always the most important phase. Never skip it.**

### Frontmatter Discipline

```yaml
---
description: [What Claude should understand about this command's purpose]
argument-hint: [Brief hint for user — optional but valuable]
allowed-tools: [Minimal — only tools actually used]
---
```

Allowed-tools checklist:
- Read, Write, Bash, Glob, Grep → core tools, include if used
- TodoWrite → include only if tracking multi-step progress
- Task → include only if spawning parallel agents
- Skill → include only if loading skills
- AskUserQuestion → include only if interactive clarification needed

Never add tools speculatively. Every tool in the list adds surface area.

---

## Agent Design

### The Specialized Persona Rule

Agents must have a sharper focus than "Claude, but with these instructions." Define a genuine specialization.

Weak: "You are a helpful assistant that reviews code quality."
Strong: "You are a security-focused code auditor. Your primary lens is attack surface. For every function, you ask: who can call this, with what inputs, and what's the worst-case outcome?"

### Parallel Agent Patterns

Use parallel agents for:
- **Exploration**: 2-3 agents examine different aspects of the codebase simultaneously
- **Design alternatives**: 2-3 agents propose different approaches (minimal/clean/robust)
- **Review**: 3 agents with different lenses (correctness/enforcement/structure)

Each parallel agent must have a meaningfully different perspective — not just the same analysis done in parallel.

### whenToUse Specificity

Provide 3+ hyper-specific whenToUse examples, not categories:
- ❌ "Use when reviewing code"  
- ✅ "Use when a command has just completed Phase 5 implementation and all files are written — this agent validates them before presenting to the user"

---

## Hook Design

### Event Selection

| Event | Use When |
|-------|----------|
| SessionStart | Injecting context that should be present throughout the session |
| PreToolUse | Preventing specific tool calls or enforcing pre-conditions |
| PostToolUse | Validating results, logging, or triggering follow-up actions |
| Stop | Requiring sign-off before Claude declares a task complete |

### Prompt-Based vs Script-Based

**Prompt-based** (prefer this):
- Static context injection
- Rule enforcement
- No external dependencies
- Faster and more reliable

**Script-based** (use only when needed):
- Dynamic content (reading files, calling APIs)
- Environment-dependent behavior
- Must use `${CLAUDE_PLUGIN_ROOT}` for portability

### Session Bootstrap Pattern

The most powerful hook pattern: load critical skills at every SessionStart so Claude never starts a session without context.

```json
{
  "event": "SessionStart",
  "type": "prompt",
  "config": {
    "prompt": "<EXTREMELY_IMPORTANT>\nBefore responding to any user message, you MUST check available skills using the Skill tool. The skills in this plugin define required behaviors for this project. Skipping skill invocation when relevant is not acceptable.\n</EXTREMELY_IMPORTANT>"
  }
}
```

---

## plugin.json

Required structure:
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Clear 1-2 sentence description for marketplace display",
  "author": { "name": "...", "email": "..." },
  "commands": [...],
  "agents": [...],
  "skills": [...]
}
```

Skill description in plugin.json must match the description in SKILL.md. This is what users see before installing.

---

## Quality Checklist

Before declaring any plugin component done, verify:

**Skill:**
- [ ] Description is third-person with 4+ specific trigger phrases
- [ ] Body is 1,500–2,000 words in imperative form
- [ ] Detailed content is in references/, not SKILL.md body
- [ ] Red Flags section present if discipline-enforcing

**Command:**
- [ ] Frontmatter has description and allowed-tools
- [ ] Allowed-tools list is minimal
- [ ] Complex workflows have Phase headers and Gate checkpoints
- [ ] Instructions are written for Claude, not as user documentation

**Agent:**
- [ ] Has specialized persona (not generic helpfulness)
- [ ] whenToUse has 3+ hyper-specific examples
- [ ] Output format is specified precisely
- [ ] Tool list is minimal for the agent's focus

**Hook:**
- [ ] Uses ${CLAUDE_PLUGIN_ROOT} for all paths
- [ ] Prompt-based unless script features are genuinely needed
- [ ] Enforcement language is absolute, not suggestive

**Overall:**
- [ ] plugin.json references all components accurately
- [ ] All referenced files exist
- [ ] README explains the plugin clearly with concrete usage examples

Load `references/patterns-deep-dive.md` for detailed examples of each pattern type.
Load `references/trigger-phrase-catalog.md` for a library of proven trigger phrase structures.
