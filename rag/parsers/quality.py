"""Quality score 0..1 for an extracted page of text.

Heuristic combining: word density, alphanumeric ratio, replacement-char penalty,
sentence-boundary presence.
"""
from __future__ import annotations

import re

REPLACEMENT = "�"


def score_page(text: str) -> float:
    if not text or not text.strip():
        return 0.0
    n = len(text)
    if n < 5:
        return 0.0

    # Only count alphabetic words (2+ letters) - excludes digit-only tokens
    words = re.findall(r"\b[a-zA-Z]{2,}\b", text)
    word_count = len(words)
    word_density = min(1.0, word_count / max(1, n / 7))  # ~1 word per 7 chars is ideal

    # Alpha ratio: letters and spaces only (digits are noise in scanned text)
    alpha = sum(c.isalpha() or c.isspace() for c in text)
    alpha_ratio = alpha / n

    replacement_chars = text.count(REPLACEMENT)
    replacement_penalty = min(1.0, replacement_chars / max(1, n / 200))

    # Count sentence ends including end-of-string
    sentence_boundaries = len(re.findall(r"[.!?](?:\s|$)", text))
    sentence_score = min(1.0, sentence_boundaries / max(1, word_count / 20))

    score = (
        0.50 * word_density       # was 0.40; bumped so positive weights sum to 1.0
        + 0.30 * alpha_ratio
        + 0.20 * sentence_score
        - 0.40 * replacement_penalty
    )
    return max(0.0, min(1.0, score))
