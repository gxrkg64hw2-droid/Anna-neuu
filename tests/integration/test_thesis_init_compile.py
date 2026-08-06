"""End-to-end test: `thesis init` -> `latexmk -lualatex` produces a non-empty PDF."""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def _has_lualatex() -> bool:
    return shutil.which("lualatex") is not None and shutil.which("latexmk") is not None


@pytest.mark.skipif(not _has_lualatex(), reason="lualatex/latexmk not on PATH")
def test_init_then_compile_produces_pdf(tmp_path, monkeypatch):
    # Run thesis init in a copied workspace to avoid polluting the real thesen/
    workspace = tmp_path / "workspace"
    shutil.copytree(REPO, workspace, ignore=shutil.ignore_patterns(
        ".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache",
        "thesen/fabian-rag-chatbot", "thesen/lisa-*", "thesen/test*",
    ))
    monkeypatch.chdir(workspace)
    result = subprocess.run(
        [sys.executable, "-m", "rag", "thesis", "init",
         "--name", "smoke", "--template", "technisch-informatik", "--mode", "lean"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, f"thesis init failed: {result.stderr}"

    tex_dir = workspace / "thesen" / "smoke" / "tex"
    assert (tex_dir / "main.tex").exists()
    assert (tex_dir / "_common" / "preamble.tex").exists()
    assert (tex_dir / "kapitel" / "01-einleitung.tex").exists()

    compile_result = subprocess.run(
        ["latexmk", "-lualatex", "-interaction=nonstopmode", "main.tex"],
        cwd=tex_dir, capture_output=True, text=True, check=False, timeout=180,
    )
    pdf = tex_dir / "main.pdf"
    assert pdf.exists() and pdf.stat().st_size > 1000, (
        f"PDF missing or too small. stdout:\n{compile_result.stdout[-2000:]}\n"
        f"stderr:\n{compile_result.stderr[-2000:]}"
    )
