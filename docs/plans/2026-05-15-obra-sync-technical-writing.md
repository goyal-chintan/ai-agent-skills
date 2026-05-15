# Obra Sync And Technical Writing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a safe Obra skill sync workflow, a new portable `technical-writing` skill, and cross-platform install/discovery updates for Claude, Codex, OpenCode, and Copilot-compatible installs.

**Architecture:** Use an explicit sync manifest and a Python sync script that clones `obra/superpowers`, updates only mapped local skills, and preserves all unmapped custom skills. Add a repo-native `technical-writing` skill with curated reference files, then align README/install documentation with actual platform support and search-friendly discovery.

**Tech Stack:** Bash, Python 3 standard library, Markdown

---

### Task 1: Build Sync Script Safety Net

**Files:**
- Create: `tests/test_sync_obra_skills.py`
- Create: `config/obra_skills.json`
- Create: `scripts/sync_obra_skills.py`

**Step 1: Write the failing test**

Create `tests/test_sync_obra_skills.py` covering:

- manifest loading returns mapped skill entries
- unsafe destination paths are rejected
- planning only includes manifest-mapped skills
- unmapped local skills are preserved

Expected design for tests:

```python
class ValidateManifestPathsTest(unittest.TestCase):
    def test_rejects_paths_outside_skills_portable(self):
        with self.assertRaises(ValueError):
            sync.validate_destination("../outside")
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_sync_obra_skills -v`
Expected: FAIL because `scripts/sync_obra_skills.py` does not exist yet

**Step 3: Write minimal implementation**

Create `config/obra_skills.json` with the explicit allowlist of Obra-backed skills documented in `README.md`.

Create `scripts/sync_obra_skills.py` with:

- manifest loading
- destination path validation
- upstream source path resolution
- update planning functions that operate on explicit manifest entries
- dry-run reporting support

Keep side-effect-free planning logic separate from the clone/copy execution path so tests can exercise it without network access.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_sync_obra_skills -v`
Expected: PASS

**Step 5: Commit**

Do not commit unless explicitly requested by the user.

### Task 2: Add Obra Clone And Sync Execution

**Files:**
- Modify: `scripts/sync_obra_skills.py`
- Test: `tests/test_sync_obra_skills.py`

**Step 1: Write the failing test**

Add tests for copy/update planning behavior, such as:

- mapped directory replacement collects file operations
- dry-run mode reports preserved custom skills

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_sync_obra_skills -v`
Expected: FAIL because execution/report helpers are incomplete

**Step 3: Write minimal implementation**

Add:

- temp clone support using `git clone --depth 1`
- manifest-driven sync execution
- summary output for updated and preserved skills
- `--dry-run` CLI option

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_sync_obra_skills -v`
Expected: PASS

**Step 5: Commit**

Do not commit unless explicitly requested by the user.

### Task 3: Add Technical Writing Skill

**Files:**
- Create: `skills/portable/technical-writing/SKILL.md`
- Create: `skills/portable/technical-writing/references/core-principles.md`
- Create: `skills/portable/technical-writing/references/document-types.md`
- Create: `skills/portable/technical-writing/references/source-guides.md`
- Create: `skills/portable/technical-writing/references/templates.md`

**Step 1: Write the failing test**

Add a lightweight test in `tests/test_sync_obra_skills.py` or a new `tests/test_skill_metadata.py` that verifies:

- `technical-writing/SKILL.md` exists
- frontmatter includes `name` and `description`
- description includes discovery terms for documentation and technical writing

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s tests -p 'test_*.py'`
Expected: FAIL because the skill does not exist yet

**Step 3: Write minimal implementation**

Create the new skill and references with:

- a search-friendly `description`
- a doc-type-first writing workflow
- audience and purpose framing
- sections for Confluence pages, concept docs, and technical explainers
- curated external references

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s tests -p 'test_*.py'`
Expected: PASS

**Step 5: Commit**

Do not commit unless explicitly requested by the user.

### Task 4: Align README And Platform Discovery Docs

**Files:**
- Modify: `README.md`
- Modify: `install.sh` if README and script behavior differ

**Step 1: Write the failing test**

Add a metadata test that asserts:

- README mentions OpenCode in supported platforms
- README install options include `--opencode`
- README includes `technical-writing`

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s tests -p 'test_*.py'`
Expected: FAIL because README does not yet contain the new content

**Step 3: Write minimal implementation**

Update `README.md` to:

- add OpenCode to the top-level platform list and install options
- add `technical-writing` to the portable skills table
- update skill counts
- document `scripts/sync_obra_skills.py`
- explain that only explicit Obra mappings are overwritten and custom local skills are preserved

Only modify `install.sh` if its current behavior and help text need alignment with README.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s tests -p 'test_*.py'`
Expected: PASS

**Step 5: Commit**

Do not commit unless explicitly requested by the user.

### Task 5: Verify End-To-End Behavior

**Files:**
- Modify: files above as needed from review feedback

**Step 1: Run unit tests**

Run: `python3 -m unittest discover -s tests -p 'test_*.py'`
Expected: PASS

**Step 2: Run sync dry run**

Run: `python3 scripts/sync_obra_skills.py --dry-run`
Expected: summary of mapped skills to update plus preserved unmapped skills, with no destructive changes

**Step 3: Review outputs**

Confirm:

- no unmapped skills are scheduled for overwrite
- `technical-writing` is not treated as upstream-managed
- OpenCode documentation is present in README

**Step 4: Commit**

Do not commit unless explicitly requested by the user.
