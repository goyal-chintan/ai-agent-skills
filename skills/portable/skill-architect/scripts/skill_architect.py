#!/usr/bin/env python3
"""Plan and create skills using the .system/skill-creator helper scripts."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))


def normalize_name(name: str) -> str:
    name = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    name = re.sub(r"-+", "-", name)
    if not name:
        raise ValueError("Skill name normalized to empty string")
    return name


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def update_frontmatter(skill_md: Path, name: str, description: str) -> None:
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return
    end = content.find("\n---\n", 4)
    if end == -1:
        return

    fm = content[4:end].splitlines()
    new_fm = []
    have_name = False
    have_desc = False
    for line in fm:
        if line.startswith("name:"):
            new_fm.append(f"name: {name}")
            have_name = True
        elif line.startswith("description:"):
            new_fm.append(f"description: {description}")
            have_desc = True
        else:
            new_fm.append(line)

    if not have_name:
        new_fm.append(f"name: {name}")
    if not have_desc:
        new_fm.append(f"description: {description}")

    remainder = content[end + 5 :]
    rebuilt = "---\n" + "\n".join(new_fm).rstrip() + "\n---\n" + remainder
    skill_md.write_text(rebuilt, encoding="utf-8")


def append_architect_sections(skill_md: Path) -> None:
    marker = "## Trigger Examples"
    content = skill_md.read_text(encoding="utf-8")
    if marker in content:
        return
    extra = """

## Trigger Examples

- "Pick the best skill for this request and install missing ones if needed."
- "Create a new skill for this repeated workflow."
- "Update this skill's trigger conditions and add validation."

## Non-Trigger Boundaries

- Simple one-off coding changes where no reusable workflow is needed.
- Casual Q&A with no skill creation or orchestration need.
"""
    skill_md.write_text(content.rstrip() + "\n" + extra.lstrip("\n"), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Skill architect wrapper")
    parser.add_argument("--name", required=True, help="Skill name (will be normalized to hyphen-case)")
    parser.add_argument("--description", required=True, help="Skill description for frontmatter")
    parser.add_argument("--resources", default="", help="Comma-separated: scripts,references,assets")
    parser.add_argument("--dest", default="", help="Destination directory; default $CODEX_HOME/skills")
    parser.add_argument("--plan-only", action="store_true", help="Print planned commands without writing")
    parser.add_argument("--apply", action="store_true", help="Create and validate the skill")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.plan_only and args.apply:
        print("Use either --plan-only or --apply, not both.", file=sys.stderr)
        return 2

    skill_name = normalize_name(args.name)
    base = Path(args.dest) if args.dest else (codex_home() / "skills")

    skill_creator_root = codex_home() / "skills" / ".system" / "skill-creator"
    init_script = skill_creator_root / "scripts" / "init_skill.py"
    validate_script = skill_creator_root / "scripts" / "quick_validate.py"

    if not init_script.exists() or not validate_script.exists():
        print("Required skill-creator scripts not found under $CODEX_HOME/skills/.system/skill-creator", file=sys.stderr)
        return 1

    init_cmd = ["python3", str(init_script), skill_name, "--path", str(base)]
    if args.resources.strip():
        init_cmd.extend(["--resources", args.resources.strip()])

    skill_dir = base / skill_name
    skill_md = skill_dir / "SKILL.md"
    validate_cmd = ["python3", str(validate_script), str(skill_dir)]

    if args.plan_only or not args.apply:
        print("Plan-only mode")
        print("1) Initialize skeleton:")
        print("   " + " ".join(init_cmd))
        print("2) Update frontmatter description and trigger boundaries")
        print("3) Validate:")
        print("   " + " ".join(validate_cmd))
        return 0

    init_proc = run(init_cmd)
    if init_proc.returncode != 0:
        print(init_proc.stderr or init_proc.stdout, file=sys.stderr)
        return init_proc.returncode

    if not skill_md.exists():
        print(f"SKILL.md not found after init: {skill_md}", file=sys.stderr)
        return 1

    update_frontmatter(skill_md, skill_name, args.description.strip())
    append_architect_sections(skill_md)

    validate_proc = run(validate_cmd)
    if validate_proc.returncode != 0:
        print(validate_proc.stdout)
        print(validate_proc.stderr, file=sys.stderr)
        return validate_proc.returncode

    print(f"Created and validated: {skill_dir}")
    print(validate_proc.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
