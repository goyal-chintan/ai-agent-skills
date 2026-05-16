"""Tests for skill metadata: frontmatter, discovery terms, and file existence."""

import os
import re
import unittest

_repo_root = os.path.join(os.path.dirname(__file__), os.pardir)
_skills_dir = os.path.join(_repo_root, "skills", "portable")


def _parse_frontmatter(path):
    """Return dict of YAML frontmatter fields from a SKILL.md file."""
    with open(path) as f:
        content = f.read()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def _read_file(path):
    with open(path) as f:
        return f.read()


def _normalize_type_name(name):
    """Normalize a doc type name for comparison (lowercase, strip punctuation, collapse spaces)."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", name.lower())).strip()


def _parse_workflow_table_types(skill_md_content):
    """Extract type names from the markdown table in the workflow section."""
    types = []
    for line in skill_md_content.splitlines():
        # Match table data rows: | Type | Purpose | Key sections |
        m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if m:
            cell = m.group(1).strip()
            # Skip header and separator rows
            if cell.lower() in ("type", "") or cell.startswith("-"):
                continue
            types.append(_normalize_type_name(cell))
    return types


def _parse_h2_headings(content):
    """Extract ## headings from markdown content."""
    return [
        _normalize_type_name(m.group(1))
        for m in re.finditer(r"^## (.+)$", content, re.MULTILINE)
    ]


def _parse_template_headings(content):
    """Extract doc type names from '## Foo Template' headings in templates.md."""
    types = []
    for m in re.finditer(r"^## (.+?) Template$", content, re.MULTILINE):
        types.append(_normalize_type_name(m.group(1)))
    return types


def _parse_doctype_structures(content):
    """Parse document-types.md into {normalized_name: [structure_keywords]}.

    Extracts the bold keywords from each doc type's **Structure:** list.
    """
    result = {}
    current_type = None
    in_structure = False
    for line in content.splitlines():
        heading = re.match(r"^## (.+)$", line)
        if heading:
            current_type = _normalize_type_name(heading.group(1))
            in_structure = False
            continue
        if current_type and re.match(r"^\*\*Structure:\*\*", line):
            in_structure = True
            result[current_type] = []
            continue
        if in_structure and current_type:
            if line.startswith("---") or (re.match(r"^## ", line)):
                in_structure = False
                continue
            # Extract bold keyword from list items like "1. **Summary** — ..."
            m = re.match(r"^[\s]*[\d\-\*]+\.?\s*\*\*(.+?)\*\*", line)
            if m:
                result[current_type].append(m.group(1).lower().strip())
    return result


def _extract_template_block(templates_content, normalized_name):
    """Return the full section text for a given doc type template heading.

    Splits on the '---' separators between template sections rather than
    on '## ' headings, because templates contain ## headings inside code blocks.
    """
    sections = re.split(r"^---$", templates_content, flags=re.MULTILINE)
    for section in sections:
        m = re.search(r"^## (.+?) Template$", section, re.MULTILINE)
        if m and _normalize_type_name(m.group(1)) == normalized_name:
            return section
    return ""


class TestTechnicalWritingSkillMetadata(unittest.TestCase):
    """technical-writing skill must exist with proper frontmatter for discovery."""

    skill_dir = os.path.join(_skills_dir, "technical-writing")
    skill_md = os.path.join(skill_dir, "SKILL.md")

    def test_skill_md_exists(self):
        self.assertTrue(
            os.path.isfile(self.skill_md),
            f"Expected {self.skill_md} to exist",
        )

    def test_frontmatter_has_name(self):
        fm = _parse_frontmatter(self.skill_md)
        self.assertIn("name", fm)
        self.assertEqual(fm["name"], "technical-writing")

    def test_frontmatter_has_description(self):
        fm = _parse_frontmatter(self.skill_md)
        self.assertIn("description", fm)
        self.assertTrue(len(fm["description"]) > 20)

    # --- Discovery term coverage ---

    def test_description_includes_documentation_discovery_term(self):
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "").lower()
        self.assertIn(
            "documentation", desc,
            "description must include 'documentation' for discovery",
        )

    def test_description_includes_technical_writing_discovery_term(self):
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "").lower()
        self.assertTrue(
            "technical writing" in desc or "technical-writing" in desc,
            "description must include 'technical writing' for discovery",
        )

    def test_description_includes_confluence_discovery_term(self):
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "").lower()
        self.assertIn(
            "confluence", desc,
            "description must include 'Confluence' for discovery",
        )

    def test_description_includes_readme_discovery_term(self):
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "").lower()
        self.assertIn(
            "readme", desc,
            "description must include 'README' for discovery",
        )

    def test_description_includes_internal_docs_discovery_term(self):
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "").lower()
        self.assertTrue(
            "internal docs" in desc or "internal documentation" in desc or "wiki" in desc,
            "description must include 'internal docs', 'internal documentation', or 'wiki' for discovery",
        )

    def test_description_includes_clear_writing_discovery_term(self):
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "").lower()
        self.assertIn(
            "clear writing", desc,
            "description must include 'clear writing' for discovery",
        )

    def test_description_includes_concept_doc_discovery_term(self):
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "").lower()
        self.assertTrue(
            "concept doc" in desc,
            "description must include 'concept doc' for discovery",
        )

    # --- Frontmatter conventions ---

    def test_description_starts_with_use_when(self):
        """Descriptions should start with 'Use when' for consistent skill routing."""
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "")
        self.assertTrue(
            desc.startswith("Use when"),
            f"description must start with 'Use when' but starts with: {desc[:30]!r}",
        )

    def test_description_does_not_over_trigger_on_arbitrary_prose(self):
        """Description should not match generic prose/writing requests."""
        fm = _parse_frontmatter(self.skill_md)
        desc = fm.get("description", "").lower()
        for phrase in ["any prose", "general writing", "all writing", "any text"]:
            self.assertNotIn(
                phrase, desc,
                f"description should not contain broad trigger '{phrase}'",
            )

    # --- Reference files ---

    def test_reference_files_exist(self):
        refs_dir = os.path.join(self.skill_dir, "references")
        expected = [
            "core-principles.md",
            "document-types.md",
            "source-guides.md",
            "templates.md",
        ]
        for fname in expected:
            path = os.path.join(refs_dir, fname)
            self.assertTrue(
                os.path.isfile(path),
                f"Expected reference file {fname} to exist",
            )


