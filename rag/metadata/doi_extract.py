"""Extract DOIs from PDF text. Returns the first real match or None.

Filters out placeholder DOIs commonly left in submitted-but-unpublished templates
(e.g. ``10.1145/nnnnnnn.nnnnnnn`` from ACM templates, or sequences of repeated
single characters like ``xxxx`` or ``yyyy``).
"""
from __future__ import annotations

import re

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
PLACEHOLDER_RUN = re.compile(r"([a-zA-Z])\1{3,}", re.IGNORECASE)


def _is_placeholder(doi: str) -> bool:
    """Detect template placeholder DOIs that contain runs of repeated letters."""
    return bool(PLACEHOLDER_RUN.search(doi))


def extract_doi_from_text(text: str) -> str | None:
    """Return the first non-placeholder DOI, or None."""
    for m in DOI_RE.finditer(text):
        doi = m.group(0).rstrip(".,;)")
        if not _is_placeholder(doi):
            return doi
    return None
