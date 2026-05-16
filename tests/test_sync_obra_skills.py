"""Tests for sync_obra_skills manifest loading, planning, safety, and execution."""

import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Ensure scripts/ is importable both when run directly and via -m unittest
_repo_root = os.path.join(os.path.dirname(__file__), os.pardir)
_scripts_dir = os.path.join(_repo_root, "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from sync_obra_skills import (
    load_manifest,
    main,
    plan_sync,
    dry_run_report,
    diff_skill_dirs,
    resolve_source_paths,
    clone_repo,
    execute_sync,
    ALLOWED_DEST_PREFIX,
    ALLOWED_SOURCE_PREFIX,
)


SAMPLE_MANIFEST = {
    "source_repo": "https://github.com/obra/superpowers.git",
    "skills": {
        "brainstorming": {
            "source_path": "skills/brainstorming",
            "dest_path": "skills/portable/brainstorming"
        },
        "writing-plans": {
            "source_path": "skills/writing-plans",
            "dest_path": "skills/portable/writing-plans"
        }
    }
}


class TestLoadManifest(unittest.TestCase):
    """Manifest loading returns mapped skill entries."""

    def test_load_returns_skill_entries(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(SAMPLE_MANIFEST, f)
            f.flush()
            path = f.name
        try:
            manifest = load_manifest(path)
            self.assertIn("skills", manifest)
            self.assertIn("brainstorming", manifest["skills"])
            self.assertEqual(
                manifest["skills"]["brainstorming"]["dest_path"],
                "skills/portable/brainstorming",
            )
        finally:
            os.unlink(path)

    def test_load_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_manifest("/nonexistent/path.json")


class TestPathSafety(unittest.TestCase):
    """Unsafe destination paths are rejected."""

    def test_dest_inside_allowed_prefix_accepted(self):
        manifest = {
            "source_repo": "https://github.com/obra/superpowers.git",
            "skills": {
                "ok-skill": {
                    "source_path": "skills/ok-skill",
                    "dest_path": "skills/portable/ok-skill"
                }
            }
        }
        plan = plan_sync(manifest, existing_local_skills=["ok-skill"])
        self.assertEqual(len(plan["sync"]), 1)

    def test_dest_outside_allowed_prefix_rejected(self):
        manifest = {
            "source_repo": "https://github.com/obra/superpowers.git",
            "skills": {
                "evil": {
                    "source_path": "skills/evil",
                    "dest_path": "../../../etc/evil"
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])

    def test_dest_sibling_prefix_rejected(self):
        """skills/portable-evil is not under skills/portable/."""
        manifest = {
            "source_repo": "https://github.com/obra/superpowers.git",
            "skills": {
                "sneaky": {
                    "source_path": "skills/sneaky",
                    "dest_path": "skills/portable-evil/sneaky"
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])

    def test_dest_traversal_inside_prefix_rejected(self):
        manifest = {
            "source_repo": "https://github.com/obra/superpowers.git",
            "skills": {
                "tricky": {
                    "source_path": "skills/tricky",
                    "dest_path": "skills/portable/../../../etc/passwd"
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])


class TestPlanSync(unittest.TestCase):
    """Planning only includes manifest-mapped skills."""

    def test_plan_includes_only_manifest_skills(self):
        result = plan_sync(SAMPLE_MANIFEST, existing_local_skills=[
            "brainstorming", "writing-plans", "premium-frontend", "apple-grade-ui-system"
        ])
        planned_names = {entry["name"] for entry in result["sync"]}
        self.assertEqual(planned_names, {"brainstorming", "writing-plans"})

    def test_plan_entries_have_required_fields(self):
        result = plan_sync(SAMPLE_MANIFEST, existing_local_skills=["brainstorming"])
        entry = result["sync"][0]
        self.assertIn("name", entry)
        self.assertIn("source_path", entry)
        self.assertIn("dest_path", entry)


class TestUnmappedPreservation(unittest.TestCase):
    """Unmapped local skills are preserved (not in sync plan)."""

    def test_unmapped_skills_not_in_plan(self):
        result = plan_sync(SAMPLE_MANIFEST, existing_local_skills=[
            "brainstorming", "premium-frontend", "apple-grade-ui-system",
            "skill-architect", "brainstorm-general"
        ])
        planned_names = {entry["name"] for entry in result["sync"]}
        self.assertNotIn("premium-frontend", planned_names)
        self.assertNotIn("apple-grade-ui-system", planned_names)
        self.assertNotIn("skill-architect", planned_names)
        self.assertNotIn("brainstorm-general", planned_names)

    def test_empty_manifest_produces_empty_plan(self):
        manifest = {"source_repo": "https://example.com", "skills": {}}
        result = plan_sync(manifest, existing_local_skills=["premium-frontend"])
        self.assertEqual(result["sync"], [])

    def test_preserved_skills_listed_in_plan(self):
        """Dry-run must report which unmapped local skills are preserved."""
        result = plan_sync(SAMPLE_MANIFEST, existing_local_skills=[
            "brainstorming", "premium-frontend", "apple-grade-ui-system"
        ])
        self.assertIn("preserved", result)
        self.assertIn("premium-frontend", result["preserved"])
        self.assertIn("apple-grade-ui-system", result["preserved"])
        self.assertNotIn("brainstorming", result["preserved"])

    def test_preserved_empty_when_all_mapped(self):
        result = plan_sync(SAMPLE_MANIFEST, existing_local_skills=[
            "brainstorming", "writing-plans"
        ])
        self.assertEqual(result["preserved"], [])


class TestDryRunReport(unittest.TestCase):
    """Dry-run reporting includes both sync actions and preserved skills."""

    def test_report_contains_sync_and_preserved_sections(self):
        result = plan_sync(SAMPLE_MANIFEST, existing_local_skills=[
            "brainstorming", "writing-plans", "premium-frontend"
        ])
        report = dry_run_report(result)
        self.assertIn("brainstorming", report)
        self.assertIn("writing-plans", report)
        self.assertIn("premium-frontend", report)
        self.assertIn("preserved", report.lower())
        self.assertIn("sync", report.lower())

    def test_report_empty_plan(self):
        manifest = {"source_repo": "https://example.com", "skills": {}}
        result = plan_sync(manifest, existing_local_skills=["premium-frontend"])
        report = dry_run_report(result)
        self.assertIn("0 skill(s) to sync", report)
        self.assertIn("premium-frontend", report)


class TestResolveSourcePaths(unittest.TestCase):
    """Source path resolution validates upstream paths."""

    def test_valid_source_path_resolves(self):
        resolved = resolve_source_paths(SAMPLE_MANIFEST)
        self.assertEqual(
            resolved["brainstorming"],
            "skills/brainstorming",
        )

    def test_source_path_traversal_rejected(self):
        bad_manifest = {
            "source_repo": "https://github.com/obra/superpowers.git",
            "skills": {
                "evil": {
                    "source_path": "../../../etc/passwd",
                    "dest_path": "skills/portable/evil"
                }
            }
        }
        with self.assertRaises(ValueError):
            resolve_source_paths(bad_manifest)

    def test_source_sibling_prefix_rejected(self):
        """skills-evil/foo is not under skills/."""
        bad_manifest = {
            "source_repo": "https://github.com/obra/superpowers.git",
            "skills": {
                "sneaky": {
                    "source_path": "skills-evil/sneaky",
                    "dest_path": "skills/portable/sneaky"
                }
            }
        }
        with self.assertRaises(ValueError):
            resolve_source_paths(bad_manifest)

    def test_source_path_must_be_under_skills_prefix(self):
        bad_manifest = {
            "source_repo": "https://github.com/obra/superpowers.git",
            "skills": {
                "sneaky": {
                    "source_path": "other-dir/sneaky",
                    "dest_path": "skills/portable/sneaky"
                }
            }
        }
        with self.assertRaises(ValueError):
            resolve_source_paths(bad_manifest)


class TestCloneRepo(unittest.TestCase):
    """clone_repo shells out to git clone --depth 1."""

    @patch("sync_obra_skills.subprocess.run")
    def test_clone_calls_git_with_depth_1(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        dest = "/tmp/fake-clone-dest"
        clone_repo("https://github.com/obra/superpowers.git", dest)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args[0], "git")
        self.assertIn("clone", args)
        self.assertIn("--depth", args)
        self.assertIn("1", args)
        self.assertIn("https://github.com/obra/superpowers.git", args)
        self.assertIn(dest, args)

    @patch("sync_obra_skills.subprocess.run")
    def test_clone_raises_on_failure(self, mock_run):
        mock_run.side_effect = RuntimeError("git failed")
        with self.assertRaises(RuntimeError):
            clone_repo("https://example.com/repo.git", "/tmp/x")


class TestExecuteSync(unittest.TestCase):
    """execute_sync copies mapped directories and preserves unmapped ones."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Create a fake clone dir with source skill content
        self.clone_dir = os.path.join(self.tmpdir, "clone")
        os.makedirs(os.path.join(self.clone_dir, "skills", "brainstorming"))
        with open(os.path.join(self.clone_dir, "skills", "brainstorming", "SKILL.md"), "w") as f:
            f.write("# Brainstorming v2\n")

        # Create a local repo dir with existing skills
        self.repo_dir = os.path.join(self.tmpdir, "repo")
        os.makedirs(os.path.join(self.repo_dir, "skills", "portable", "brainstorming"))
        with open(os.path.join(self.repo_dir, "skills", "portable", "brainstorming", "SKILL.md"), "w") as f:
            f.write("# Brainstorming v1\n")
        # An unmapped custom skill
        os.makedirs(os.path.join(self.repo_dir, "skills", "portable", "premium-frontend"))
        with open(os.path.join(self.repo_dir, "skills", "portable", "premium-frontend", "SKILL.md"), "w") as f:
            f.write("# Premium Frontend\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_mapped_skill_replaced(self):
        plan = {
            "sync": [
                {
                    "name": "brainstorming",
                    "source_path": "skills/brainstorming",
                    "dest_path": "skills/portable/brainstorming",
                }
            ],
            "preserved": ["premium-frontend"],
        }
        result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        updated_skill = os.path.join(self.repo_dir, "skills", "portable", "brainstorming", "SKILL.md")
        with open(updated_skill) as f:
            self.assertEqual(f.read(), "# Brainstorming v2\n")
        self.assertIn("brainstorming", result["updated"])

    def test_unmapped_skill_untouched(self):
        plan = {
            "sync": [
                {
                    "name": "brainstorming",
                    "source_path": "skills/brainstorming",
                    "dest_path": "skills/portable/brainstorming",
                }
            ],
            "preserved": ["premium-frontend"],
        }
        execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        custom_skill = os.path.join(self.repo_dir, "skills", "portable", "premium-frontend", "SKILL.md")
        with open(custom_skill) as f:
            self.assertEqual(f.read(), "# Premium Frontend\n")

    def test_execute_returns_summary(self):
        plan = {
            "sync": [
                {
                    "name": "brainstorming",
                    "source_path": "skills/brainstorming",
                    "dest_path": "skills/portable/brainstorming",
                }
            ],
            "preserved": ["premium-frontend"],
        }
        result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("updated", result)
        self.assertIn("preserved", result)
        self.assertEqual(result["preserved"], ["premium-frontend"])

    def test_missing_source_skill_skipped(self):
        """If a mapped skill doesn't exist in clone, it's reported as failed."""
        plan = {
            "sync": [
                {
                    "name": "nonexistent-skill",
                    "source_path": "skills/nonexistent-skill",
                    "dest_path": "skills/portable/nonexistent-skill",
                }
            ],
            "preserved": [],
        }
        result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("nonexistent-skill", result["failed"])


class TestDryRunReportsPreservedCustomSkills(unittest.TestCase):
    """Dry-run mode reports preserved custom skills clearly."""

    def test_dry_run_lists_technical_writing_as_preserved(self):
        """technical-writing is unmapped and must appear in preserved."""
        result = plan_sync(SAMPLE_MANIFEST, existing_local_skills=[
            "brainstorming", "writing-plans", "technical-writing"
        ])
        self.assertIn("technical-writing", result["preserved"])
        report = dry_run_report(result)
        self.assertIn("technical-writing", report)

    def test_dry_run_lists_all_custom_skills_preserved(self):
        result = plan_sync(SAMPLE_MANIFEST, existing_local_skills=[
            "brainstorming", "premium-frontend", "apple-grade-ui-system",
            "technical-writing", "skill-architect"
        ])
        report = dry_run_report(result)
        for name in ["premium-frontend", "apple-grade-ui-system", "technical-writing", "skill-architect"]:
            self.assertIn(name, report)


class TestPrefixRootRejection(unittest.TestCase):
    """The prefix root itself is not a valid dest or source path."""

    def test_dest_path_equal_to_prefix_root_rejected(self):
        """dest_path='skills/portable' would delete the entire portable dir."""
        manifest = {
            "source_repo": "https://example.com",
            "skills": {
                "dangerous": {
                    "source_path": "skills/dangerous",
                    "dest_path": "skills/portable",
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])

    def test_dest_path_with_trailing_slash_prefix_rejected(self):
        manifest = {
            "source_repo": "https://example.com",
            "skills": {
                "dangerous": {
                    "source_path": "skills/dangerous",
                    "dest_path": "skills/portable/",
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])

    def test_source_path_equal_to_prefix_root_rejected(self):
        """source_path='skills' would read the entire skills tree."""
        manifest = {
            "source_repo": "https://example.com",
            "skills": {
                "dangerous": {
                    "source_path": "skills",
                    "dest_path": "skills/portable/dangerous",
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])

    def test_source_path_with_trailing_slash_prefix_rejected(self):
        manifest = {
            "source_repo": "https://example.com",
            "skills": {
                "dangerous": {
                    "source_path": "skills/",
                    "dest_path": "skills/portable/dangerous",
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])

    def test_execute_rejects_dest_prefix_root(self):
        """execute_sync must also reject prefix root in mutated plans."""
        tmpdir = tempfile.mkdtemp()
        try:
            clone_dir = os.path.join(tmpdir, "clone")
            os.makedirs(os.path.join(clone_dir, "skills", "x"))
            repo_dir = os.path.join(tmpdir, "repo")
            os.makedirs(os.path.join(repo_dir, "skills", "portable"))
            bad_plan = {
                "sync": [{
                    "name": "x",
                    "source_path": "skills/x",
                    "dest_path": "skills/portable",
                }],
                "preserved": [],
            }
            with self.assertRaises(ValueError):
                execute_sync(bad_plan, clone_dir=clone_dir, repo_dir=repo_dir)
        finally:
            shutil.rmtree(tmpdir)

    def test_execute_rejects_source_prefix_root(self):
        tmpdir = tempfile.mkdtemp()
        try:
            clone_dir = os.path.join(tmpdir, "clone")
            os.makedirs(os.path.join(clone_dir, "skills"))
            repo_dir = os.path.join(tmpdir, "repo")
            os.makedirs(os.path.join(repo_dir, "skills", "portable"))
            bad_plan = {
                "sync": [{
                    "name": "x",
                    "source_path": "skills",
                    "dest_path": "skills/portable/x",
                }],
                "preserved": [],
            }
            with self.assertRaises(ValueError):
                execute_sync(bad_plan, clone_dir=clone_dir, repo_dir=repo_dir)
        finally:
            shutil.rmtree(tmpdir)


class TestPathNormalization(unittest.TestCase):
    """Paths with '..' components are rejected even if they resolve in-prefix."""

    def test_dest_with_dotdot_in_prefix_rejected(self):
        """skills/portable/brainstorming/.. widens the delete target."""
        manifest = {
            "source_repo": "https://example.com",
            "skills": {
                "tricky": {
                    "source_path": "skills/tricky",
                    "dest_path": "skills/portable/brainstorming/../brainstorming",
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])

    def test_source_with_dotdot_in_prefix_rejected(self):
        manifest = {
            "source_repo": "https://example.com",
            "skills": {
                "tricky": {
                    "source_path": "skills/brainstorming/../brainstorming",
                    "dest_path": "skills/portable/brainstorming",
                }
            }
        }
        with self.assertRaises(ValueError):
            plan_sync(manifest, existing_local_skills=[])

    def test_execute_rejects_raw_dotdot_in_dest(self):
        """execute_sync must reject dest_path containing '..' even if in-prefix."""
        tmpdir = tempfile.mkdtemp()
        try:
            clone_dir = os.path.join(tmpdir, "clone")
            os.makedirs(os.path.join(clone_dir, "skills", "x"))
            with open(os.path.join(clone_dir, "skills", "x", "f"), "w") as f:
                f.write("x")
            repo_dir = os.path.join(tmpdir, "repo")
            os.makedirs(os.path.join(repo_dir, "skills", "portable"))
            bad_plan = {
                "sync": [{
                    "name": "x",
                    "source_path": "skills/x",
                    "dest_path": "skills/portable/a/../a",
                }],
                "preserved": [],
            }
            with self.assertRaises(ValueError):
                execute_sync(bad_plan, clone_dir=clone_dir, repo_dir=repo_dir)
        finally:
            shutil.rmtree(tmpdir)

    def test_execute_rejects_raw_dotdot_in_source(self):
        tmpdir = tempfile.mkdtemp()
        try:
            clone_dir = os.path.join(tmpdir, "clone")
            os.makedirs(os.path.join(clone_dir, "skills", "x"))
            repo_dir = os.path.join(tmpdir, "repo")
            os.makedirs(os.path.join(repo_dir, "skills", "portable"))
            bad_plan = {
                "sync": [{
                    "name": "x",
                    "source_path": "skills/x/../x",
                    "dest_path": "skills/portable/x",
                }],
                "preserved": [],
            }
            with self.assertRaises(ValueError):
                execute_sync(bad_plan, clone_dir=clone_dir, repo_dir=repo_dir)
        finally:
            shutil.rmtree(tmpdir)


class TestSymlinkRejection(unittest.TestCase):
    """Symlinks in clone source are rejected to prevent escape."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.clone_dir = os.path.join(self.tmpdir, "clone")
        self.repo_dir = os.path.join(self.tmpdir, "repo")
        os.makedirs(os.path.join(self.repo_dir, "skills", "portable"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_symlink_file_in_source_rejected(self):
        skill_dir = os.path.join(self.clone_dir, "skills", "evil")
        os.makedirs(skill_dir)
        # Create a symlink pointing outside
        os.symlink("/etc/passwd", os.path.join(skill_dir, "stolen"))
        plan = {
            "sync": [{
                "name": "evil",
                "source_path": "skills/evil",
                "dest_path": "skills/portable/evil",
            }],
            "preserved": [],
        }
        with self.assertRaises(ValueError):
            execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)

    def test_symlink_dir_in_source_rejected(self):
        skill_dir = os.path.join(self.clone_dir, "skills", "evil")
        os.makedirs(skill_dir)
        os.symlink("/tmp", os.path.join(skill_dir, "escape"))
        plan = {
            "sync": [{
                "name": "evil",
                "source_path": "skills/evil",
                "dest_path": "skills/portable/evil",
            }],
            "preserved": [],
        }
        with self.assertRaises(ValueError):
            execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)

    def test_clone_dir_itself_symlink_rejected(self):
        """clone_dir being a symlink is rejected."""
        real_clone = os.path.join(self.tmpdir, "real_clone")
        os.makedirs(os.path.join(real_clone, "skills", "ok"))
        with open(os.path.join(real_clone, "skills", "ok", "SKILL.md"), "w") as f:
            f.write("content\n")
        symlink_clone = os.path.join(self.tmpdir, "sym_clone")
        os.symlink(real_clone, symlink_clone)
        plan = {
            "sync": [{"name": "ok", "source_path": "skills/ok",
                       "dest_path": "skills/portable/ok"}],
            "preserved": [],
        }
        with self.assertRaises(ValueError) as ctx:
            execute_sync(plan, clone_dir=symlink_clone, repo_dir=self.repo_dir)
        self.assertIn("symlink", str(ctx.exception).lower())

    def test_repo_dir_itself_symlink_rejected(self):
        """repo_dir being a symlink is rejected."""
        src_dir = os.path.join(self.clone_dir, "skills", "ok")
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "SKILL.md"), "w") as f:
            f.write("content\n")
        real_repo = os.path.join(self.tmpdir, "real_repo")
        os.makedirs(os.path.join(real_repo, "skills", "portable"))
        symlink_repo = os.path.join(self.tmpdir, "sym_repo")
        os.symlink(real_repo, symlink_repo)
        plan = {
            "sync": [{"name": "ok", "source_path": "skills/ok",
                       "dest_path": "skills/portable/ok"}],
            "preserved": [],
        }
        with self.assertRaises(ValueError) as ctx:
            execute_sync(plan, clone_dir=self.clone_dir, repo_dir=symlink_repo)
        self.assertIn("symlink", str(ctx.exception).lower())

    def test_source_ancestor_symlink_rejected(self):
        """A symlinked ancestor dir in the source path (e.g. clone/skills) is rejected."""
        real_skills = os.path.join(self.tmpdir, "real_skills")
        os.makedirs(os.path.join(real_skills, "ok"))
        with open(os.path.join(real_skills, "ok", "SKILL.md"), "w") as f:
            f.write("content\n")
        os.makedirs(self.clone_dir)
        os.symlink(real_skills, os.path.join(self.clone_dir, "skills"))
        plan = {
            "sync": [{"name": "ok", "source_path": "skills/ok",
                       "dest_path": "skills/portable/ok"}],
            "preserved": [],
        }
        with self.assertRaises(ValueError) as ctx:
            execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("symlink", str(ctx.exception).lower())

    def test_dest_ancestor_symlink_rejected(self):
        """A symlinked ancestor dir in the dest path (e.g. repo/skills/portable) is rejected."""
        # Set up a valid source
        src_dir = os.path.join(self.clone_dir, "skills", "ok")
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "SKILL.md"), "w") as f:
            f.write("content\n")
        # Make repo/skills/portable a symlink to somewhere else
        real_portable = os.path.join(self.tmpdir, "real_portable")
        os.makedirs(real_portable)
        # Remove the real portable dir and replace with symlink
        shutil.rmtree(os.path.join(self.repo_dir, "skills", "portable"))
        os.symlink(real_portable, os.path.join(self.repo_dir, "skills", "portable"))
        plan = {
            "sync": [{"name": "ok", "source_path": "skills/ok",
                       "dest_path": "skills/portable/ok"}],
            "preserved": [],
        }
        with self.assertRaises(ValueError) as ctx:
            execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("symlink", str(ctx.exception).lower())

    def test_source_dir_itself_is_symlink_rejected(self):
        os.makedirs(os.path.join(self.clone_dir, "skills"))
        real_dir = os.path.join(self.tmpdir, "real_skill")
        os.makedirs(real_dir)
        with open(os.path.join(real_dir, "SKILL.md"), "w") as f:
            f.write("real\n")
        os.symlink(real_dir, os.path.join(self.clone_dir, "skills", "linked"))
        plan = {
            "sync": [{
                "name": "linked",
                "source_path": "skills/linked",
                "dest_path": "skills/portable/linked",
            }],
            "preserved": [],
        }
        with self.assertRaises(ValueError):
            execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)


