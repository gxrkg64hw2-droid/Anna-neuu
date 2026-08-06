"""Recursive 512-token chunking with sentence-aware boundaries.

Uses tiktoken for token counting. Chunks try to end at sentence boundaries (. ! ?)
within a tolerance window. Overlap is taken from the *end* of the previous chunk.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

import tiktoken

ENCODING = tiktoken.get_encoding("cl100k_base")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True)
class Chunk:
    text: str
    token_count: int
    char_start: int
    char_end: int


def _token_len(s: str) -> int:
    return len(ENCODING.encode(s))


def _split_at_sentence(text: str, target: int, tolerance: int = 50) -> tuple[str, str]:
    """Take a target-token-sized chunk, ending at a sentence boundary if possible."""
    encoded = ENCODING.encode(text)
    if len(encoded) <= target:
        return text, ""
    # Decode the target slice plus tolerance window
    upper = ENCODING.decode(encoded[: target + tolerance])
    boundaries = [m.end() for m in SENTENCE_END.finditer(upper)]
    # Pick the boundary closest to target token count
    target_chars = len(ENCODING.decode(encoded[:target]))
    best = None
    for b in boundaries:
        if b >= target_chars - 200:  # near the target
            best = b
            break
    if best is None:
        # Fallback: hard cut at target tokens
        head = ENCODING.decode(encoded[:target])
        tail = text[len(head):]
        return head, tail
    head = upper[:best]
    tail = text[best:]
    return head, tail


def chunk_text(text: str, target_tokens: int = 512, overlap_tokens: int = 80) -> list[Chunk]:
    if not text or not text.strip():
        return []
    out: list[Chunk] = []
    cursor = 0
    remaining = text
    while remaining.strip():
        head, tail = _split_at_sentence(remaining, target_tokens)
        head_stripped = head.strip()
        if not head_stripped:
            break
        char_start = cursor
        char_end = cursor + len(head)
        out.append(
            Chunk(
                text=head_stripped,
                token_count=_token_len(head_stripped),
                char_start=char_start,
                char_end=char_end,
            )
        )
        if not tail.strip():
            break
        # Overlap: take last `overlap_tokens` from head and prepend to tail
        head_encoded = ENCODING.encode(head)
        if len(head_encoded) > overlap_tokens:
            overlap_text = ENCODING.decode(head_encoded[-overlap_tokens:])
        else:
            overlap_text = head
        cursor += len(head) - len(overlap_text)
        remaining = overlap_text + tail
    return out
