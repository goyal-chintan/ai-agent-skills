---
name: skill-selector-router
description: Select the best-fit Codex skills for a prompt, detect missing capabilities, and produce a plan-first local-to-curated-to-create path before any install/create action.
---

# Skill Selector Router

## Overview

Use this skill when the user asks which skill(s) should be used, when multiple skills could apply, or when a required skill may be missing.

Default behavior is plan-first: recommend the path first, do not install/create automatically.

## Workflow

1. Collect the user prompt and optional context.
2. Run selector analysis:
```bash
python3 "$CODEX_HOME/skills/skill-selector-router/scripts/select_skills.py" \
  --prompt "<user prompt>" \
  --context "<optional extra context>"
```
3. Use selected local skills first.
4. If capability is missing, follow this order:
   1. Local installed skills (re-check exact name).
   2. Curated install via `skill-installer`.
   3. Create skill with `skill-architect`.
5. Before mutating actions (install/create), present the proposed action to the user first.

## Curated Install Fallback

If curated listing/install fails due SSL certificate verification, fallback to git method:

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo openai/skills \
  --path "skills/.curated/<skill-name>" \
  --method git
```

## Notes

- Explicit `$skill-name` mentions get highest priority.
- This skill is a router/orchestrator; it should not replace domain skills.