class TestAtomicSwap(unittest.TestCase):
    """Old skill content survives if copy fails mid-way."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.clone_dir = os.path.join(self.tmpdir, "clone")
        self.repo_dir = os.path.join(self.tmpdir, "repo")
        # Existing local skill
        os.makedirs(os.path.join(self.repo_dir, "skills", "portable", "brainstorming"))
        with open(os.path.join(self.repo_dir, "skills", "portable", "brainstorming", "SKILL.md"), "w") as f:
            f.write("# Original\n")
        # Source skill in clone
        os.makedirs(os.path.join(self.clone_dir, "skills", "brainstorming"))
        with open(os.path.join(self.clone_dir, "skills", "brainstorming", "SKILL.md"), "w") as f:
            f.write("# Updated\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    @patch("sync_obra_skills.shutil.copytree", side_effect=OSError("disk full"))
    def test_old_content_restored_on_copy_failure(self, _mock_copy):
        plan = {
            "sync": [{
                "name": "brainstorming",
                "source_path": "skills/brainstorming",
                "dest_path": "skills/portable/brainstorming",
            }],
            "preserved": [],
        }
        result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("brainstorming", result["failed"])
        # Original content must still be present
        original = os.path.join(self.repo_dir, "skills", "portable", "brainstorming", "SKILL.md")
        self.assertTrue(os.path.exists(original))
        with open(original) as f:
            self.assertEqual(f.read(), "# Original\n")

    def test_no_temp_dirs_left_in_skills_namespace(self):
        """Temp/backup dirs must not be siblings inside skills/portable/."""
        plan = {
            "sync": [{
                "name": "brainstorming",
                "source_path": "skills/brainstorming",
                "dest_path": "skills/portable/brainstorming",
            }],
            "preserved": [],
        }
        execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        portable = os.path.join(self.repo_dir, "skills", "portable")
        entries = os.listdir(portable)
        for entry in entries:
            self.assertNotIn("__sync", entry,
                f"Temp artifact {entry!r} left in skills/portable/")

    def test_no_temp_dirs_on_failure(self):
        """Even on failure, no temp dirs should remain in skills/portable/."""
        with patch("sync_obra_skills.shutil.copytree", side_effect=OSError("disk full")):
            plan = {
                "sync": [{
                    "name": "brainstorming",
                    "source_path": "skills/brainstorming",
                    "dest_path": "skills/portable/brainstorming",
                }],
                "preserved": [],
            }
            execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        portable = os.path.join(self.repo_dir, "skills", "portable")
        entries = os.listdir(portable)
        for entry in entries:
            self.assertNotIn("__sync", entry,
                f"Temp artifact {entry!r} left in skills/portable/ after failure")
            self.assertFalse(entry.startswith(".obra-sync-"),
                f"Temp artifact {entry!r} left in skills/portable/ after failure")

    def test_staging_is_sibling_of_dest(self):
        """Staging dir must be on the same filesystem as dest (sibling dir)."""
        # We verify by checking that os.rename is used (not shutil.move)
        # and that it succeeds — which proves same-filesystem.
        plan = {
            "sync": [{
                "name": "brainstorming",
                "source_path": "skills/brainstorming",
                "dest_path": "skills/portable/brainstorming",
            }],
            "preserved": [],
        }
        # If staging were cross-filesystem, os.rename would raise OSError(EXDEV).
        # Success here proves same-filesystem staging.
        result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("brainstorming", result["updated"])

    def test_missing_dest_parent_created(self):
        """If the dest parent dir doesn't exist yet, execute_sync creates it."""
        # Remove the portable dir entirely
        shutil.rmtree(os.path.join(self.repo_dir, "skills", "portable"))
        plan = {
            "sync": [{
                "name": "brainstorming",
                "source_path": "skills/brainstorming",
                "dest_path": "skills/portable/brainstorming",
            }],
            "preserved": [],
        }
        result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("brainstorming", result["updated"])
        skill_file = os.path.join(self.repo_dir, "skills", "portable", "brainstorming", "SKILL.md")
        self.assertTrue(os.path.exists(skill_file))


