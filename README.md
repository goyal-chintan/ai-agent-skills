# AI Agent Skills

A curated library of reusable skills for AI coding assistants. Works across **Codex**, **Claude Code**, and **Antigravity**.

Each skill teaches a discipline, methodology, or tool workflow that the agent doesn't enforce natively.

## Quick Start

```bash
git clone git@github.com:goyal-chintan/ai-agent-skills.git
cd ai-agent-skills
./install.sh --all          # symlink into all agents
./install.sh --dry-run      # preview without changes
```

## Skills (33)

### Portable (19) — Work on any agent

| Skill | Category | Purpose | Upstream |
|-------|----------|---------|----------|
| [brainstorm-general](skills/portable/brainstorm-general/SKILL.md) | Planning | 6-step decision framework for complex choices | — |
| [brainstorming](skills/portable/brainstorming/SKILL.md) | Planning | Design-before-code gate with collaborative exploration | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/brainstorming) |
| [writing-plans](skills/portable/writing-plans/SKILL.md) | Planning | Bite-sized implementation plans with verification | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/writing-plans) |
| [executing-plans](skills/portable/executing-plans/SKILL.md) | Workflow | Batch execution with review checkpoints | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/executing-plans) |
| [dispatching-parallel-agents](skills/portable/dispatching-parallel-agents/SKILL.md) | Workflow | Dispatch independent tasks to concurrent agents | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/dispatching-parallel-agents) |
| [subagent-driven-development](skills/portable/subagent-driven-development/SKILL.md) | Workflow | Orchestrate subagents for parallel implementation | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development) |
| [systematic-debugging](skills/portable/systematic-debugging/SKILL.md) | Debugging | 4-phase root-cause-first debugging methodology | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) |
| [test-driven-development](skills/portable/test-driven-development/SKILL.md) | Development | Red-Green-Refactor cycle enforcement | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) |
| [verification-before-completion](skills/portable/verification-before-completion/SKILL.md) | Quality | Evidence-based claims — run tests before declaring done | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) |
| [receiving-code-review](skills/portable/receiving-code-review/SKILL.md) | Review | Rigorous code review response protocol | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review) |
| [requesting-code-review](skills/portable/requesting-code-review/SKILL.md) | Review | Preparation and context for review requests | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/requesting-code-review) |
| [finishing-a-development-branch](skills/portable/finishing-a-development-branch/SKILL.md) | Git | Branch completion workflow (merge/PR/keep/discard) | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch) |
| [using-git-worktrees](skills/portable/using-git-worktrees/SKILL.md) | Git | Isolated parallel development environments | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/using-git-worktrees) |
| [using-superpowers](skills/portable/using-superpowers/SKILL.md) | Meta | Skill discovery and invocation discipline | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/using-superpowers) |
| [writing-skills](skills/portable/writing-skills/SKILL.md) | Meta | TDD applied to documentation — how to create new skills | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/writing-skills) |
| [claude-md-improver](skills/portable/claude-md-improver/SKILL.md) | Meta | Audit and improve CLAUDE.md project files | — |
| [skill-architect](skills/portable/skill-architect/SKILL.md) | Meta | Design and create reusable skills from patterns | — |
| [skill-selector-router](skills/portable/skill-selector-router/SKILL.md) | Meta | Select best-fit skills for a given prompt | — |
| [premium-frontend](skills/portable/premium-frontend/SKILL.md) | Design | World-class UI/UX — aesthetic direction, technical precision, anti-pattern protection | [Synthesized¹](#sources--upstream-references) |

### Tools (9) — Require external CLI tools

| Skill | Category | Requires | Upstream |
|-------|----------|----------|----------|
| [gh-address-comments](skills/tools/gh-address-comments/SKILL.md) | GitHub | `gh` CLI | — |
| [gh-fix-ci](skills/tools/gh-fix-ci/SKILL.md) | GitHub | `gh` CLI | — |
| [playwright](skills/tools/playwright/SKILL.md) | Browser | `npx`, Node.js | — |
| [screenshot](skills/tools/screenshot/SKILL.md) | Desktop | OS screenshot utils | — |
| [imagegen](skills/tools/imagegen/SKILL.md) | Image | `OPENAI_API_KEY` | — |
| [doc](skills/tools/doc/SKILL.md) | Document | `python-docx`, LibreOffice | — |
| [pdf](skills/tools/pdf/SKILL.md) | Document | `reportlab`, Poppler | — |
| [spreadsheet](skills/tools/spreadsheet/SKILL.md) | Document | `openpyxl`, `pandas` | — |
| [jupyter-notebook](skills/tools/jupyter-notebook/SKILL.md) | Notebook | `jupyterlab` | — |

### Integrations (5) — Require Jira/Confluence MCP

| Skill | Purpose | Upstream |
|-------|---------|----------|
| [capture-tasks-from-meeting-notes](skills/integrations/capture-tasks-from-meeting-notes/SKILL.md) | Extract action items → Jira tasks | — |
| [generate-status-report](skills/integrations/generate-status-report/SKILL.md) | Query Jira → Confluence status reports | — |
| [search-company-knowledge](skills/integrations/search-company-knowledge/SKILL.md) | Cross-system knowledge search | — |
| [spec-to-backlog](skills/integrations/spec-to-backlog/SKILL.md) | Confluence specs → Jira epics + tickets | — |
| [triage-issue](skills/integrations/triage-issue/SKILL.md) | Bug triage with duplicate detection | — |

## Install Script

```bash
./install.sh [OPTIONS]

Options:
  --codex           Install for Codex (~/.codex/skills/)
  --claude          Install for Claude Code (~/.claude/commands/)
  --antigravity     Install for Antigravity (~/.gemini/antigravity/skills/)
  --all             Install for all agents (default)
  --portable-only   Skip tools & integrations
  --dry-run         Preview without changes
  --uninstall       Remove all symlinks
```

## Skill Structure

```
skills/<category>/<skill-name>/
  SKILL.md              # Main reference (required)
  scripts/              # Helper scripts (optional)
  references/           # Additional docs (optional)
  agents/               # Sub-agent configs (optional)
```

Each `SKILL.md` has YAML frontmatter:
```yaml
---
name: skill-name
description: "Use when [triggering conditions]"
---
```

## Adding New Skills

Follow the [writing-skills](skills/portable/writing-skills/SKILL.md) methodology:
1. **RED**: Run a scenario without the skill, document what goes wrong
2. **GREEN**: Write the skill, verify compliance
3. **REFACTOR**: Find loopholes, add counters, retest

## Sources & Upstream References

Use the links below to check for updates and sync changes from official sources.

### `obra/superpowers` — 14 skills
**Repo:** https://github.com/obra/superpowers  
**Plugin:** `superpowers@claude-plugins-official` (currently v5.0.5)  
**Covers:** brainstorming, writing-plans, executing-plans, dispatching-parallel-agents, subagent-driven-development, systematic-debugging, test-driven-development, verification-before-completion, receiving-code-review, requesting-code-review, finishing-a-development-branch, using-git-worktrees, using-superpowers, writing-skills

To check for updates: compare local `SKILL.md` files against the installed plugin cache at  
`~/.claude/plugins/cache/claude-plugins-official/superpowers/<version>/skills/`

### Anthropic Official Skills — `frontend-design` plugin
**Repo:** https://github.com/anthropics/skills  
**Plugin:** `frontend-design@claude-plugins-official`  
**Covers:** The aesthetic direction layer of `premium-frontend`

Plugin cache: `~/.claude/plugins/cache/claude-plugins-official/frontend-design/<version>/skills/frontend-design/SKILL.md`

### `premium-frontend` — Synthesized (¹)
Built from five sources. Check each for updates:

| Layer | Source |
|---|---|
| Aesthetic direction | [anthropics/skills — frontend-design](https://github.com/anthropics/skills) |
| Technical precision (6 reference files) | [job-ops `frontend-design` reference](../job-ops/.agents/skills/frontend-design/reference/) |
| Anti-pattern rules | [cyxzdev/Uncodixfy](https://github.com/cyxzdev/Uncodixfy) |
| UX guidelines + style catalog | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| Grid + design system precision | [job-ops `design-principles`](../job-ops/.codex/skills/design-principles/SKILL.md) |

### Custom Skills — Original
The following skills have no upstream and were authored for this repo:  
`brainstorm-general`, `claude-md-improver`, `skill-architect`, `skill-selector-router`,  
all **Tools** skills, all **Integrations** skills.

## License

MIT
