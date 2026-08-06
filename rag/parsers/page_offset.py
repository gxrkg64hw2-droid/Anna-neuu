"""Detect printed-page-number offset in PDFs.

Returns (offset, confidence). offset = pdf_page_index - printed_page.
"""
from __future__ import annotations

import re

# Patterns that indicate "this page is the start of printed page 1"
CHAPTER_ONE_PATTERNS = [
    re.compile(r"\b1\s+Introduction\b", re.IGNORECASE),
    re.compile(r"\bChapter\s+1\b", re.IGNORECASE),
    re.compile(r"\bKapitel\s+1\b", re.IGNORECASE),
    re.compile(r"^1\s*$", re.MULTILINE),
    re.compile(r"^\s*1\s+[A-ZAOUÄÖÜ]", re.MULTILINE),  # includes German Umlaute
]

# Frontmatter signals that increase confidence the offset is real
FRONTMATTER_PATTERNS = [
    re.compile(r"\b(table of contents|inhaltsverzeichnis|inhalt)\b", re.IGNORECASE),
    re.compile(r"\b(preface|vorwort|abstract|abstrakt)\b", re.IGNORECASE),
    re.compile(r"\b(acknowledg(e?ments?)?|danksagung)\b", re.IGNORECASE),
    re.compile(r"\b(copyright|isbn)\b", re.IGNORECASE),
]


def detect_print_offset(pages: list[str], scan_pages: int = 30) -> tuple[int, float]:
    """Return (offset, confidence in [0, 1])."""
    if not pages:
        return 0, 1.0

    scan = pages[:scan_pages]
    chapter_one_pdf_page: int | None = None
    frontmatter_hits = 0

    for i, text in enumerate(scan, start=1):
        if chapter_one_pdf_page is None:
            for pat in CHAPTER_ONE_PATTERNS:
                if pat.search(text):
                    chapter_one_pdf_page = i
                    break
        if chapter_one_pdf_page is None:
            for pat in FRONTMATTER_PATTERNS:
                if pat.search(text):
                    frontmatter_hits += 1
                    break

    if chapter_one_pdf_page is None:
        return 0, 0.5  # no marker found, treat as no offset, low confidence

    offset = chapter_one_pdf_page - 1
    if offset == 0:
        return 0, 1.0

    # Confidence rises with frontmatter presence and offset plausibility
    base = 0.6
    if frontmatter_hits >= 2:
        base += 0.25
    elif frontmatter_hits == 1:
        base += 0.15
    if 1 <= offset <= 50:
        base += 0.05
    return offset, min(1.0, base)
