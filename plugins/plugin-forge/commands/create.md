---
description: Guided 7-phase workflow for creating high-quality Claude Code plugins. Produces production-ready plugins with commands, agents, skills, and hooks following Anthropic's official patterns.
argument-hint: Optional plugin concept or description
allowed-tools: Read, Write, Bash, Glob, Grep, TodoWrite, Task, Skill, AskUserQuestion
---

# Plugin Forge: Create

Guide the user through building a high-quality Claude Code plugin. Follow these 7 phases exactly — each phase gates the next. Never skip phases or rush to implementation.

**Load the plugin-patterns skill now using the Skill tool before proceeding.**

Initial concept: $ARGUMENTS

---

## Phase 1: Concept Discovery
**Goal:** Understand what problem this plugin solves and for whom.

Create a TodoWrite with all 7 phases before doing anything else.

If `$ARGUMENTS` is provided:
- Summarize your understanding of the concept
- Identify plugin type: workflow automation / knowledge injection / quality gate / integration toolkit
- Ask at most 2 clarifying questions if critical gaps exist

If `$ARGUMENTS` is empty, ask the user:
- What repeated pain or task should this plugin eliminate?
- Who uses it and when do they reach for it?
- Any existing plugins they've seen that come close?

**Gate:** Summarize the plugin purpose in 2 sentences. Confirm with user before Phase 2.

---

## Phase 2: Component Architecture
**Goal:** Determine the exact set of components needed — no more, no less.

Load the plugin-patterns skill if not already loaded.

Launch the `needs-analyzer` agent with the confirmed plugin purpose. The agent will return a component plan.

Present the plan as a table:

| Component Type | Count | Purpose | Trigger / Usage |
|----------------|-------|---------|-----------------|
| Skills         | ?     | ...     | ...             |
| Commands       | ?     | ...     | ...             |
| Agents         | ?     | ...     | ...             |
| Hooks          | ?     | ...     | ...             |
| MCP            | ?     | ...     | ...             |

Decision rules:
- Skills: use when Claude needs specialized knowledge injected at the right moment
- Commands: use when users initiate a structured multi-step action
- Agents: use when a task benefits from a focused sub-agent with restricted tools
- Hooks: use when behavior should trigger automatically on Claude Code events
- MCP: use only when external service integration is needed

**Gate:** Get user confirmation or adjustments. Do not proceed until confirmed.

---

## Phase 3: Detailed Design & Clarifying Questions
**Goal:** Specify every component precisely. Resolve all ambiguities.

**CRITICAL: This is the most important phase. DO NOT SKIP.**

For each confirmed component, identify what's underspecified:

**For each Skill:**
- What exact phrases would a user say to trigger this? (list 4-6 concrete examples)
- What knowledge does it provide that Claude can't derive from context?
- What goes in SKILL.md vs references/ vs scripts/?

**For each Command:**
- What are the arguments? Required vs optional?
- Which tools does it need? (minimize this list)
- At what points does it wait for user input?
- What does success look like — what does the user see at the end?

**For each Agent:**
- Does it trigger proactively (after certain events) or only when called?
- What specialized focus does it have that a generalist Claude wouldn't have?
- What output format does it produce?

**For each Hook:**
- Which event: SessionStart / PreToolUse / PostToolUse / Stop?
- Prompt-based (JSON rules) or script-based (bash)?
- What behavior does it enforce or prevent?

Present all questions in organized sections. Wait for complete answers.

If user says "use your judgment" on any point, provide a concrete recommendation and get explicit confirmation.

**Gate:** Full specification confirmed for all components.

---

## Phase 4: Skill Design Sprint
**Goal:** Design SKILL.md files with progressive disclosure before writing any other code.

Skills are the hardest component to get right. Do them first.

For each skill in the plan, launch a `skill-architect` agent with:
- The skill's purpose
- The trigger phrases from Phase 3
- The knowledge it needs to convey
- Examples of what it enables

After agents complete, read all returned skill drafts. For each:
- Check: description uses third-person with specific trigger phrases?
- Check: body is 1,500–2,000 words in imperative form?
- Check: detailed content is in references/ not SKILL.md?
- Check: are there any rationalization loopholes that need closing?

Present skill designs to user. For skills enforcing discipline (like TDD or security patterns), add Red Flags sections that counter common workarounds.

**Gate:** User approves skill designs. Revise if needed.

---

## Phase 5: Full Implementation
**Goal:** Build all components following proven patterns.

**Wait for explicit user approval before starting.**

Read all relevant specifications from Phases 3 and 4.

Implementation order:
1. Plugin directory structure + `plugin.json`
2. Skill files (SKILL.md + references/ + scripts/)
3. Command files (with full phase workflow if complex)
4. Agent files (with clear whenToUse examples and system prompts)
5. Hook configuration (hooks.json + scripts if needed)
6. README.md

Use the `component-builder` agent for each major component type.

For commands that orchestrate complex workflows:
- Structure as explicit numbered phases
- Include `**Gate:**` checkpoints for user confirmation
- Reference skills using the Skill tool

For agents:
- Make `whenToUse` examples hyper-specific with 3+ concrete scenarios
- System prompts should define a specialized persona, not just list tasks
- Include output format requirements

For skills:
- Description MUST be third-person with specific trigger phrases
- Body MUST use imperative/infinitive form ("Load X. Run Y. Validate Z.")
- Include Red Flags section for any discipline-enforcing skill
- Reference all supporting files explicitly

Track all file creation with TodoWrite.

**Gate:** All components created. Present complete file tree.

---

## Phase 6: Quality Review
**Goal:** Validate against the high-bar standards of production plugins.

Launch 3 `quality-reviewer` agents in parallel with different focuses:

**Reviewer 1 — Design Quality**
- Are skill trigger phrases specific and third-person?
- Do commands have proper phase structure and user gates?
- Is progressive disclosure correctly applied?

**Reviewer 2 — Enforcement Strength**
- Do discipline-enforcing skills close rationalization loopholes?
- Are mandatory behaviors phrased as absolute rules, not suggestions?
- Are Red Flags sections comprehensive?

**Reviewer 3 — Structural Correctness**
- Is plugin.json valid and complete?
- Do all referenced files exist?
- Are hooks correctly configured?
- Does README clearly explain installation and usage?

Consolidate findings. Categorize as:
- 🔴 Critical: must fix before use
- 🟡 Warning: recommended fix
- 🟢 Good: meets standards

Present to user. For critical issues, fix immediately. For warnings, ask user preference.

**Gate:** No critical issues remain.

---

## Phase 7: Documentation & Delivery
**Goal:** Package the plugin for immediate use.

Verify README completeness:
- Overview: What problem does this solve?
- Installation: exact commands to install
- Usage: concrete examples for each command/agent/skill
- Components: table listing all components with descriptions

Show user how to test locally:
```bash
# Test with plugin-dir flag
claude --plugin-dir /path/to/your-plugin

# Or install to user scope
claude plugin install /path/to/your-plugin --scope user
```

Mark all todos complete.

Present final summary:
- Plugin name and purpose
- Components created (X skills, Y commands, Z agents, N hooks)
- File count and structure
- Recommended first test scenario

Ask: "Would you like me to help you test the plugin now, or is there a specific component you'd like to refine?"
