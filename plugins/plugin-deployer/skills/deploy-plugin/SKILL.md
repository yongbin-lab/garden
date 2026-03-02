---
name: deploy-plugin
description: Deploys a Claude Code plugin to a GitHub marketplace. Triggers when the user wants to deploy, publish, release, or share a plugin to a marketplace. Responds to phrases like "플러그인 배포해줘", "마켓플레이스에 올려줘", "플러그인 공유하고 싶어", "deploy this plugin", "publish to marketplace".
---

# Plugin Deployer Skill

You help users deploy Claude Code plugins to GitHub-hosted marketplaces so anyone can install them.

## When to Activate

Activate when the user wants to:
- Deploy/publish/release a plugin to a marketplace
- Share a plugin on GitHub so others can install it
- Upload a plugin to a marketplace
- "배포", "퍼블리시", "마켓플레이스에 올려", "공유" related to plugins

## Workflow

### Step 1: Identify the Plugin

Determine which plugin to deploy:
- If the user points to a specific path, use that
- If they just created a plugin in this session, offer to deploy that one
- If unclear, ask which plugin they want to deploy

Validate the plugin:
1. Check `.claude-plugin/plugin.json` exists with name, description, version
2. Check component directories are at plugin root (not inside .claude-plugin/)
3. Show a summary of what will be deployed

### Step 2: Find Existing Marketplace or Gather Config

**Always check for existing marketplaces first.** One marketplace repo holds all plugins.

#### 2-A: Scan for existing marketplaces

1. List directories under `~/.claude/plugins/marketplaces/`
2. Read `.claude-plugin/marketplace.json` from each
3. Get the GitHub remote URL via `git remote -v`

If found → show the marketplace info and ask "이 마켓플레이스에 추가할까요?"

#### 2-B: No existing marketplace — gather config

| Setting | Default | How to detect |
|---------|---------|---------------|
| GitHub username | Auto-detect via `gh api user --jq '.login'` | Fall back to asking |
| Repo name | `<username>-plugins` | Confirm with user |
| Marketplace name | `<username>-plugins` | Confirm with user |
| Visibility | public | Confirm with user |
| License | MIT | Confirm with user |

Present all defaults at once: "이대로 진행할까요?" — one confirmation, not five separate questions.

### Step 3: Deploy

#### 3-A: Add to existing marketplace (default path)

1. Work in the marketplace directory (`~/.claude/plugins/marketplaces/<name>/`)
2. Copy plugin into `plugins/<plugin-name>/`
3. Add entry to `marketplace.json` plugins array
4. Add plugin section to `README.md`
5. `git add -A && git commit && git push`

If a plugin with the same name already exists, compare versions and ask before overwriting.

#### 3-B: Create new marketplace

1. Create structure in `/tmp/<repo-name>/`:
```
<repo-name>/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── <plugin-name>/
└── README.md
```
2. `gh auth status` — check auth
3. `git init` + initial commit
4. `gh repo create <repo> --public --source=. --push`

### Step 4: Show Results

**Added to existing marketplace:**
```
✅ 배포 완료!

📦 마켓플레이스: https://github.com/<username>/<repo>
📌 추가된 플러그인: <plugin-name> v<version>

🔧 설치:
  /plugin install <plugin-name>@<marketplace-name>
```

**Created new marketplace:**
```
✅ 배포 완료!

📦 레포: https://github.com/<username>/<repo>

🔧 설치:
  /plugin marketplace add <username>/<repo>
  /plugin install <plugin-name>@<marketplace-name>

📝 다음 플러그인 배포 시 이 마켓플레이스에 자동으로 추가됩니다.
```

## Prerequisites Check

Before starting deployment, verify:
- `gh` CLI is installed → if not, guide: `brew install gh`
- `gh auth status` passes → if not, guide: `gh auth login`
- `git` is available and configured → if not, help set up `git config`

If any prerequisite fails, stop and help the user fix it before proceeding.

## Safety Rules

- NEVER force push
- NEVER overwrite existing plugins without asking
- Warn about sensitive files (.env, credentials, tokens)
- Always show what will be created/pushed before doing it
- One marketplace repo for all plugins — do NOT create a new repo per plugin
