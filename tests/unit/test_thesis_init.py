"""Unit tests for `python -m rag thesis init`."""

import pytest


def test_slug_validation_rejects_invalid():
    from rag.thesis.init import SlugError, validate_slug
    invalid = ["", "with space", "UPPERCASE", "trail-", "-lead", "double--dash", "ünicode"]
    for s in invalid:
        with pytest.raises(SlugError):
            validate_slug(s)


def test_slug_validation_accepts_valid():
    from rag.thesis.init import validate_slug
    for s in ["fabian", "fabian-rag-chatbot", "lisa-konsumenten", "a-b-c", "ba2026"]:
        validate_slug(s)  # no exception


def test_init_thesis_creates_expected_files(tmp_path):
    """init_thesis copies _template + chosen LaTeX profile, patches CLAUDE.md."""
    from rag.thesis.init import init_thesis
    repo_root = tmp_path / "repo"
    (repo_root / "thesen" / "_template").mkdir(parents=True)
    (repo_root / "thesen" / "_template" / "CLAUDE.md").write_text(
        "# CLAUDE.md (Thesis Brief)\n\n"
        "## Mode\n\n- [ ] **Premium**\n- [ ] **Lean**\n\n"
        "## Thesis topic\n\n<your-name>\n"
    )
    (repo_root / "thesen" / "_template" / "pdfs").mkdir()
    (repo_root / "thesen" / "_template" / "tex").mkdir()
    (repo_root / "thesen" / "_template" / "bibliography.bib").write_text("")
    (repo_root / "thesen" / "_template" / "overrides.toml").write_text("")
    (repo_root / "templates" / "latex" / "_common").mkdir(parents=True)
    (repo_root / "templates" / "latex" / "_common" / "preamble.tex").write_text("% preamble")
    profile_root = repo_root / "templates" / "latex" / "technisch-informatik"
    (profile_root / "kapitel").mkdir(parents=True)
    (profile_root / "main.tex").write_text("% main")
    (profile_root / "kapitel" / "01-einleitung.tex").write_text("% intro")

    result = init_thesis(
        slug="testname",
        template="technisch-informatik",
        mode="premium",
        repo_root=repo_root,
    )

    thesis_dir = repo_root / "thesen" / "testname"
    assert thesis_dir.exists()
    assert (thesis_dir / "tex" / "main.tex").exists()
    # _common/ must be a child of tex/ so relative \input{_common/...} resolves
    assert (thesis_dir / "tex" / "_common" / "preamble.tex").exists()
    assert (thesis_dir / "tex" / "kapitel" / "01-einleitung.tex").exists()
    assert (thesis_dir / "pdfs").exists()
    assert (thesis_dir / "bibliography.bib").exists()
    assert (thesis_dir / "overrides.toml").exists()
    claude_md = (thesis_dir / "CLAUDE.md").read_text()
    assert "testname" in claude_md
    assert "technisch-informatik" in claude_md
    # Premium mode marker
    assert "[x] **Premium**" in claude_md
    assert isinstance(result, dict)
    assert result["thesis"] == "testname"
    assert result["template"] == "technisch-informatik"
    assert result["mode"] == "premium"


def test_init_thesis_refuses_existing_folder(tmp_path):
    from rag.thesis.init import SlugError, init_thesis
    repo_root = tmp_path / "repo"
    (repo_root / "thesen" / "existing").mkdir(parents=True)
    (repo_root / "thesen" / "_template").mkdir()
    (repo_root / "templates" / "latex" / "_common").mkdir(parents=True)
    (repo_root / "templates" / "latex" / "technisch-informatik").mkdir(parents=True)
    with pytest.raises(SlugError):
        init_thesis(
            slug="existing", template="technisch-informatik",
            mode="lean", repo_root=repo_root,
        )


def test_init_thesis_refuses_unknown_template(tmp_path):
    from rag.thesis.init import SlugError, init_thesis
    repo_root = tmp_path / "repo"
    (repo_root / "thesen" / "_template").mkdir(parents=True)
    (repo_root / "templates" / "latex" / "_common").mkdir(parents=True)
    with pytest.raises(SlugError):
        init_thesis(slug="t", template="does-not-exist", mode="lean", repo_root=repo_root)