class TestDocTypeTemplateConsistency(unittest.TestCase):
    """Workflow table, document-types.md, and templates.md must stay in sync."""

    skill_dir = os.path.join(_skills_dir, "technical-writing")
    refs_dir = os.path.join(skill_dir, "references")

    @classmethod
    def setUpClass(cls):
        cls.skill_md = _read_file(os.path.join(cls.skill_dir, "SKILL.md"))
        cls.doc_types_md = _read_file(os.path.join(cls.refs_dir, "document-types.md"))
        cls.templates_md = _read_file(os.path.join(cls.refs_dir, "templates.md"))
        cls.workflow_types = _parse_workflow_table_types(cls.skill_md)
        cls.doctype_headings = _parse_h2_headings(cls.doc_types_md)
        cls.template_headings = _parse_template_headings(cls.templates_md)

    def test_workflow_table_is_nonempty(self):
        self.assertTrue(
            len(self.workflow_types) >= 4,
            f"Workflow table should have at least 4 doc types, found {len(self.workflow_types)}",
        )

    def test_every_workflow_type_has_doctype_entry(self):
        """Every type in the SKILL.md workflow table must have a heading in document-types.md."""
        for wtype in self.workflow_types:
            self.assertTrue(
                any(wtype in dh for dh in self.doctype_headings),
                f"Workflow type {wtype!r} has no matching heading in document-types.md. "
                f"Available: {self.doctype_headings}",
            )

    def test_every_workflow_type_has_template(self):
        """Every type in the SKILL.md workflow table must have a template in templates.md."""
        for wtype in self.workflow_types:
            self.assertTrue(
                any(wtype in th for th in self.template_headings),
                f"Workflow type {wtype!r} has no matching template in templates.md. "
                f"Available: {self.template_headings}",
            )

    def test_every_doctype_has_template(self):
        """Every doc type in document-types.md must have a matching template."""
        for dh in self.doctype_headings:
            self.assertTrue(
                any(dh in th for th in self.template_headings),
                f"Document type {dh!r} has no matching template in templates.md. "
                f"Available: {self.template_headings}",
            )

    def test_howto_template_includes_goal_section(self):
        """How-To Guide template must include a Goal section matching document-types.md."""
        self.assertIn(
            "## Goal", self.templates_md,
            "How-To Guide template must include a '## Goal' section",
        )

    def test_template_bodies_contain_doctype_structure_sections(self):
        """Each template must contain headings matching its doc type's Structure keywords."""
        structures = _parse_doctype_structures(self.doc_types_md)
        for dtype, keywords in structures.items():
            if not keywords:
                continue
            template_body = _extract_template_block(self.templates_md, dtype).lower()
            if not template_body:
                # Missing template is caught by test_every_doctype_has_template
                continue
            for kw in keywords:
                self.assertTrue(
                    kw in template_body,
                    f"Template for {dtype!r} is missing structure section {kw!r}. "
                    f"Expected keywords: {keywords}",
                )

    def test_arch_design_template_is_not_adr_specific(self):
        """Architecture / Design Document template must be a general design doc, not ADR-only."""
        template = _extract_template_block(self.templates_md, "architecture design document")
        # Must have Summary section (from document-types.md structure)
        self.assertIn("## Summary", template,
            "Architecture / Design Document template must include '## Summary'")
        # The title line inside the code block must not use ADR numbering
        m = re.search(r"```markdown\n(# .+)\n", template)
        self.assertIsNotNone(m, "Template must have a title line inside the code block")
        title_line = m.group(1)
        self.assertNotIn("ADR-[number]", title_line,
            "Template title should not use ADR-specific numbering format")


if __name__ == "__main__":
    unittest.main()
