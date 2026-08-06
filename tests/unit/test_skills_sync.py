"""Tests for tools/skills-sync.sh.

The sync script is idempotent: running it twice produces no diff. It clones a
pinned K-Dense commit, vendors ten target skills into .claude/skills/, applies
mechanical patches (Schematics strip, em-dash replacement, bilingual frontmatter),
and overlays DACH-specific reference files plus DEUTSCHE-KONVENTIONEN.md per skill.
"""
import os
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "skills-sync.sh"


def test_script_exists_and_is_executable():
    assert SCRIPT.exists(), "tools/skills-sync.sh must exist"
    assert os.access(SCRIPT, os.X_OK), "tools/skills-sync.sh must be executable"


def test_script_has_pinned_commit_variable():
    text = SCRIPT.read_text()
    assert "PINNED_COMMIT=" in text, "script must declare PINNED_COMMIT"
    import re
    m = re.search(r'PINNED_COMMIT="([0-9a-f]{40})"', text)
    assert m, "PINNED_COMMIT must be a 40-char SHA"


def test_script_targets_ten_skills():
    text = SCRIPT.read_text()
    expected = [
        "scientific-writing", "scientific-critical-thinking", "literature-review",
        "hypothesis-generation", "statistical-analysis", "market-research-reports",
        "scientific-visualization", "scholar-evaluation", "scientific-brainstorming",
        "peer-review",
    ]
    for s in expected:
        assert s in text, f"target skill {s} missing from script"


def test_no_em_dashes_after_sync():
    """User CLAUDE.md forbids em (—) and en (–) dashes anywhere."""
    skills_dir = REPO / ".claude" / "skills"
    if not skills_dir.exists():
        pytest.skip("run skills-sync.sh first")
    forbidden = []
    for md in skills_dir.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for ch, name in (("—", "em-dash"), ("–", "en-dash")):
            if ch in text:
                forbidden.append(f"{md.relative_to(REPO)}: contains {name}")
    assert not forbidden, "\n".join(forbidden)


def test_no_schematics_block_after_sync():
    """The K-Dense Schematics promo block uses proprietary Nano Banana 2 API and
    must be stripped from every vendored SKILL.md."""
    skills_dir = REPO / ".claude" / "skills"
    if not skills_dir.exists():
        pytest.skip("run skills-sync.sh first")
    leaked = []
    for skill_md in skills_dir.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        forbidden_phrases = [
            "Visual Enhancement with Scientific Schematics",
            "scientific-schematics",
            "generate_schematic.py",
            "generate_schematic_ai.py",
            "generate_image.py",
            "Nano Banana",
        ]
        for phrase in forbidden_phrases:
            if phrase in text:
                leaked.append(f"{skill_md.relative_to(REPO)}: contains '{phrase}'")
    assert not leaked, "\n".join(leaked)


def test_bilingual_frontmatter_after_sync():
    """Each vendored SKILL.md must have a bilingual description: 'DE: ...; EN: ...'"""
    skills_dir = REPO / ".claude" / "skills"
    if not skills_dir.exists():
        pytest.skip("run skills-sync.sh first")
    for skill_md in skills_dir.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        assert ("DE:" in text and "EN:" in text), (
            f"{skill_md.relative_to(REPO)}: frontmatter description not bilingual"
        )


def test_no_proprietary_scripts_after_sync():
    skills_dir = REPO / ".claude" / "skills"
    if not skills_dir.exists():
        pytest.skip("run skills-sync.sh first")
    forbidden = ["generate_schematic.py", "generate_schematic_ai.py", "generate_image.py",
                 "search_databases.py", "verify_citations.py", "generate_pdf.py"]
    leaks = []
    for f in skills_dir.rglob("*.py"):
        if f.name in forbidden:
            leaks.append(str(f.relative_to(REPO)))
    assert not leaks, "stripped scripts present: " + ", ".join(leaks)


def test_overlay_files_copied_when_present():
    """If tools/skills-overlay/<name>/DEUTSCHE-KONVENTIONEN.md exists, it must end up
    in .claude/skills/<name>/DEUTSCHE-KONVENTIONEN.md after sync."""
    overlay = REPO / "tools" / "skills-overlay"
    skills_dir = REPO / ".claude" / "skills"
    if not skills_dir.exists() or not overlay.exists():
        pytest.skip("run skills-sync.sh first")
    for skill_dir in overlay.iterdir():
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name
        src = skill_dir / "DEUTSCHE-KONVENTIONEN.md"
        if src.exists():
            dst = skills_dir / name / "DEUTSCHE-KONVENTIONEN.md"
            assert dst.exists(), f"overlay not copied: {name}/DEUTSCHE-KONVENTIONEN.md"
            assert dst.read_text() == src.read_text(), f"overlay content mismatch: {name}"
