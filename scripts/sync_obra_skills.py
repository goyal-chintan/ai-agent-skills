#!/usr/bin/env python3
"""Sync selected skills from obra/superpowers into this repo.

Design principles:
- Explicit allowlist only: only skills listed in the manifest are synced.
- Path safety: destination must resolve inside ALLOWED_DEST_PREFIX.
- Source safety: source paths must resolve inside ALLOWED_SOURCE_PREFIX.
- Side-effect-free planning: plan_sync() does no I/O beyond reading the manifest.
- Unmapped local skills are never modified or removed.
- Dry-run reports both sync actions and preserved unmapped skills.
"""

from __future__ import annotations

import json
import os
import posixpath
import shutil
import subprocess
import tempfile
import uuid

ALLOWED_DEST_PREFIX = "skills/portable/"
ALLOWED_SOURCE_PREFIX = "skills/"


def load_manifest(path: str) -> dict:
    """Load and return the JSON manifest from *path*.

    Raises FileNotFoundError if the file does not exist.
    """
    with open(path, "r") as f:
        return json.load(f)


def _validate_dest_path(name: str, dest_path: str) -> str:
    """Raise ValueError if *dest_path* escapes the allowed prefix, contains '..',
    or equals the prefix root itself.

    Returns the normalized path.
    """
    if ".." in dest_path.split("/"):
        raise ValueError(
            f"Skill {name!r}: dest_path {dest_path!r} contains '..' component"
        )
    normalized = posixpath.normpath(dest_path)
    if not (normalized + "/").startswith(ALLOWED_DEST_PREFIX):
        raise ValueError(
            f"Skill {name!r}: dest_path {dest_path!r} resolves to "
            f"{normalized!r} which is outside {ALLOWED_DEST_PREFIX!r}"
        )
    # Reject the prefix root itself — must be a child path
    prefix_root = ALLOWED_DEST_PREFIX.rstrip("/")
    if normalized == prefix_root:
        raise ValueError(
            f"Skill {name!r}: dest_path {dest_path!r} resolves to the prefix "
            f"root {prefix_root!r}; must target a child directory"
        )
    return normalized


def _validate_source_path(name: str, source_path: str) -> str:
    """Validate and normalize a source path. Returns normalized path.

    Raises ValueError if the path escapes ALLOWED_SOURCE_PREFIX, contains '..',
    or equals the prefix root itself.
    """
    if ".." in source_path.split("/"):
        raise ValueError(
            f"Skill {name!r}: source_path {source_path!r} contains '..' component"
        )
    normalized = posixpath.normpath(source_path)
    if not (normalized + "/").startswith(ALLOWED_SOURCE_PREFIX):
        raise ValueError(
            f"Skill {name!r}: source_path {source_path!r} resolves to "
            f"{normalized!r} which is outside {ALLOWED_SOURCE_PREFIX!r}"
        )
    # Reject the prefix root itself — must be a child path
    prefix_root = ALLOWED_SOURCE_PREFIX.rstrip("/")
    if normalized == prefix_root:
        raise ValueError(
            f"Skill {name!r}: source_path {source_path!r} resolves to the prefix "
            f"root {prefix_root!r}; must target a child directory"
        )
    return normalized


def resolve_source_paths(manifest: dict) -> dict[str, str]:
    """Validate and resolve all source paths in the manifest.

    Returns a dict mapping skill name -> normalized source path.
    Raises ValueError if any source path is unsafe.
    """
    result = {}
    for name, entry in manifest.get("skills", {}).items():
        result[name] = _validate_source_path(name, entry["source_path"])
    return result


def plan_sync(
    manifest: dict,
    existing_local_skills: list[str] | None = None,
) -> dict:
    """Return a plan with sync actions and preserved skills.

    Returns a dict with:
      - "sync": list of dicts with keys name, source_path, dest_path
      - "preserved": list of local skill names not in the manifest

    Only skills present in the manifest are included in sync.
    Unmapped local skills appear in preserved.

    Raises ValueError if any dest_path or source_path is unsafe.
    """
    skills = manifest.get("skills", {})
    existing = existing_local_skills or []

    sync = []
    for name, entry in skills.items():
        dest_path = _validate_dest_path(name, entry["dest_path"])
        source_path = _validate_source_path(name, entry["source_path"])
        sync.append({
            "name": name,
            "source_path": source_path,
            "dest_path": dest_path,
        })

    mapped_names = set(skills.keys())
    preserved = sorted(n for n in existing if n not in mapped_names)

    return {"sync": sync, "preserved": preserved}


def _list_files(directory: str) -> set[str]:
    """Return the set of relative file paths under *directory*."""
    result: set[str] = set()
    for dirpath, _dirnames, filenames in os.walk(directory):
        for fname in filenames:
            full = os.path.join(dirpath, fname)
            result.add(os.path.relpath(full, directory))
    return result


