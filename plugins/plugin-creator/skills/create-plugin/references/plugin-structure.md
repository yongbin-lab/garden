# Claude Code Plugin Structure Reference

## Directory Layout

```
<plugin-name>/                  # Plugin root
├── .claude-plugin/             # Manifest directory (ONLY plugin.json goes here)
│   └── plugin.json             # Required: name, description, version
├── commands/                   # User-invoked slash commands
│   ├── review.md               # → /<plugin>:review
│   └── deploy.md               # → /<plugin>:deploy
├── skills/                     # Auto-triggered agent skills
│   ├── code-review/
│   │   ├── SKILL.md            # Required: frontmatter + instructions
│   │   └── references/         # Optional: additional context files
│   │       └── guidelines.md
│   └── testing/
│       └── SKILL.md
├── agents/                     # Specialized sub-agents
│   └── researcher.md           # Agent with specific model/tools
├── hooks/                      # Event-driven automation
│   └── hooks.json              # Hook definitions
├── .mcp.json                   # MCP server configurations
└── .lsp.json                   # LSP server configurations
```

## Component Selection Guide

### Use Commands when:
- The user should explicitly trigger the action
- It requires user input via $ARGUMENTS
- It's a workflow with clear start/end (e.g., deploy, scaffold, generate)

### Use Skills when:
- Claude should automatically activate based on context
- It enhances Claude's capabilities without explicit invocation
- Examples: code review patterns, testing strategies, documentation style

### Use Agents when:
- A task benefits from a specialized sub-agent
- You need a different model (e.g., haiku for fast tasks, opus for complex)
- The agent needs a restricted set of tools
- Examples: code researcher, test runner, documentation writer

### Use Hooks when:
- You want automation on specific events
- Examples: auto-lint after file write, notify on completion, validate before tool use

### Use MCP when:
- You need to integrate external APIs or tools
- Examples: database access, cloud services, third-party APIs

### Use LSP when:
- You need code intelligence for a specific language
- The language doesn't have an existing official LSP plugin

## Hook Events Reference

| Event | Trigger | Common Use |
|-------|---------|------------|
| PreToolUse | Before a tool executes | Validation, blocking |
| PostToolUse | After a tool executes | Linting, formatting |
| Notification | Claude sends a notification | Alerts, logging |
| Stop | Main agent stops | Cleanup, summary |
| SubagentStop | Sub-agent completes | Result processing |

## Naming Conventions

- Plugin name: lowercase, hyphens only (e.g., `my-plugin`)
- Command files: lowercase .md (e.g., `deploy.md`)
- Skill directories: lowercase, hyphens (e.g., `code-review/`)
- Skill file: always `SKILL.md` (uppercase)
- Agent files: lowercase .md (e.g., `researcher.md`)

## Skill Frontmatter Fields

```yaml
---
name: skill-name                    # Required
description: When to trigger        # Required — be specific about trigger conditions
disable-model-invocation: true      # Optional — if true, only user can invoke
---
```

## Agent Frontmatter Fields

```yaml
---
name: agent-name                    # Required
description: What this agent does   # Required
model: sonnet                       # Optional: sonnet (default), opus, haiku
tools:                              # Required: list of allowed tools
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
  - WebSearch
---
```
