#!/usr/bin/env bash
# tools/skills-sync.sh
#
# Vendors ten K-Dense scientific skills into .claude/skills/ at a pinned commit,
# applies mechanical patches (em/en-dash replacement, Schematics-block strip,
# bilingual frontmatter rewrite), and overlays DACH-specific reference files +
# DEUTSCHE-KONVENTIONEN.md per skill. Idempotent.
#
# Usage:
#   ./tools/skills-sync.sh            # sync at PINNED_COMMIT
#   ./tools/skills-sync.sh --dry-run  # show what would change
set -euo pipefail

PINNED_COMMIT="37a148ba51810e930f89551b5485c331f42171ca"
UPSTREAM_REPO="https://github.com/K-Dense-AI/claude-scientific-skills.git"
UPSTREAM_SKILLS_PATH="scientific-skills"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/.claude/skills"
OVERLAY_DIR="$REPO_ROOT/tools/skills-overlay"
LOG_FILE="$REPO_ROOT/tools/skills-sync.log"

TARGET_SKILLS=(
  scientific-writing
  scientific-critical-thinking
  literature-review
  hypothesis-generation
  statistical-analysis
  market-research-reports
  scientific-visualization
  scholar-evaluation
  scientific-brainstorming
  peer-review
)

log() { echo "[$1] $2" | tee -a "$LOG_FILE"; }

TMP_DIR=""

cleanup() { [[ -n "$TMP_DIR" ]] && rm -rf "$TMP_DIR"; }
trap cleanup EXIT

main() {
  : > "$LOG_FILE"
  log INFO "skills-sync starting at $(date -Iseconds)"
  log INFO "pinned commit: $PINNED_COMMIT"

  TMP_DIR="$(mktemp -d)"

  log INFO "cloning $UPSTREAM_REPO into $TMP_DIR/upstream"
  git clone --quiet "$UPSTREAM_REPO" "$TMP_DIR/upstream"
  git -C "$TMP_DIR/upstream" checkout --quiet "$PINNED_COMMIT"

  mkdir -p "$SKILLS_DIR"

  for skill in "${TARGET_SKILLS[@]}"; do
    sync_skill "$TMP_DIR/upstream/$UPSTREAM_SKILLS_PATH/$skill" "$skill"
  done

  log INFO "skills-sync done"
}

strip_schematics() {
  local file="$1"
  # Pass 1: Remove any H2 section whose heading starts with "## Visual Enhancement"
  # (covers both "## Visual Enhancement with Scientific Schematics" and
  # "## Visual Enhancement Requirements" variants). State machine: skip lines
  # from the matching H2 until the next H2 or EOF.
  awk '
    BEGIN { skip = 0 }
    /^## Visual Enhancement/ { skip = 1; next }
    /^## / && skip == 1 { skip = 0 }
    skip == 0 { print }
  ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"

  # Pass 2: Strip residual inline references to the Schematics API that survive
  # outside the H2 block (e.g. YAML frontmatter, bullet lists, table cells).
  # Each perl call rewrites only lines containing the target phrase.
  local patterns=(
    's/ with scientific-schematics and generate-image,? *//g'
    's/ *scientific-schematics and generate-image,? *//g'
    's/scientific-schematics//g'
    's/generate_schematic_ai\.py//g'
    's/generate_schematic\.py//g'
    's/generate_image\.py//g'
    's/Nano Banana//g'
  )
  for pat in "${patterns[@]}"; do
    perl -i -pe "$pat" "$file"
  done
}

