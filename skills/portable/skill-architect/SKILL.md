---
name: skill-architect
description: Design, create, and update reusable Codex skills from task patterns using a template workflow and skill-creator tooling.
---

# Skill Architect

## Overview

Use this skill to create or update skills in a repeatable way when capabilities are missing or existing skills need better triggers/workflows.

## Plan-First Workflow

1. Capture concrete use cases (3-5 examples).
2. Define trigger and non-trigger sentence patterns.
3. Decide resources: `scripts`, `references`, `assets`.
4. Generate scaffold via `skill-creator` init script.
5. Fill `SKILL.md` with concise trigger conditions and workflow.
6. Validate frontmatter/shape using `quick_validate.py`.
7. Provide trigger examples and boundary examples.

## Wrapper Script

Use:

```bash
python3 "$CODEX_HOME/skills/skill-architect/scripts/skill_architect.py" \
  --name "<skill-name>" \
  --description "<when and why to use this skill>" \
  --resources scripts,references \
  --plan-only
```

Then apply creation:

```bash
python3 "$CODEX_HOME/skills/skill-architect/scripts/skill_architect.py" \
  --name "<skill-name>" \
  --description "<when and why to use this skill>" \
  --resources scripts,references \
  --apply
```

## Required Quality Gate

- Frontmatter has clear `name` and trigger-focused `description`.
- Workflow is deterministic where mistakes are costly.
- Non-trigger boundaries are explicit.
- `quick_validate.py` must pass.

## Template

Use the brief template at:
`$CODEX_HOME/skills/skill-architect/references/skill-brief-template.md`
