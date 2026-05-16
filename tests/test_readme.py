"""Tests for README.md: platform coverage, install options, skill counts, and sync docs."""

import os
import re
import subprocess
import unittest

_repo_root = os.path.join(os.path.dirname(__file__), os.pardir)
_readme_path = os.path.join(_repo_root, "README.md")
_install_sh_path = os.path.join(_repo_root, "install.sh")


def _read_file(path):
    with open(path) as f:
        return f.read()


def _extract_install_sh_agent_flags(content):
    """Extract --<agent> flags from install.sh case statement."""
    flags = set()
    for m in re.finditer(r"--(\w+)\)\s+INSTALL_\w+=true", content):
        flags.add(m.group(1))
    return flags


def _extract_readme_install_option_flags(content):
    """Extract --<flag> entries from the README Install Script options block."""
    # Grab the fenced code block under ## Install Script
    m = re.search(
        r"## Install Script\s*\n```bash\n(.*?)```", content, re.DOTALL
    )
    if not m:
        return set()
    block = m.group(1)
    return set(re.findall(r"--([\w-]+)", block))


def _extract_readme_header_platforms(content):
    """Extract bold platform names from the first paragraph."""
    header = "\n".join(content.splitlines()[:5])
    return [m.group(1) for m in re.finditer(r"\*\*(.+?)\*\*", header)]


def _count_table_rows(section):
    """Count markdown table data rows (lines starting with '| [')."""
    return len(re.findall(r"^\| \[[\w-]+\]", section, re.MULTILINE))


def _split_sections(content):
    """Return (portable_section, tools_section, integrations_section)."""
    parts = re.split(r"^### ", content, flags=re.MULTILINE)
    portable = tools = integrations = ""
    for p in parts:
        if p.startswith("Portable"):
            portable = p
        elif p.startswith("Tools"):
            tools = p
        elif p.startswith("Integrations"):
            integrations = p
    return portable, tools, integrations


# ---------------------------------------------------------------------------
# Finding 1: All category counts and top-level total must match table rows
# ---------------------------------------------------------------------------

class TestReadmeSkillCounts(unittest.TestCase):
    """Heading counts must match actual table rows for every category."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read_file(_readme_path)
        cls.portable, cls.tools, cls.integrations = _split_sections(cls.content)

    def test_portable_count_matches_table(self):
        m = re.search(r"Portable \((\d+)\)", self.portable)
        self.assertIsNotNone(m, "Must have Portable (N) heading")
        self.assertEqual(int(m.group(1)), _count_table_rows(self.portable))

    def test_tools_count_matches_table(self):
        m = re.search(r"Tools \((\d+)\)", self.tools)
        self.assertIsNotNone(m, "Must have Tools (N) heading")
        self.assertEqual(int(m.group(1)), _count_table_rows(self.tools))

    def test_integrations_count_matches_table(self):
        m = re.search(r"Integrations \((\d+)\)", self.integrations)
        self.assertIsNotNone(m, "Must have Integrations (N) heading")
        self.assertEqual(int(m.group(1)), _count_table_rows(self.integrations))

    def test_top_level_total_matches_sum_of_categories(self):
        m = re.search(r"## Skills \((\d+)\)", self.content)
        self.assertIsNotNone(m, "Must have ## Skills (N) heading")
        stated_total = int(m.group(1))
        actual_total = (
            _count_table_rows(self.portable)
            + _count_table_rows(self.tools)
            + _count_table_rows(self.integrations)
        )
        self.assertEqual(
            stated_total, actual_total,
            f"Top-level total says {stated_total} but categories sum to {actual_total}",
        )

    def test_technical_writing_in_portable_table(self):
        self.assertIn("technical-writing", self.portable)


# ---------------------------------------------------------------------------
# Finding 2: Platform/discovery tests anchored to install section and install.sh
# ---------------------------------------------------------------------------

class TestReadmePlatformAndInstallAlignment(unittest.TestCase):
    """README platforms and install options must align with install.sh."""

    @classmethod
    def setUpClass(cls):
        cls.readme = _read_file(_readme_path)
        cls.install_sh = _read_file(_install_sh_path)
        cls.install_sh_agent_flags = _extract_install_sh_agent_flags(cls.install_sh)
        cls.readme_option_flags = _extract_readme_install_option_flags(cls.readme)
        cls.header_platforms = _extract_readme_header_platforms(cls.readme)

    # -- Every agent flag in install.sh must appear in README options block --

    def test_every_install_sh_agent_flag_documented_in_readme(self):
        """Each --<agent> flag in install.sh must appear in the README Install Script block."""
        missing = self.install_sh_agent_flags - self.readme_option_flags
        self.assertFalse(
            missing,
            f"install.sh agent flags missing from README options: {sorted(missing)}",
        )

    def test_every_readme_agent_option_exists_in_install_sh(self):
        """README should not document agent flags that install.sh doesn't support."""
        # Agent-specific flags only (exclude utility flags like all, dry-run, etc.)
        agent_keywords = {"codex", "claude", "opencode", "copilot", "antigravity"}
        readme_agent_flags = self.readme_option_flags & agent_keywords
        extra = readme_agent_flags - self.install_sh_agent_flags
        self.assertFalse(
            extra,
            f"README documents agent flags not in install.sh: {sorted(extra)}",
        )

    # -- Header platform list must cover the key agents --

    def test_header_mentions_claude(self):
        self.assertTrue(
            any("Claude" in p for p in self.header_platforms),
            f"Header platforms {self.header_platforms} must mention Claude",
        )

    def test_header_mentions_codex(self):
        self.assertTrue(
            any("Codex" in p for p in self.header_platforms),
            f"Header platforms {self.header_platforms} must mention Codex",
        )

    def test_header_mentions_opencode(self):
        self.assertTrue(
            any("OpenCode" in p for p in self.header_platforms),
            f"Header platforms {self.header_platforms} must mention OpenCode",
        )

    def test_header_mentions_copilot(self):
        self.assertTrue(
            any("Copilot" in p for p in self.header_platforms),
            f"Header platforms {self.header_platforms} must mention Copilot",
        )

    def test_header_mentions_antigravity(self):
        self.assertTrue(
            any("Antigravity" in p for p in self.header_platforms),
            f"Header platforms {self.header_platforms} must mention Antigravity",
        )

    # -- Install options block must include utility flags too --

    def test_readme_documents_all_flag(self):
        self.assertIn("all", self.readme_option_flags)

    def test_readme_documents_dry_run_flag(self):
        self.assertIn("dry-run", self.readme_option_flags)

    def test_readme_documents_uninstall_flag(self):
        self.assertIn("uninstall", self.readme_option_flags)


