"""Lightweight sentence splitter for .tex files. Strips comments and commands."""
from __future__ import annotations

import re
from pathlib import Path

CMD_RE = re.compile(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?")
COMMENT_RE = re.compile(r"(?<!\\)%.*$", re.MULTILINE)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def iter_sentences(path: Path):
    text = path.read_text()
    text = COMMENT_RE.sub("", text)
    text = CMD_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for s in SENTENCE_RE.split(text):
        s = s.strip()
        if len(s) > 20:
            yield s