def diff_skill_dirs(src_dir: str | None, dst_dir: str | None) -> dict[str, list[str]]:
    """Compare two skill directories and return file-level operations.

    Returns a dict with keys: added, changed, removed — each a sorted list
    of relative file paths.

    Either directory may be None or non-existent:
    - src_dir missing/None: all dst files are 'removed'
    - dst_dir missing/None: all src files are 'added'
    """
    import filecmp

    src_files = _list_files(src_dir) if src_dir and os.path.isdir(src_dir) else set()
    dst_files = _list_files(dst_dir) if dst_dir and os.path.isdir(dst_dir) else set()

    added = sorted(src_files - dst_files)
    removed = sorted(dst_files - src_files)
    changed = []
    for f in sorted(src_files & dst_files):
        sf = os.path.join(src_dir, f) if src_dir else ""
        df = os.path.join(dst_dir, f) if dst_dir else ""
        if sf and df and not filecmp.cmp(sf, df, shallow=False):
            changed.append(f)

    return {"added": added, "changed": changed, "removed": removed}


def dry_run_report(plan: dict, *, repo_dir: str | None = None) -> str:
    """Format a human-readable dry-run report from a plan.

    If *repo_dir* is provided, reports file-level detail for existing local
    skill directories (showing files that would be removed/replaced).
    """
    lines = []
    sync = plan["sync"]
    preserved = plan["preserved"]

    lines.append(f"Sync: {len(sync)} skill(s) to sync")
    for a in sync:
        lines.append(f"  {a['name']}: {a['source_path']} -> {a['dest_path']}")
        if repo_dir:
            dst_abs = os.path.join(repo_dir, a["dest_path"])
            if os.path.isdir(dst_abs):
                local_files = sorted(_list_files(dst_abs))
                if local_files:
                    lines.append(f"    local files to replace: {', '.join(local_files)}")
                else:
                    lines.append("    (empty local directory)")
            else:
                lines.append("    (new skill — no local directory)")

    lines.append(f"Preserved: {len(preserved)} unmapped local skill(s)")
    for name in preserved:
        lines.append(f"  {name}")

    return "\n".join(lines)


def clone_repo(repo_url: str, dest: str) -> None:
    """Shallow-clone *repo_url* into *dest* directory."""
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, dest],
        check=True,
    )


def _check_no_ancestor_symlinks(path: str, root: str, name: str, label: str) -> None:
    """Raise ValueError if *root* itself or any component between *root* and *path* is a symlink."""
    if os.path.islink(root):
        raise ValueError(
            f"Skill {name!r}: {label} root {root!r} is a symlink"
        )
    # Walk from root down to path, checking each intermediate component.
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    current = root
    for part in parts:
        current = os.path.join(current, part)
        if os.path.islink(current):
            raise ValueError(
                f"Skill {name!r}: symlink found in {label} ancestor at {current!r}"
            )


def _check_no_symlinks(path: str, name: str) -> None:
    """Raise ValueError if *path* or anything inside it is a symlink."""
    if os.path.islink(path):
        raise ValueError(
            f"Skill {name!r}: source path {path!r} is a symlink"
        )
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for entry in dirnames + filenames:
                full = os.path.join(dirpath, entry)
                if os.path.islink(full):
                    raise ValueError(
                        f"Skill {name!r}: symlink found at {full!r}"
                    )


