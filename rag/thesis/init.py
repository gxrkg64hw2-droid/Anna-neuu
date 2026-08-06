"""Implementation of `python -m rag thesis init`."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

VALID_TEMPLATES = (
    "technisch-informatik",
    "empirisch-quantitativ",
    "theoretisch-konzeptionell",
    "marketing-case-study",
    "mixed-methods-mayring",
)


class SlugError(Exception):
    """Raised when slug or template is invalid."""


_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$", re.ASCII)


def validate_slug(slug: str) -> None:
    if not slug or not _SLUG_RE.match(slug):
        raise SlugError(
            f"slug must match [a-z0-9]+(-[a-z0-9]+)*, got: {slug!r}"
        )


def init_thesis(
    *,
    slug: str,
    template: str,
    mode: str,
    repo_root: Path,
) -> dict:
    validate_slug(slug)
    if template not in VALID_TEMPLATES:
        raise SlugError(
            f"template must be one of {VALID_TEMPLATES}, got {template!r}"
        )
    if mode not in ("premium", "lean"):
        raise SlugError(f"mode must be premium|lean, got {mode!r}")

    thesen_dir = repo_root / "thesen"
    thesis_dir = thesen_dir / slug
    if thesis_dir.exists():
        raise SlugError(f"thesis folder already exists: thesen/{slug}")

    template_src = repo_root / "thesen" / "_template"
    if not template_src.exists():
        raise SlugError(f"thesis template missing: {template_src}")

    common_src = repo_root / "templates" / "latex" / "_common"
    profile_src = repo_root / "templates" / "latex" / template
    if not common_src.exists():
        raise SlugError(f"latex common layer missing: {common_src}")
    if not profile_src.exists():
        raise SlugError(f"latex profile missing: {profile_src}")

    # 1. Copy thesen/_template -> thesen/<slug>
    shutil.copytree(template_src, thesis_dir)

    # 2. Copy templates/latex/_common -> thesen/<slug>/tex/_common
    tex_dir = thesis_dir / "tex"
    tex_dir.mkdir(exist_ok=True)
    shutil.copytree(common_src, tex_dir / "_common", dirs_exist_ok=True)

    # 3. Copy templates/latex/<template>/* -> thesen/<slug>/tex/ (overlay flat)
    created = 0
    for item in profile_src.iterdir():
        dst = tex_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dst, dirs_exist_ok=True)
            created += sum(1 for f in item.rglob("*") if f.is_file())
        else:
            shutil.copy2(item, dst)
            created += 1

    # 4. Patch thesis-level CLAUDE.md
    claude_md = thesis_dir / "CLAUDE.md"
    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8")
        text = text.replace("<your-name>", slug)
        if mode == "premium":
            text = text.replace("- [ ] **Premium**", "- [x] **Premium**", 1)
        else:
            text = text.replace("- [ ] **Lean**", "- [x] **Lean**", 1)
        # Insert profile line after first H1 if not already present
        if f"Profile: `{template}`" not in text:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("# "):
                    lines.insert(i + 1, f"\n**Profile:** `{template}`\n")
                    break
            text = "\n".join(lines)
        claude_md.write_text(text, encoding="utf-8")

    # 5. Ensure side files and directories exist
    for p in ("pdfs",):
        (thesis_dir / p).mkdir(exist_ok=True)
    for f in ("bibliography.bib", "overrides.toml"):
        path = thesis_dir / f
        if not path.exists():
            path.write_text("")

    return {
        "thesis": slug,
        "template": template,
        "mode": mode,
        "created_files": created,
        "next_steps": [
            f"Drop your PDFs into thesen/{slug}/pdfs/",
            f"If Premium mode: place your Zotero export at thesen/{slug}/bibliography.bib",
            f"Run: python -m rag index --thesis {slug}",
            f"Compile a smoke-test: cd thesen/{slug}/tex && latexmk -lualatex main.tex",
        ],
    }


def run_thesis_init(args: argparse.Namespace) -> int:
    try:
        result = init_thesis(
            slug=args.name,
            template=args.template,
            mode=args.mode,
            repo_root=Path(__file__).resolve().parents[2],
        )
    except SlugError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    indent = 2 if getattr(args, "pretty", False) else None
    print(json.dumps(result, indent=indent, ensure_ascii=False))
    return 0