patch_dashes() {
  local dir="$1"
  # Em-dash (U+2014): replace with ". " when surrounded by spaces, else ", "
  # En-dash (U+2013): replace with "-" (hyphen-minus) for ranges/compounds
  while IFS= read -r -d '' f; do
    local before
    before="$(perl -CSD -ne 'BEGIN{$/=undef} print scalar(()=/[\x{2013}\x{2014}]/g)' "$f" 2>/dev/null || echo 0)"
    # Em-dash with spaces both sides -> ". "
    perl -i -CSD -pe 's/ \x{2014} /. /g' "$f"
    # Em-dash anywhere remaining -> ", "
    perl -i -CSD -pe 's/\x{2014}/, /g' "$f"
    # En-dash -> hyphen
    perl -i -CSD -pe 's/\x{2013}/-/g' "$f"
    if [[ -n "$before" && "$before" != "0" ]]; then
      log INFO "  patch_dashes $(basename "$f"): replaced $before dashes"
    fi
  done < <(find "$dir" -type f \( -name "*.md" -o -name "*.txt" \) -print0)
}

rewrite_frontmatter() {
  local skill_md="$1"
  local name="$2"
  local de_file="$OVERLAY_DIR/$name/description.de.txt"
  local en_file="$OVERLAY_DIR/$name/description.en.txt"

  if [[ ! -f "$de_file" || ! -f "$en_file" ]]; then
    log WARN "  no bilingual description for $name (de=$de_file, en=$en_file)"
    return
  fi

  local de en
  de="$(tr '\n' ' ' < "$de_file" | sed 's/  */ /g; s/ *$//')"
  en="$(tr '\n' ' ' < "$en_file" | sed 's/  */ /g; s/ *$//')"

  python3 - "$skill_md" "$de" "$en" <<'PY'
import sys, re, pathlib
path = pathlib.Path(sys.argv[1])
de = sys.argv[2]
en = sys.argv[3]
text = path.read_text(encoding="utf-8")
new = "description: |\n  DE: " + de + "\n  EN: " + en
patched, n = re.subn(r"(?m)^description:[ \t]+.+$", new, text, count=1)
if n == 0:
    sys.exit(0)
path.write_text(patched, encoding="utf-8")
PY
  log INFO "  bilingual frontmatter applied to $name"
}

triage_scripts() {
  local dst="$1"
  local strip=(
    generate_schematic.py
    generate_schematic_ai.py
    generate_image.py
    search_databases.py
    verify_citations.py
    generate_pdf.py
  )
  for s in "${strip[@]}"; do
    if [[ -f "$dst/scripts/$s" ]]; then
      rm "$dst/scripts/$s"
      log STRIP "  $s"
    fi
  done
}

apply_overlay() {
  local name="$1"
  local dst="$SKILLS_DIR/$name"
  local src="$OVERLAY_DIR/$name"

  if [[ ! -d "$src" ]]; then
    return
  fi

  # Top-level: DEUTSCHE-KONVENTIONEN.md
  if [[ -f "$src/DEUTSCHE-KONVENTIONEN.md" ]]; then
    cp "$src/DEUTSCHE-KONVENTIONEN.md" "$dst/DEUTSCHE-KONVENTIONEN.md"
    log OVERLAY "  $name/DEUTSCHE-KONVENTIONEN.md"
  fi

  # references/*.md replacements (overwrite upstream files of same name)
  if [[ -d "$src/references" ]]; then
    mkdir -p "$dst/references"
    while IFS= read -r -d '' f; do
      local rel
      rel="${f#$src/references/}"
      cp "$f" "$dst/references/$rel"
      log OVERLAY "  $name/references/$rel"
    done < <(find "$src/references" -type f -print0)
  fi
}

sync_skill() {
  local src="$1"
  local name="$2"
  local dst="$SKILLS_DIR/$name"

  if [[ ! -d "$src" ]]; then
    log WARN "upstream skill not found: $name (skipping)"
    return
  fi

  log INFO "sync $name"
  rm -rf "$dst"
  mkdir -p "$dst"

  cp "$src/SKILL.md" "$dst/SKILL.md"
  if [[ -d "$src/references" ]]; then cp -r "$src/references" "$dst/"; fi
  if [[ -d "$src/scripts" ]];    then cp -r "$src/scripts"    "$dst/"; fi

  strip_schematics "$dst/SKILL.md"
  patch_dashes "$dst"
  rewrite_frontmatter "$dst/SKILL.md" "$name"
  triage_scripts "$dst"
  apply_overlay "$name"
}

main "$@"