def execute_sync(plan: dict, *, clone_dir: str, repo_dir: str) -> dict:
    """Execute a sync plan: replace mapped skill dirs, skip missing sources.

    Validates every action's dest_path and source_path against allowed
    prefixes before performing any I/O, even if the plan was mutated.
    Rejects symlinks in source trees.
    Uses atomic temp/swap so old content survives copy failure.

    Returns a summary dict with keys: updated, preserved, failed.
    Raises ValueError if any path in the plan is unsafe or contains symlinks.
    """
    # Validate ALL entries before touching the filesystem
    for action in plan["sync"]:
        _validate_dest_path(action["name"], action["dest_path"])
        _validate_source_path(action["name"], action["source_path"])

    # Check for symlinks in all source dirs before any I/O
    for action in plan["sync"]:
        src = os.path.join(clone_dir, action["source_path"])
        # Reject symlinks in ancestor path components (e.g. clone_dir/skills is a symlink)
        _check_no_ancestor_symlinks(src, clone_dir, action["name"], "source")
        if os.path.exists(src) or os.path.islink(src):
            _check_no_symlinks(src, action["name"])

    # Check for symlinks in destination ancestor paths before any I/O
    for action in plan["sync"]:
        dst = os.path.join(repo_dir, action["dest_path"])
        _check_no_ancestor_symlinks(dst, repo_dir, action["name"], "destination")

    updated = []
    failed = []
    file_ops: dict[str, dict[str, list[str]]] = {}

    for action in plan["sync"]:
        src = os.path.join(clone_dir, action["source_path"])
        dst = os.path.join(repo_dir, action["dest_path"])

        if not os.path.isdir(src):
            failed.append(action["name"])
            continue

        # Compute file-level diff before replacing
        file_ops[action["name"]] = diff_skill_dirs(src, dst)

        if not os.path.isdir(src):
            failed.append(action["name"])
            continue

        # Ensure destination parent exists
        dst_parent = os.path.dirname(dst)
        os.makedirs(dst_parent, exist_ok=True)

        # Atomic swap: stage as hidden sibling of dst (same filesystem,
        # so os.rename is guaranteed to work without EXDEV).
        tag = uuid.uuid4().hex[:12]
        staging = os.path.join(dst_parent, f".obra-sync-new-{tag}")
        backup = os.path.join(dst_parent, f".obra-sync-old-{tag}")
        has_backup = False
        try:
            # Copy source to staging dir (sibling of dst)
            shutil.copytree(src, staging)

            # Backup existing dest (same-fs rename, atomic)
            if os.path.exists(dst):
                os.rename(dst, backup)
                has_backup = True

            # Swap in the new copy (same-fs rename, atomic)
            os.rename(staging, dst)

            # Success — clean up backup
            if has_backup:
                shutil.rmtree(backup, ignore_errors=True)

            updated.append(action["name"])
        except Exception:
            # Restore backup if swap failed
            if os.path.exists(staging):
                shutil.rmtree(staging, ignore_errors=True)
            if has_backup and os.path.exists(backup) and not os.path.exists(dst):
                try:
                    os.rename(backup, dst)
                except OSError:
                    # Restore failed — leave backup in place as the only
                    # remaining copy of the original content.
                    pass
            if has_backup and os.path.exists(backup) and os.path.exists(dst):
                # Only clean up backup if dst was successfully restored
                shutil.rmtree(backup, ignore_errors=True)
            failed.append(action["name"])

    return {
        "updated": updated,
        "preserved": list(plan["preserved"]),
        "failed": failed,
        "file_ops": file_ops,
    }


def main(argv: list[str] | None = None) -> None:
    """CLI entrypoint. Parses *argv* (defaults to sys.argv[1:]) and runs sync.

    Raises SystemExit(1) on failure.
    """
    import argparse
    import sys

    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_repo_root = os.path.normpath(os.path.join(script_dir, os.pardir))

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default=os.path.join(default_repo_root, "config", "obra_skills.json"),
        help="Path to obra_skills.json manifest",
    )
    parser.add_argument(
        "--repo-root",
        default=default_repo_root,
        help="Repository root directory",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    args = parser.parse_args(argv)

    manifest = load_manifest(args.manifest)

    # Discover existing local skills
    portable_dir = os.path.join(args.repo_root, "skills", "portable")
    if os.path.isdir(portable_dir):
        local_skills = [
            d for d in os.listdir(portable_dir)
            if os.path.isdir(os.path.join(portable_dir, d))
        ]
    else:
        local_skills = []

    result = plan_sync(manifest, existing_local_skills=local_skills)

    if args.dry_run:
        print(dry_run_report(result, repo_dir=args.repo_root))
        return

    repo_url = manifest.get("source_repo", "")
    if not repo_url:
        print("Error: source_repo not set in manifest.", file=sys.stderr)
        raise SystemExit(1)

    clone_dir = tempfile.mkdtemp(prefix="obra-sync-")
    try:
        print(f"Cloning {repo_url} ...")
        clone_repo(repo_url, clone_dir)
        summary = execute_sync(result, clone_dir=clone_dir, repo_dir=args.repo_root)
        print(f"Updated: {len(summary['updated'])} skill(s)")
        for name in summary["updated"]:
            ops = summary["file_ops"].get(name, {})
            added = ops.get("added", [])
            changed = ops.get("changed", [])
            removed = ops.get("removed", [])
            detail = []
            if added:
                detail.append(f"+{len(added)}")
            if changed:
                detail.append(f"~{len(changed)}")
            if removed:
                detail.append(f"-{len(removed)}")
            suffix = f" ({', '.join(detail)})" if detail else ""
            print(f"  {name}{suffix}")
        if summary["failed"]:
            print(f"Failed: {len(summary['failed'])} skill(s)")
            for name in summary["failed"]:
                print(f"  {name}")
        print(f"Preserved: {len(summary['preserved'])} unmapped skill(s)")
        for name in summary["preserved"]:
            print(f"  {name}")
        if summary["failed"]:
            raise SystemExit(1)
    finally:
        shutil.rmtree(clone_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