# ---------------------------------------------------------------------------
# Sync documentation
# ---------------------------------------------------------------------------

class TestReadmeSyncDocs(unittest.TestCase):
    """README must document the sync script and its safety model."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read_file(_readme_path)

    def test_mentions_sync_obra_skills_script(self):
        self.assertIn(
            "sync_obra_skills", self.content,
            "README must document scripts/sync_obra_skills.py",
        )

    def test_documents_sync_safety_model(self):
        content_lower = self.content.lower()
        self.assertTrue(
            ("custom" in content_lower and "preserved" in content_lower)
            or ("custom" in content_lower and "not overwritten" in content_lower)
            or ("only" in content_lower and "obra" in content_lower and "overwritten" in content_lower),
            "README must explain that custom local skills are preserved during sync",
        )

    def test_sync_reporting_description_matches_cli_output(self):
        """README sync description must not overstate what the CLI emits (counts, not file lists)."""
        # The CLI prints per-skill counts like (+N, ~N, -N), not full file lists.
        # README must not claim it reports file-level lists/operations in live mode.
        self.assertNotRegex(
            self.content,
            r"(?i)reports?\s+file[- ]level\s+operations",
            "README should not claim file-level operations; CLI emits per-skill counts",
        )

    def test_sync_examples_use_python3(self):
        """README sync examples must use python3, not bare python."""
        # Extract the sync code block
        m = re.search(
            r"## Syncing Upstream Skills\s*\n.*?```bash\n(.*?)```",
            self.content, re.DOTALL,
        )
        self.assertIsNotNone(m, "Must have sync code block")
        block = m.group(1)
        # Must not have bare 'python ' (without '3')
        self.assertNotRegex(
            block, r"(?<!\w)python(?!3)\s",
            "Sync examples must use 'python3' not 'python'",
        )


# ---------------------------------------------------------------------------
# Finding 3: Uninstall wording
# ---------------------------------------------------------------------------

class TestReadmeUninstallWording(unittest.TestCase):
    """Uninstall description must clarify it only removes symlinks created by this script."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read_file(_readme_path)

    def test_uninstall_option_says_created_by_this_script(self):
        """The --uninstall line must say 'created by this script' or equivalent."""
        # Find the --uninstall line in the install options block
        m = re.search(r"--uninstall\s+(.+)", self.content)
        self.assertIsNotNone(m, "Must have --uninstall option documented")
        desc = m.group(1).lower()
        self.assertTrue(
            "created by this script" in desc or "installed by this script" in desc,
            f"--uninstall description must clarify scope; got: {m.group(1)!r}",
        )


if __name__ == "__main__":
    unittest.main()
