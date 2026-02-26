---
name: local-plugin-install
description: "This skill should be used when the user asks \"플러그인 설치해줘\", \"install this plugin\", \"로컬 마켓플레이스에 등록해줘\", \"플러그인 등록\", \"register plugin\", \"plugin install\", \"이 플러그인 쓸 수 있게 해줘\", or \"마켓플레이스에 추가해줘\". Provides the exact file structure, naming conventions, and CLI commands required to register and install a local Claude Code plugin."
---

# Skill: local-plugin-install

## Description (Layer 1)

This skill should be used when a user asks to install, register, or enable a locally-built Claude Code plugin. Activate when the user says "플러그인 설치해줘", "install this plugin", "로컬 마켓플레이스에 등록해줘", "플러그인 등록", "register plugin", "plugin install", "이 플러그인 쓸 수 있게 해줘", or "마켓플레이스에 추가해줘". The skill provides the exact file structure requirements, common format pitfalls, and the CLI commands to register a plugin in the local marketplace and install it.

---

## Body (Layer 2)

### Prerequisites

- Local marketplace already registered at `/Users/mlt359/Desktop/local-marketplace`
- Plugin source stored under `/Users/mlt359/garden/plugins/`

---

### Step 1 — Validate Plugin File Structure

Before attempting installation, verify the plugin directory matches this exact structure:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED — simplified meta (name, version, description only)
├── plugin.json              # Full manifest (commands, agents, skills)
├── commands/
│   └── my-command.md
├── agents/
│   └── my-agent.md          # MUST be .md with YAML frontmatter, NOT .json
├── skills/
│   └── my-skill/
│       └── SKILL.md
└── README.md
```

Run `claude plugin validate /path/to/my-plugin` to check structural correctness.

---

### Step 2 — Check for Common Format Errors

These are the exact pitfalls that will silently break plugin loading. Check every one before proceeding.

| Item | Correct | Wrong — will silently fail |
|------|---------|---------------------------|
| `.claude-plugin/plugin.json` | Must exist | Missing = plugin not recognized |
| Agent file extension | `.md` (YAML frontmatter) | `.json` |
| plugin.json component path key | `"file"` | `"path"` |
| Command frontmatter `allowed-tools` | Inline comma: `Read, Write, Bash` | YAML list: `- Read` |
| Skill path in plugin.json | `skills/my-skill/SKILL.md` | `skills/my-skill` (directory only) |

#### `.claude-plugin/plugin.json` format

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description"
}
```

#### plugin.json component references — use `"file"`, not `"path"`

```json
{
  "commands": [{ "name": "cmd", "description": "...", "file": "commands/cmd.md" }],
  "agents":  [{ "name": "agt", "description": "...", "file": "agents/agt.md" }],
  "skills":  [{ "name": "skl", "description": "...", "file": "skills/skl/SKILL.md" }]
}
```

#### Command frontmatter — inline comma format

```yaml
---
description: "Command description"
allowed-tools: Skill, Read, Write, Bash, AskUserQuestion
---
```

#### Agent file — `.md` with YAML frontmatter

```yaml
---
name: my-agent
description: "Agent description"
whenToUse:
  - "Specific scenario 1"
tools:
  - Bash
  - Read
---

System prompt content here...
```

---

### Step 3 — Place Source in garden/plugins

```bash
cp -r /path/to/my-plugin /Users/mlt359/garden/plugins/my-plugin
```

---

### Step 4 — Register in Local Marketplace

#### 4-1. Create symlink

```bash
ln -s /Users/mlt359/garden/plugins/my-plugin /Users/mlt359/Desktop/local-marketplace/plugins/my-plugin
```

#### 4-2. Add entry to marketplace.json

Edit `/Users/mlt359/Desktop/local-marketplace/.claude-plugin/marketplace.json` — append to `plugins` array:

```json
{
  "name": "my-plugin",
  "description": "Plugin description",
  "source": "./plugins/my-plugin",
  "category": "development"
}
```

---

### Step 5 — Update Marketplace & Install

```bash
claude plugin marketplace update local-plugins
claude plugin install my-plugin@local-plugins --scope user
```

This automatically handles:
- Copying files to `~/.claude/plugins/cache/local-plugins/my-plugin/1.0.0/`
- Adding entry to `~/.claude/plugins/installed_plugins.json`
- Adding `"my-plugin@local-plugins": true` to `~/.claude/settings.json` `enabledPlugins`

---

### Step 6 — Verify

Open a new session and test the plugin's slash commands.

---

### Updating After Source Changes

```bash
claude plugin update my-plugin@local-plugins
```

Or edit files directly in cache: `~/.claude/plugins/cache/local-plugins/my-plugin/1.0.0/`

---

### Red Flags — Do Not Do These

| Action | Why it fails |
|--------|-------------|
| Manually edit `installed_plugins.json` | `claude plugin install` handles this correctly |
| Manually edit `settings.json` `enabledPlugins` | `claude plugin install` handles this correctly |
| Copy files directly to `~/.claude/plugins/cache/` | Must go through marketplace registration |
| Create agent files as `.json` | Must be `.md` with YAML frontmatter |
| Use `"path"` key in plugin.json | Must be `"file"` |
| Use YAML list for `allowed-tools` in command frontmatter | Must be inline comma-separated |
| Skip `.claude-plugin/plugin.json` | Plugin will not be recognized at all |
