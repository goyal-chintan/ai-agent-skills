#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────
# AI Agent Skills — Installer
# Symlinks skills into Claude, Codex, and/or Antigravity
# ─────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"

# Defaults
INSTALL_CODEX=false
INSTALL_CLAUDE=false
INSTALL_ANTIGRAVITY=false
INSTALL_ALL=false
PORTABLE_ONLY=false
DRY_RUN=false

# Agent skill directories
CODEX_SKILLS="${CODEX_HOME:-$HOME/.codex}/skills"
CLAUDE_COMMANDS="$HOME/.claude/commands"
ANTIGRAVITY_SKILLS="$HOME/.gemini/antigravity/skills"

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Install AI agent skills via symlinks.

Options:
  --codex           Install for Codex
  --claude          Install for Claude Code
  --antigravity     Install for Antigravity
  --all             Install for all agents (default if none specified)
  --portable-only   Only install portable skills (skip tools & integrations)
  --dry-run         Show what would be done without doing it
  --uninstall       Remove all symlinks created by this script
  -h, --help        Show this help

Examples:
  ./install.sh --all                    # Install everything for all agents
  ./install.sh --codex --claude         # Install for Codex and Claude only
  ./install.sh --all --portable-only    # Only portable skills, all agents
EOF
  exit 0
}

# ── Parse args ──────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case $1 in
    --codex)        INSTALL_CODEX=true ;;
    --claude)       INSTALL_CLAUDE=true ;;
    --antigravity)  INSTALL_ANTIGRAVITY=true ;;
    --all)          INSTALL_ALL=true ;;
    --portable-only) PORTABLE_ONLY=true ;;
    --dry-run)      DRY_RUN=true ;;
    --uninstall)    UNINSTALL=true ;;
    -h|--help)      usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
  shift
done

# Default to --all if nothing specified
if ! $INSTALL_CODEX && ! $INSTALL_CLAUDE && ! $INSTALL_ANTIGRAVITY && ! $INSTALL_ALL; then
  INSTALL_ALL=true
fi
if $INSTALL_ALL; then
  INSTALL_CODEX=true
  INSTALL_CLAUDE=true
  INSTALL_ANTIGRAVITY=true
fi

# ── Uninstall mode ──────────────────────────────────────────
if [[ "${UNINSTALL:-false}" == "true" ]]; then
  echo "🗑  Removing symlinked skills..."
  for dir in "$CODEX_SKILLS" "$ANTIGRAVITY_SKILLS"; do
    if [[ -d "$dir" ]]; then
      find "$dir" -maxdepth 1 -type l -lname "*ai-agent-skills*" -exec rm -v {} \;
    fi
  done
  if [[ -d "$CLAUDE_COMMANDS" ]]; then
    find "$CLAUDE_COMMANDS" -maxdepth 1 -type l -lname "*ai-agent-skills*" -exec rm -v {} \;
  fi
  echo "✅ Uninstall complete."
  exit 0
fi

# ── Helpers ─────────────────────────────────────────────────
installed=0
skipped=0

link_skill_dir() {
  local src="$1" dest="$2" name
  name="$(basename "$src")"

  if [[ -L "$dest/$name" ]]; then
    # Already a symlink — check if it points to us
    if [[ "$(readlink "$dest/$name")" == "$src" ]]; then
      ((skipped++)) || true
      return
    fi
    rm "$dest/$name"
  elif [[ -d "$dest/$name" ]]; then
    echo "  ⚠️  Skipping $name — real directory exists at $dest/$name"
    ((skipped++)) || true
    return
  fi

  if $DRY_RUN; then
    echo "  [dry-run] ln -s $src → $dest/$name"
  else
    mkdir -p "$dest"
    ln -s "$src" "$dest/$name"
  fi
  ((installed++)) || true
}

link_skill_claude() {
  local src="$1" name
  name="$(basename "$src")"
  local skill_md="$src/SKILL.md"
  local dest_file="$CLAUDE_COMMANDS/$name.md"

  if [[ ! -f "$skill_md" ]]; then
    return
  fi

  if [[ -L "$dest_file" ]]; then
    if [[ "$(readlink "$dest_file")" == "$skill_md" ]]; then
      ((skipped++)) || true
      return
    fi
    rm "$dest_file"
  elif [[ -f "$dest_file" ]]; then
    echo "  ⚠️  Skipping $name — real file exists at $dest_file"
    ((skipped++)) || true
    return
  fi

  if $DRY_RUN; then
    echo "  [dry-run] ln -s $skill_md → $dest_file"
  else
    mkdir -p "$CLAUDE_COMMANDS"
    ln -s "$skill_md" "$dest_file"
  fi
  ((installed++)) || true
}

install_category() {
  local category="$1"
  local category_dir="$SKILLS_DIR/$category"

  if [[ ! -d "$category_dir" ]]; then
    return
  fi

  for skill_dir in "$category_dir"/*/; do
    [[ -d "$skill_dir" ]] || continue
    skill_dir="${skill_dir%/}"

    if $INSTALL_CODEX; then
      link_skill_dir "$skill_dir" "$CODEX_SKILLS"
    fi
    if $INSTALL_ANTIGRAVITY; then
      link_skill_dir "$skill_dir" "$ANTIGRAVITY_SKILLS"
    fi
    if $INSTALL_CLAUDE; then
      link_skill_claude "$skill_dir"
    fi
  done
}

# ── Install ─────────────────────────────────────────────────
echo "🚀 Installing AI Agent Skills..."
echo ""

if $DRY_RUN; then
  echo "   (dry run — no changes will be made)"
  echo ""
fi

agents=()
$INSTALL_CODEX && agents+=("Codex")
$INSTALL_CLAUDE && agents+=("Claude")
$INSTALL_ANTIGRAVITY && agents+=("Antigravity")
echo "   Agents: ${agents[*]}"

categories=("portable")
if ! $PORTABLE_ONLY; then
  categories+=("tools" "integrations")
fi
echo "   Categories: ${categories[*]}"
echo ""

for cat in "${categories[@]}"; do
  echo "📦 Installing $cat skills..."
  install_category "$cat"
done

echo ""
echo "✅ Done! Installed: $installed | Already present: $skipped"
if $DRY_RUN; then
  echo "   (dry run — re-run without --dry-run to apply)"
fi
