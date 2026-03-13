#!/usr/bin/env python3
"""Select best-fit Codex skills and propose plan-first resolution for missing capabilities."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "please",
    "should",
    "that",
    "the",
    "this",
    "to",
    "use",
    "want",
    "we",
    "with",
    "you",
    "your",
}

KEYWORD_BOOSTS = {
    "screenshot": {"screenshot", "screen", "window", "capture", "desktop"},
    "jupyter-notebook": {"jupyter", "notebook", "ipynb", "experiment", "tutorial"},
    "spreadsheet": {"spreadsheet", "xlsx", "csv", "tsv", "openpyxl", "pandas"},
    "pdf": {"pdf", "reportlab", "pdfplumber", "pypdf"},
    "playwright": {"playwright", "browser", "automation", "navigate", "scrape"},
    "imagegen": {"image", "inpaint", "mask", "background", "transparent"},
    "gh-address-comments": {"review", "comments", "pull", "request", "gh"},
    "gh-fix-ci": {"ci", "checks", "workflow", "actions", "failing"},
    "skill-installer": {"install", "skills", "curated", "github"},
    "skill-creator": {"create", "skill", "update", "skill.md"},
    "brainstorm-general": {"brainstorm", "options", "tradeoff", "plan"},
}

MIN_SELECTION_SCORE = 6

CAPABILITY_RULES = [
    {
        "capability": "desktop screenshot capture",
        "patterns": [r"\bscreenshot\b", r"screen\s*capture", r"capture\s+(the\s+)?screen"],
        "skill": "screenshot",
    },
    {
        "capability": "jupyter notebook creation/editing",
        "patterns": [r"\bjupyter\b", r"\.ipynb\b", r"\bnotebook\b"],
        "skill": "jupyter-notebook",
    },
    {
        "capability": "spreadsheet processing",
        "patterns": [r"\bxlsx\b", r"\bcsv\b", r"\bspreadsheet\b", r"\btsv\b"],
        "skill": "spreadsheet",
    },
    {
        "capability": "pdf processing",
        "patterns": [r"\bpdf\b", r"reportlab", r"pdfplumber", r"pypdf"],
        "skill": "pdf",
    },
    {
        "capability": "browser automation",
        "patterns": [r"\bplaywright\b", r"browser\s+automation", r"automate\s+browser"],
        "skill": "playwright",
    },
    {
        "capability": "github review comments",
        "patterns": [r"review\s+comment", r"address\s+comment", r"pull\s+request\s+comment"],
        "skill": "gh-address-comments",
    },
    {
        "capability": "github ci checks debugging",
        "patterns": [r"\bci\b", r"github\s+actions", r"failing\s+checks"],
        "skill": "gh-fix-ci",
    },
]


@dataclass
class Skill:
    name: str
    description: str
    path: str
    is_system: bool


@dataclass
class CuratedLookup:
    names: set[str]
    ssl_failed: bool
    error: str | None


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def tokenize(text: str) -> list[str]:
    return [tok for tok in re.findall(r"[a-z0-9]+", normalize_text(text)) if tok not in STOPWORDS]


def parse_frontmatter(skill_md: Path) -> tuple[str | None, str]:
    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    if not content.startswith("---\n"):
        return None, ""
    end = content.find("\n---\n", 4)
    if end == -1:
        return None, ""
    fm = content[4:end]
    name = None
    description = ""
    for line in fm.splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"').strip("'")
    return name, description


def scan_installed_skills(skills_dir: Path) -> dict[str, Skill]:
    results: dict[str, Skill] = {}
    if not skills_dir.exists():
        return results

    for skill_md in skills_dir.rglob("SKILL.md"):
        parent = skill_md.parent
        rel_parts = parent.relative_to(skills_dir).parts
        if any(part.startswith(".") and part != ".system" for part in rel_parts):
            continue
        name, description = parse_frontmatter(skill_md)
        skill_name = (name or parent.name).strip().lower()
        if not skill_name:
            continue
        results[skill_name] = Skill(
            name=skill_name,
            description=description,
            path=str(parent),
            is_system=(".system" in rel_parts),
        )
    return results


def extract_explicit_mentions(text: str) -> set[str]:
    return {m.lower() for m in re.findall(r"\$([a-zA-Z0-9][a-zA-Z0-9-]*)", text)}


def score_skill(skill: Skill, prompt_tokens: list[str], full_text: str, explicit: set[str]) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0

    if skill.name in explicit:
        score += 1000
        reasons.append("explicit $skill mention")

    skill_tokens = set(tokenize(skill.name.replace("-", " ") + " " + skill.description))
    overlap = sorted(set(prompt_tokens) & skill_tokens)
    if overlap:
        score += len(overlap) * 4
        reasons.append(f"token overlap: {', '.join(overlap[:6])}")

    boosts = KEYWORD_BOOSTS.get(skill.name, set())
    matched_boosts = sorted({kw for kw in boosts if kw in full_text})
    if matched_boosts:
        score += len(matched_boosts) * 5
        reasons.append(f"keyword signals: {', '.join(matched_boosts[:6])}")

    if skill.is_system and skill.name not in explicit:
        # Keep system helper skills opt-in unless user explicitly asks for them.
        score = max(0, score - 6)
        if score > 0:
            reasons.append("system-skill penalty")

    return score, reasons


def detect_capability_needs(full_text: str) -> list[dict[str, str]]:
    needs = []
    for rule in CAPABILITY_RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, full_text, flags=re.IGNORECASE):
                needs.append({"capability": rule["capability"], "skill": rule["skill"]})
                break
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for need in needs:
        key = (need["capability"], need["skill"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(need)
    return deduped


def derive_unknown_capability(prompt_tokens: list[str]) -> tuple[str, str]:
    meaningful = [t for t in prompt_tokens if len(t) > 2]
    if not meaningful:
        return "unspecified capability", "custom-skill"
    phrase_tokens = meaningful[:3]
    capability = " ".join(phrase_tokens)
    suggested_name = "-".join(phrase_tokens[:2]) + "-skill"
    suggested_name = re.sub(r"-+", "-", suggested_name).strip("-")
    return capability, suggested_name


def run_subprocess(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def compact_error(raw: str) -> str:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        return "unknown error"
    # Keep signal while avoiding huge trace dumps.
    if len(lines) <= 6:
        return " | ".join(lines)
    return " | ".join(lines[:3] + [lines[-1]])


def lookup_curated_skills(codex_home: Path) -> CuratedLookup:
    list_script = codex_home / "skills" / ".system" / "skill-installer" / "scripts" / "list-skills.py"
    if not list_script.exists():
        return CuratedLookup(names=set(), ssl_failed=False, error="skill-installer list script not found")

    cmd = ["python3", str(list_script), "--format", "json"]
    proc = run_subprocess(cmd)
    if proc.returncode != 0:
        err = (proc.stderr or "") + (proc.stdout or "")
        ssl_failed = "CERTIFICATE_VERIFY_FAILED" in err or "ssl" in err.lower()
        return CuratedLookup(
            names=set(),
            ssl_failed=ssl_failed,
            error=compact_error(err.strip() or "curated listing failed"),
        )

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return CuratedLookup(names=set(), ssl_failed=False, error="invalid curated json response")

    names = {entry.get("name", "").strip().lower() for entry in payload if isinstance(entry, dict)}
    names.discard("")
    return CuratedLookup(names=names, ssl_failed=False, error=None)


def build_install_command(codex_home: Path, skill_name: str, method: str) -> str:
    install_script = codex_home / "skills" / ".system" / "skill-installer" / "scripts" / "install-skill-from-github.py"
    return (
        "python3 "
        + f'"{install_script}" '
        + "--repo openai/skills "
        + f'--path "skills/.curated/{skill_name}" '
        + f"--method {method}"
    )


def attempt_install(codex_home: Path, skill_name: str) -> dict[str, str]:
    install_script = codex_home / "skills" / ".system" / "skill-installer" / "scripts" / "install-skill-from-github.py"
    if not install_script.exists():
        return {"status": "error", "message": "install script not found"}

    auto_cmd = [
        "python3",
        str(install_script),
        "--repo",
        "openai/skills",
        "--path",
        f"skills/.curated/{skill_name}",
        "--method",
        "auto",
    ]
    auto_proc = run_subprocess(auto_cmd)
    if auto_proc.returncode == 0:
        return {"status": "installed", "method": "auto", "message": auto_proc.stdout.strip()}

    err = (auto_proc.stderr or "") + (auto_proc.stdout or "")
    if "CERTIFICATE_VERIFY_FAILED" in err or "ssl" in err.lower():
        git_cmd = auto_cmd[:-1] + ["git"]
        git_proc = run_subprocess(git_cmd)
        if git_proc.returncode == 0:
            return {"status": "installed", "method": "git", "message": git_proc.stdout.strip()}
        return {
            "status": "error",
            "method": "git",
            "message": (git_proc.stderr or git_proc.stdout or "install failed").strip(),
        }

    return {"status": "error", "method": "auto", "message": err.strip() or "install failed"}


def make_resolution_entries(
    missing_items: Iterable[dict[str, str]],
    curated: CuratedLookup,
    codex_home: Path,
) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for item in missing_items:
        skill_name = item.get("skill") or item.get("suggested_skill") or ""
        skill_name = skill_name.lower()

        install_auto = build_install_command(codex_home, skill_name, "auto") if skill_name else None
        install_git = build_install_command(codex_home, skill_name, "git") if skill_name else None

        curated_status = "unknown"
        if skill_name and curated.names:
            curated_status = "available" if skill_name in curated.names else "not_found"
        elif curated.ssl_failed:
            curated_status = "unverified_ssl_error"

        create_cmd = (
            "python3 "
            + f'"{codex_home / "skills" / "skill-architect" / "scripts" / "skill_architect.py"}" '
            + f'--name "{skill_name or item.get("capability", "new-skill").replace(" ", "-")}" '
            + f'--description "Skill for {item.get("capability", "missing capability")}" '
            + "--plan-only"
        )

        entries.append(
            {
                "capability": item.get("capability", "missing capability"),
                "required_skill": item.get("skill"),
                "suggested_skill": skill_name or None,
                "resolution_order": [
                    "local installed skills",
                    "curated install via skill-installer",
                    "create via skill-architect",
                ],
                "curated_status": curated_status,
                "recommended_install_command": install_git if curated.ssl_failed else install_auto,
                "fallback_install_command": install_git,
                "recommended_create_command": create_cmd,
            }
        )
    return entries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select best-fit Codex skills for a prompt.")
    parser.add_argument("--prompt", required=True, help="User prompt to analyze")
    parser.add_argument("--context", action="append", default=[], help="Optional extra context")
    parser.add_argument("--skills-dir", help="Override skills directory (default: $CODEX_HOME/skills)")
    parser.add_argument("--max-selected", type=int, default=4, help="Max number of selected skills")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument(
        "--attempt-install",
        action="store_true",
        help="Attempt curated install for missing known skills (not default; plan-first remains default).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    codex_home = default_codex_home()
    skills_dir = Path(args.skills_dir) if args.skills_dir else (codex_home / "skills")

    full_text = normalize_text(" ".join([args.prompt] + list(args.context)))
    prompt_tokens = tokenize(full_text)

    installed = scan_installed_skills(skills_dir)
    explicit = extract_explicit_mentions(full_text)

    scored = []
    missing_explicit = []
    for name in sorted(explicit):
        if name not in installed:
            missing_explicit.append({"capability": f"explicitly requested skill {name}", "skill": name})

    for skill in installed.values():
        score, reasons = score_skill(skill, prompt_tokens, full_text, explicit)
        if score > 0:
            scored.append((score, skill, reasons))

    scored.sort(key=lambda item: (-item[0], item[1].name))
    selected = []
    selected_names = set()
    for score, skill, reasons in scored:
        if score < MIN_SELECTION_SCORE:
            continue
        if skill.name in selected_names:
            continue
        selected.append(
            {
                "name": skill.name,
                "score": score,
                "reasons": reasons,
                "path": skill.path,
            }
        )
        selected_names.add(skill.name)
        if len(selected) >= args.max_selected:
            break

    needs = detect_capability_needs(full_text)
    missing = []
    for need in needs:
        if need["skill"] in installed:
            if need["skill"] not in selected_names:
                selected.append(
                    {
                        "name": need["skill"],
                        "score": 900,
                        "reasons": [f"capability match: {need['capability']}"],
                        "path": installed[need["skill"]].path,
                    }
                )
                selected_names.add(need["skill"])
        else:
            missing.append({"capability": need["capability"], "skill": need["skill"]})

    missing.extend(missing_explicit)

    if not selected and not missing:
        capability, suggested_skill = derive_unknown_capability(prompt_tokens)
        missing.append({"capability": capability, "suggested_skill": suggested_skill})

    curated = lookup_curated_skills(codex_home)
    resolutions = make_resolution_entries(missing, curated, codex_home)

    install_results = []
    if args.attempt_install:
        for item in missing:
            skill_name = (item.get("skill") or "").strip().lower()
            if not skill_name:
                continue
            install_results.append({"skill": skill_name, "result": attempt_install(codex_home, skill_name)})

    result = {
        "mode": "plan-first",
        "selected_skills": selected,
        "missing_capabilities": resolutions,
        "curated_lookup": {
            "available_count": len(curated.names),
            "ssl_failed": curated.ssl_failed,
            "error": curated.error,
        },
        "install_attempts": install_results,
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("Mode: plan-first (recommend before mutate)")
    if selected:
        print("\nSelected skills:")
        for item in selected:
            reasons = "; ".join(item["reasons"])
            print(f"- {item['name']} (score {item['score']}): {reasons}")
    else:
        print("\nSelected skills: none")

    if resolutions:
        print("\nMissing capabilities and resolution path:")
        for item in resolutions:
            print(f"- Capability: {item['capability']}")
            print(f"  Suggested skill: {item.get('suggested_skill') or item.get('required_skill')}")
            print(f"  Curated status: {item['curated_status']}")
            if item["recommended_install_command"]:
                print(f"  Install command: {item['recommended_install_command']}")
            if item["fallback_install_command"]:
                print(f"  SSL fallback:   {item['fallback_install_command']}")
            print(f"  Create command: {item['recommended_create_command']}")
    else:
        print("\nMissing capabilities: none")

    if curated.ssl_failed:
        print("\nNote: curated listing hit SSL verification failure. Use git method fallback if installing.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