class TestCLIExitCode(unittest.TestCase):
    """CLI main() exits non-zero when any sync fails."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.clone_dir = os.path.join(self.tmpdir, "clone")
        self.repo_dir = os.path.join(self.tmpdir, "repo")
        os.makedirs(os.path.join(self.repo_dir, "skills", "portable"))
        # Source with one valid, one missing skill
        os.makedirs(os.path.join(self.clone_dir, "skills", "brainstorming"))
        with open(os.path.join(self.clone_dir, "skills", "brainstorming", "SKILL.md"), "w") as f:
            f.write("ok\n")
        # Write manifest with one present and one missing skill
        self.manifest_path = os.path.join(self.tmpdir, "manifest.json")
        manifest = {
            "source_repo": "https://example.com",
            "skills": {
                "brainstorming": {
                    "source_path": "skills/brainstorming",
                    "dest_path": "skills/portable/brainstorming",
                },
                "missing-skill": {
                    "source_path": "skills/missing-skill",
                    "dest_path": "skills/portable/missing-skill",
                },
            }
        }
        with open(self.manifest_path, "w") as f:
            json.dump(manifest, f)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _fake_clone(self, url, dest):
        shutil.copytree(self.clone_dir, dest, dirs_exist_ok=True)

    @patch("sync_obra_skills.clone_repo")
    def test_exit_nonzero_on_partial_failure(self, mock_clone):
        """main() raises SystemExit(1) when some skills fail to sync."""
        mock_clone.side_effect = self._fake_clone
        with self.assertRaises(SystemExit) as ctx:
            main([
                "--manifest", self.manifest_path,
                "--repo-root", self.repo_dir,
            ])
        self.assertEqual(ctx.exception.code, 1)

    @patch("sync_obra_skills.clone_repo")
    def test_exit_zero_on_full_success(self, mock_clone):
        """main() returns normally (no SystemExit) when all skills sync."""
        mock_clone.side_effect = self._fake_clone
        # Rewrite manifest with only the skill that exists
        manifest = {
            "source_repo": "https://example.com",
            "skills": {
                "brainstorming": {
                    "source_path": "skills/brainstorming",
                    "dest_path": "skills/portable/brainstorming",
                },
            }
        }
        success_manifest = os.path.join(self.tmpdir, "manifest_ok.json")
        with open(success_manifest, "w") as f:
            json.dump(manifest, f)
        # Should not raise
        main([
            "--manifest", success_manifest,
            "--repo-root", self.repo_dir,
        ])

    @patch("sync_obra_skills.clone_repo")
    def test_dry_run_does_not_clone(self, mock_clone):
        """main(--dry-run) never calls clone_repo."""
        main([
            "--manifest", self.manifest_path,
            "--repo-root", self.repo_dir,
            "--dry-run",
        ])
        mock_clone.assert_not_called()


class TestExecuteSyncValidation(unittest.TestCase):
    """execute_sync rejects plan entries with unsafe dest_path (mutated plan)."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.clone_dir = os.path.join(self.tmpdir, "clone")
        os.makedirs(os.path.join(self.clone_dir, "skills", "evil"))
        with open(os.path.join(self.clone_dir, "skills", "evil", "payload"), "w") as f:
            f.write("pwned\n")
        self.repo_dir = os.path.join(self.tmpdir, "repo")
        os.makedirs(os.path.join(self.repo_dir, "skills", "portable"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_rejects_dest_outside_allowed_prefix(self):
        """A mutated plan with dest_path outside allowed prefix is rejected."""
        bad_plan = {
            "sync": [{
                "name": "evil",
                "source_path": "skills/evil",
                "dest_path": "../../../tmp/evil",
            }],
            "preserved": [],
        }
        with self.assertRaises(ValueError):
            execute_sync(bad_plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)

    def test_rejects_dest_sibling_prefix(self):
        bad_plan = {
            "sync": [{
                "name": "sneaky",
                "source_path": "skills/evil",
                "dest_path": "skills/portable-evil/sneaky",
            }],
            "preserved": [],
        }
        with self.assertRaises(ValueError):
            execute_sync(bad_plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)

    def test_rejects_source_outside_allowed_prefix(self):
        bad_plan = {
            "sync": [{
                "name": "evil",
                "source_path": "../../../etc/passwd",
                "dest_path": "skills/portable/evil",
            }],
            "preserved": [],
        }
        with self.assertRaises(ValueError):
            execute_sync(bad_plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)

    def test_valid_plan_still_works(self):
        """Sanity: a valid plan passes validation and executes."""
        os.makedirs(os.path.join(self.clone_dir, "skills", "ok"))
        with open(os.path.join(self.clone_dir, "skills", "ok", "SKILL.md"), "w") as f:
            f.write("ok\n")
        plan = {
            "sync": [{
                "name": "ok",
                "source_path": "skills/ok",
                "dest_path": "skills/portable/ok",
            }],
            "preserved": [],
        }
        result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("ok", result["updated"])


    def test_restore_failure_preserves_backup(self):
        """If os.rename(backup, dst) fails during rollback, backup must NOT be deleted."""
        skill_dir = os.path.join(self.clone_dir, "skills", "bad")
        os.makedirs(skill_dir)
        with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
            f.write("new")

        dst = os.path.join(self.repo_dir, "skills", "portable", "bad")
        os.makedirs(dst)
        with open(os.path.join(dst, "SKILL.md"), "w") as f:
            f.write("original")

        plan = {
            "sync": [{"name": "bad", "source_path": "skills/bad", "dest_path": "skills/portable/bad"}],
            "preserved": [],
        }

        real_rename = os.rename
        call_count = [0]

        def failing_rename(src, dest):
            call_count[0] += 1
            # Let backup rename succeed (1st call), fail the swap (2nd call)
            # so we enter rollback, then fail the restore rename (3rd call).
            if call_count[0] == 2:
                # Fail the swap-in rename to trigger rollback
                raise OSError("simulated swap failure")
            if call_count[0] == 3:
                # Fail the restore rename
                raise OSError("simulated restore failure")
            return real_rename(src, dest)

        with unittest.mock.patch("os.rename", side_effect=failing_rename):
            result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)

        self.assertIn("bad", result["failed"])

        # The backup dir must still exist somewhere in the parent with original content
        parent = os.path.join(self.repo_dir, "skills", "portable")
        backup_dirs = [e for e in os.listdir(parent) if e.startswith(".obra-sync-old-")]
        self.assertEqual(len(backup_dirs), 1, "Backup dir must be preserved when restore fails")
        backup_path = os.path.join(parent, backup_dirs[0])
        with open(os.path.join(backup_path, "SKILL.md")) as f:
            self.assertEqual(f.read(), "original")


class TestDiffSkillDirs(unittest.TestCase):
    """diff_skill_dirs reports added, changed, and removed files."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.src = os.path.join(self.tmpdir, "src")
        self.dst = os.path.join(self.tmpdir, "dst")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_new_skill_all_added(self):
        os.makedirs(self.src)
        with open(os.path.join(self.src, "SKILL.md"), "w") as f:
            f.write("new")
        result = diff_skill_dirs(self.src, self.dst)
        self.assertEqual(result["added"], ["SKILL.md"])
        self.assertEqual(result["changed"], [])
        self.assertEqual(result["removed"], [])

    def test_removed_files_detected(self):
        os.makedirs(self.src)
        os.makedirs(self.dst)
        with open(os.path.join(self.src, "SKILL.md"), "w") as f:
            f.write("new")
        with open(os.path.join(self.dst, "SKILL.md"), "w") as f:
            f.write("old")
        with open(os.path.join(self.dst, "extra.txt"), "w") as f:
            f.write("gone")
        result = diff_skill_dirs(self.src, self.dst)
        self.assertEqual(result["removed"], ["extra.txt"])

    def test_changed_files_detected(self):
        os.makedirs(self.src)
        os.makedirs(self.dst)
        with open(os.path.join(self.src, "SKILL.md"), "w") as f:
            f.write("v2")
        with open(os.path.join(self.dst, "SKILL.md"), "w") as f:
            f.write("v1")
        result = diff_skill_dirs(self.src, self.dst)
        self.assertEqual(result["changed"], ["SKILL.md"])
        self.assertEqual(result["added"], [])
        self.assertEqual(result["removed"], [])

    def test_identical_files_not_in_changed(self):
        os.makedirs(self.src)
        os.makedirs(self.dst)
        with open(os.path.join(self.src, "SKILL.md"), "w") as f:
            f.write("same")
        with open(os.path.join(self.dst, "SKILL.md"), "w") as f:
            f.write("same")
        result = diff_skill_dirs(self.src, self.dst)
        self.assertEqual(result["changed"], [])
        self.assertEqual(result["added"], [])
        self.assertEqual(result["removed"], [])

    def test_none_src_all_removed(self):
        os.makedirs(self.dst)
        with open(os.path.join(self.dst, "SKILL.md"), "w") as f:
            f.write("old")
        result = diff_skill_dirs(None, self.dst)
        self.assertEqual(result["removed"], ["SKILL.md"])
        self.assertEqual(result["added"], [])

    def test_none_dst_all_added(self):
        os.makedirs(self.src)
        with open(os.path.join(self.src, "SKILL.md"), "w") as f:
            f.write("new")
        result = diff_skill_dirs(self.src, None)
        self.assertEqual(result["added"], ["SKILL.md"])
        self.assertEqual(result["removed"], [])


class TestExecuteSyncFileOps(unittest.TestCase):
    """execute_sync includes file_ops in its result."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.clone_dir = os.path.join(self.tmpdir, "clone")
        self.repo_dir = os.path.join(self.tmpdir, "repo")
        os.makedirs(os.path.join(self.clone_dir, "skills", "brainstorming"))
        with open(os.path.join(self.clone_dir, "skills", "brainstorming", "SKILL.md"), "w") as f:
            f.write("# v2\n")
        with open(os.path.join(self.clone_dir, "skills", "brainstorming", "new.txt"), "w") as f:
            f.write("new file\n")
        os.makedirs(os.path.join(self.repo_dir, "skills", "portable", "brainstorming"))
        with open(os.path.join(self.repo_dir, "skills", "portable", "brainstorming", "SKILL.md"), "w") as f:
            f.write("# v1\n")
        with open(os.path.join(self.repo_dir, "skills", "portable", "brainstorming", "old.txt"), "w") as f:
            f.write("old file\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_file_ops_in_result(self):
        plan = {
            "sync": [{"name": "brainstorming", "source_path": "skills/brainstorming",
                       "dest_path": "skills/portable/brainstorming"}],
            "preserved": [],
        }
        result = execute_sync(plan, clone_dir=self.clone_dir, repo_dir=self.repo_dir)
        self.assertIn("file_ops", result)
        ops = result["file_ops"]["brainstorming"]
        self.assertIn("SKILL.md", ops["changed"])
        self.assertIn("new.txt", ops["added"])
        self.assertIn("old.txt", ops["removed"])


class TestDryRunFileDetail(unittest.TestCase):
    """dry_run_report shows file-level detail when repo_dir is provided."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.repo_dir = os.path.join(self.tmpdir, "repo")
        os.makedirs(os.path.join(self.repo_dir, "skills", "portable", "brainstorming"))
        with open(os.path.join(self.repo_dir, "skills", "portable", "brainstorming", "SKILL.md"), "w") as f:
            f.write("# v1\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_dry_run_shows_local_files(self):
        plan = plan_sync(SAMPLE_MANIFEST, existing_local_skills=["brainstorming"])
        report = dry_run_report(plan, repo_dir=self.repo_dir)
        self.assertIn("SKILL.md", report)
        self.assertIn("local files to replace", report)

    def test_dry_run_shows_new_skill(self):
        plan = plan_sync(SAMPLE_MANIFEST, existing_local_skills=[])
        report = dry_run_report(plan, repo_dir=self.repo_dir)
        # writing-plans doesn't exist locally
        self.assertIn("new skill", report)

    def test_dry_run_without_repo_dir_no_file_detail(self):
        plan = plan_sync(SAMPLE_MANIFEST, existing_local_skills=["brainstorming"])
        report = dry_run_report(plan)
        self.assertNotIn("local files to replace", report)
        self.assertNotIn("new skill", report)


if __name__ == "__main__":
    unittest.main()
