# Obra Sync And Technical Writing Design

## Summary

Add a safe upstream sync workflow for Obra-derived skills and introduce a new portable `technical-writing` skill that improves document generation across Claude, Codex, OpenCode, and Copilot-compatible installations. The sync workflow must overwrite only an explicit allowlist of mapped Obra skills while preserving all custom local skills, including synthesized frontend skills and any repo-specific additions.

## Goals

- Add an automated script that clones `obra/superpowers` and updates only explicitly mapped local skills.
- Prevent accidental replacement of custom or synthesized skills.
- Add a portable `technical-writing` skill for clear general writing, technical documentation, concept explainers, and Confluence-ready pages.
- Improve repo metadata so install and discovery docs accurately cover OpenCode, Claude Code, Codex, and GitHub Copilot CLI.

## Non-Goals

- Do not add a full generated-vendor pipeline.
- Do not auto-sync synthesized skills such as `premium-frontend` or `apple-grade-ui-system`.
- Do not replace unmapped local skills, even if they resemble upstream content.

## Current Repo Observations

- `README.md` already documents upstream references for the Obra-backed workflow skills.
- `install.sh` already supports `--opencode`, but `README.md` does not yet document it in the install options or top-level platform list.
- There is no existing `docs/` directory or dedicated automated test harness.
- The repo mixes upstream-backed, synthesized, and original skills under `skills/portable/`.

## Approach

### 1. Explicit Obra Sync Manifest

Add a checked-in manifest that lists only the local skills that should be overwritten from `obra/superpowers`.

Each manifest entry should include:

- upstream skill name
- local destination path
- local category

This manifest is the only source of truth for overwrite behavior. If a local skill is not listed, the sync script must not modify it.

### 2. Sync Script Behavior

Add `scripts/sync_obra_skills.py` as the repo-maintained updater.

Expected behavior:

- clone `https://github.com/obra/superpowers.git` into a temporary directory
- read the manifest
- for each mapped skill:
  - verify the upstream source exists
  - replace the exact local destination directory contents with upstream contents
  - report added, changed, and removed files
- detect unmapped local skills and list them as preserved
- support `--dry-run`
- support a repo-relative execution model so it works the same from Claude, Codex, OpenCode, or shell usage

Safety rules:

- never scan `skills/portable/` heuristically for similar names
- never touch skills outside the manifest
- never touch synthesized or custom frontend skills unless they are deliberately added to the manifest later
- if the manifest points to a local path outside `skills/portable/`, fail hard

### 3. Technical Writing Skill

Add a new portable skill: `skills/portable/technical-writing/`.

Purpose:

- generate engaging and clear writing for normal and technical documents
- improve technical documentation
- improve concept explanations
- help draft Confluence pages and internal documentation

Structure:

- `SKILL.md`: when to use, workflow, doc-type selection, audience-first drafting, clarity rules, revision checklist
- `references/core-principles.md`: scannability, sentence design, examples, terminology control, structure
- `references/document-types.md`: concept docs, task docs, reference docs, status updates, proposals, ADR-lite, Confluence pages
- `references/source-guides.md`: curated external resources and when each is useful
- `references/templates.md`: short templates for docs, explainers, updates, and Confluence pages

External references to curate:

- Google Technical Writing
- Microsoft Writing Style Guide
- Write the Docs Guide
- plain-language guidance from Digital.gov / PlainLanguage.gov lineage

### 4. Cross-Platform Search And Discovery

The user asked to make sure skill discovery works well across Claude, Codex, and OpenCode.

Repo changes should therefore also improve discoverability:

- add the `technical-writing` skill to `README.md`
- update skill counts
- mention OpenCode anywhere the README lists supported agents
- keep `technical-writing` frontmatter and description optimized for search triggers across agent platforms
- ensure wording uses likely user queries such as `documentation`, `technical writing`, `Confluence page`, `explainer`, `concept doc`, and `clear writing`

### 5. Validation

Add lightweight tests for the sync script using Python `unittest`.

Tests should cover:

- manifest loading
- path safety validation
- mapped-only update planning
- preservation of unmapped local skills
- dry-run output planning

Repo-level verification after implementation should include:

- `python3 -m unittest discover -s tests -p 'test_*.py'`
- direct sync script dry run

## Risks And Mitigations

### Risk: accidental overwrite of custom skills

Mitigation:

- explicit manifest allowlist only
- hard path validation
- dry-run mode
- preservation report for unmapped local skills

### Risk: platform docs drift again

Mitigation:

- align `README.md` with `install.sh`
- document OpenCode support in the same sections that document Claude/Codex/Copilot

### Risk: writing skill becomes too vague or generic

Mitigation:

- make document-type choice a first-class step
- include concrete templates and reference guidance
- optimize description for actual trigger conditions, not process summary

## Implementation Outline

1. Add docs directory, design doc, and implementation plan.
2. Add failing tests for sync script behavior and path safety.
3. Implement sync manifest and sync script.
4. Add the `technical-writing` skill and curated references.
5. Update `README.md` and install docs for OpenCode and new skill discovery.
6. Run tests and a sync dry run.

## Success Criteria

- Running the sync script updates only explicitly mapped Obra-backed skills.
- Custom and synthesized skills remain untouched.
- `technical-writing` is installed like other portable skills and is discoverable across supported platforms.
- `README.md` accurately reflects supported agents, install options, skill counts, and the Obra sync workflow.
