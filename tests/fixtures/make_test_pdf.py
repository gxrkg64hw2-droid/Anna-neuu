"""Build small test PDFs on demand using PyMuPDF's own writer."""
from __future__ import annotations

from pathlib import Path

import pymupdf


def build_simple_pdf(path: Path, pages: list[str]) -> None:
    doc = pymupdf.open()
    for text in pages:
        page = doc.new_page()
        page.insert_text((72, 72), text, fontsize=11)
    doc.save(str(path))
    doc.close()
