"""OCR fallback using ocrmypdf (Tesseract under the hood).

Triggered when page quality is low. Re-OCRs only the affected pages.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def needs_ocr(page_qualities: list[float], threshold: float = 0.4) -> list[int]:
    """Return 1-indexed page numbers whose quality is below threshold."""
    return [i for i, q in enumerate(page_qualities, start=1) if q < threshold]


def run_ocr_on_pdf(
    input_pdf: Path,
    output_pdf: Path,
    pages_to_ocr: list[int],
    languages: str = "deu+eng",
) -> dict:
    """Run ocrmypdf on the specified pages. Returns metadata dict."""
    if not pages_to_ocr:
        return {"ocred_pages": [], "skipped": True}

    if shutil.which("ocrmypdf") is None:
        raise RuntimeError(
            "ocrmypdf not found. Install via: brew install ocrmypdf tesseract tesseract-lang"
        )

    pages_arg = ",".join(str(p) for p in pages_to_ocr)
    cmd = [
        "ocrmypdf",
        "--language", languages,
        "--pages", pages_arg,
        "--output-type", "pdf",
        "--skip-text",
        str(input_pdf),
        str(output_pdf),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ocrmypdf failed: {result.stderr}")
    return {"ocred_pages": pages_to_ocr, "skipped": False}
