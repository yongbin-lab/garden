# Marketplace Structure Reference

## marketplace.json Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Marketplace identifier (kebab-case, no spaces) |
| `owner` | object | Maintainer info (name required, email optional) |
| `plugins` | array | List of available plugins |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `metadata.description` | string | Short marketplace description |
| `metadata.version` | string | Marketplace version |
| `metadata.pluginRoot` | string | Base directory for relative plugin sources |

### Plugin Entry Fields

**Required:**
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case) |
| `source` | string or object | Where to fetch the plugin |

**Optional:**
| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Plugin description |
| `version` | string | Plugin version |
| `author` | object | Plugin author (name, email) |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | SPDX license identifier |
| `keywords` | array | Search tags |
| `category` | string | Plugin category |
| `tags` | array | Additional tags |

## Plugin Source Types

### Relative path (for monorepo marketplaces)
```json
{ "name": "my-plugin", "source": "./my-plugin" }
```
Note: Only works when marketplace is added via Git, not via direct URL.

### GitHub repo
```json
{
  "name": "my-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v1.0.0"
  }
}
```

### Git URL
```json
{
  "name": "my-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

## Reserved Marketplace Names (cannot use)

- claude-code-marketplace
- claude-code-plugins
- claude-plugins-official
- anthropic-marketplace
- anthropic-plugins
- agent-skills
- life-sciences

## User Commands Reference

### For marketplace owners
```bash
# Validate marketplace
claude plugin validate .
# or inside Claude Code:
/plugin validate .
```

### For users installing plugins
```bash
# Add a marketplace
/plugin marketplace add <owner>/<repo>

# Install a plugin from marketplace
/plugin install <plugin-name>@<marketplace-name>

# Update marketplace catalog
/plugin marketplace update

# List installed plugins
/plugin list
```

## README Template

```markdown
# <Marketplace Name>

<Description>

## Plugins

### <Plugin Name>
<Plugin description>

## Installation

1. Add this marketplace:
   ```
   /plugin marketplace add <owner>/<repo>
   ```

2. Install the plugin:
   ```
   /plugin install <plugin-name>@<marketplace-name>
   ```

## Usage

<How to use each plugin — commands, skills, etc.>

## License

<License>
```
