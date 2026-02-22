# plugin-forge

**A guided 7-phase workflow for creating high-quality Claude Code plugins.**

Stop generating mediocre plugins with a single prompt. Plugin Forge guides you through discovery, architecture, design, and implementation — with parallel expert agents and quality validation — producing plugins that match the standards of Anthropic's official plugin-dev and obra/superpowers.

---

## What Makes This Different

Most plugin builders dump code and hope for the best. Plugin Forge applies the patterns that make top plugins work:

- **7-phase workflow** with explicit user gates at every decision point
- **Parallel expert agents** — needs analyzer, skill architect, component builder, quality reviewer
- **Progressive disclosure** — lean SKILL.md bodies with depth in references/
- **Enforcement language** — Red Flags sections that close rationalization loopholes
- **Session bootstrap** — hooks that ensure standards are applied every time

---

## Installation

```bash
# Install to user scope (available in all projects)
claude plugin install /path/to/plugin-forge --scope user

# Or install to project scope
claude plugin install /path/to/plugin-forge --scope project
```

---

## Usage

### Create a new plugin

```
/create
```

Starts the guided 7-phase workflow. You'll be walked through:
1. Concept discovery
2. Component architecture
3. Detailed design and clarifying questions
4. Skill design sprint
5. Full implementation
6. Quality review
7. Documentation and delivery

### Create with a concept

```
/create A plugin that enforces security review before any deployment command
```

Phase 1 will use your description as a starting point.

---

## Components

### Commands
| Command | Description |
|---------|-------------|
| `/create` | Guided 7-phase plugin creation workflow |

### Agents
| Agent | Focus |
|-------|-------|
| `needs-analyzer` | Determines optimal component architecture from a plugin concept |
| `skill-architect` | Designs SKILL.md with progressive disclosure and trigger phrases |
| `component-builder` | Implements commands, agents, hooks, and plugin.json |
| `quality-reviewer` | Validates against production plugin standards |

### Skills
| Skill | Triggers |
|-------|---------|
| `plugin-patterns` | "create a plugin", "write a SKILL.md", "build a command", "add a hook", and more |

### Hooks
| Hook | Event | Behavior |
|------|-------|---------|
| `bootstrap-plugin-patterns` | SessionStart | Ensures plugin-patterns skill is applied every session |

---

## The 7 Phases

**Phase 1: Concept Discovery** — Understand what problem the plugin solves and for whom.

**Phase 2: Component Architecture** — Determine exactly what components are needed (skills, commands, agents, hooks, MCP) — no more, no less.

**Phase 3: Detailed Design** *(most important phase)* — Specify every component precisely. Resolve all ambiguities before writing a single file.

**Phase 4: Skill Design Sprint** — Design all SKILL.md files with progressive disclosure and strong trigger phrases before implementing anything else.

**Phase 5: Full Implementation** — Build all components following proven patterns. Requires explicit user approval before starting.

**Phase 6: Quality Review** — 3 parallel quality reviewers validate against production standards (design quality, enforcement strength, structural correctness).

**Phase 7: Documentation & Delivery** — Complete README, installation instructions, and first-test scenario.

---

## What You Get

After Phase 7, you'll have a plugin directory with:
- `plugin.json` — complete manifest
- `commands/` — phase-structured command files
- `agents/` — specialized agent system prompts
- `skills/[name]/SKILL.md` — lean skill body + references/
- `hooks/hooks.json` — session bootstrap configuration
- `README.md` — clear documentation with usage examples

Ready to install and use immediately.

---

## Quality Standards Applied

Plugin Forge applies the patterns from:
- **Anthropic's official plugin-dev** — Phase structure, skill progressive disclosure, parallel agents
- **obra/superpowers** — Enforcement language, Red Flags sections, session bootstrap hooks
- **Anthropic's feature-dev** — User gate checkpoints, clarifying question discipline

See `skills/plugin-patterns/SKILL.md` for the full quality checklist.
