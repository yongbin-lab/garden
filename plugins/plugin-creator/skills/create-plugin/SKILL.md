---
name: create-plugin
description: Creates a new Claude Code plugin when the user wants to build, make, or scaffold a plugin. Triggers on phrases like "플러그인 만들어줘", "플러그인 만들고 싶어", "create a plugin", "build a plugin", "make a plugin".
---

# Plugin Creator Skill

You are a Claude Code plugin creation assistant. When the user describes a plugin they want to create, follow this structured workflow.

## When to Activate

Activate when the user expresses intent to create a Claude Code plugin, such as:
- "~하는 플러그인 만들어줘"
- "~하는 플러그인 만들고 싶어"
- "I want to create/build/make a plugin that..."
- "Can you make a plugin for..."

## Workflow

### Step 1: Understand Requirements

From the user's description, determine:

1. **Plugin name** — lowercase with hyphens (e.g., `code-reviewer`, `auto-formatter`)
2. **Purpose** — what problem does it solve? (1-2 sentences)
3. **Components needed** — which of these does the plugin require?

| Component | Directory | Use When |
|-----------|-----------|----------|
| Commands | `commands/` | User explicitly invokes via `/<plugin>:<command>` |
| Skills | `skills/` | Claude should auto-trigger based on context |
| Agents | `agents/` | Task needs a specialized sub-agent with specific tools/model |
| Hooks | `hooks/` | Automation on events (file save, tool use, etc.) |
| MCP | `.mcp.json` | External API/tool integration needed |
| LSP | `.lsp.json` | Code intelligence for a programming language |

If the user's description is vague, ask targeted questions. If clear enough, proceed directly.

### Step 2: Present the Plan

Show the user the proposed plugin structure as a tree diagram, listing each file that will be created with a one-line explanation. Ask for confirmation before creating files.

### Step 3: Create the Plugin

Create all files in the current working directory under `<plugin-name>/`.

**Critical rules:**
- `.claude-plugin/plugin.json` goes inside `.claude-plugin/`
- Everything else (commands/, skills/, agents/, hooks/, .mcp.json, .lsp.json) goes at the plugin ROOT level
- NEVER nest component directories inside `.claude-plugin/`
- Write real, functional content — not placeholder templates
- Match the user's language for descriptions (Korean descriptions for Korean users, etc.)
- Plugin name in plugin.json must be lowercase with hyphens only

#### File Templates

**plugin.json:**
```json
{
  "name": "<name>",
  "description": "<description>",
  "version": "1.0.0",
  "author": { "name": "<author>" }
}
```

**Command (commands/<name>.md):**
```markdown
---
description: <what this command does>
---

<Detailed instructions for Claude>

User input: $ARGUMENTS
```

**Skill (skills/<name>/SKILL.md):**
```markdown
---
name: <name>
description: <when Claude should auto-trigger this skill — be specific>
---

<Comprehensive instructions including:
- What to do step by step
- What tools to use
- What output format to produce
- Edge cases to handle>
```

**Agent (agents/<name>.md):**
```markdown
---
name: <name>
description: <specialization>
model: sonnet
tools:
  - <list only tools this agent needs>
---

<Agent behavior instructions>
```

**Hooks (hooks/hooks.json):**
```json
{
  "hooks": {
    "<Event>": [
      {
        "matcher": "<tool-pattern>",
        "hooks": [{ "type": "command", "command": "<shell-command>" }]
      }
    ]
  }
}
```
Available events: PreToolUse, PostToolUse, Notification, Stop, SubagentStop

### Step 4: Test Instructions

After creating all files, provide the user with:

1. **How to load**: `claude --plugin-dir ./<plugin-name>`
2. **How to test each component**: specific commands to try
3. **How to iterate**: edit files and restart Claude Code to pick up changes
4. **How to share**: mention `plugin.json` versioning and marketplace deployment

## Quality Checklist

Before finishing, verify:
- [ ] plugin.json has valid name, description, version
- [ ] No component directories are inside .claude-plugin/
- [ ] Each skill has its own subdirectory with SKILL.md
- [ ] Commands have descriptive frontmatter
- [ ] All file content is functional, not boilerplate
- [ ] Skill descriptions clearly state trigger conditions
- [ ] Agent tool lists are minimal (only what's needed)
