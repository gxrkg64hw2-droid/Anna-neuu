"""BM25 wrapper using bm25s. ~500x faster than rank-bm25.

Saves to <index_dir>/bm25.npz + bm25_meta.json.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import bm25s
import Stemmer


@dataclass
class BM25Index:
    retriever: bm25s.BM25
    chunk_ids: list[int]
    language: str


def _stemmer_for(language: str):
    if language in ("english", "german"):
        return Stemmer.Stemmer(language)
    return None


def build_bm25_index(
    chunk_ids: list[int], texts: list[str], language: str = "english"
) -> BM25Index:
    if len(chunk_ids) != len(texts):
        raise ValueError("chunk_ids and texts must align")
    stemmer = _stemmer_for(language)
    tokens = bm25s.tokenize(texts, stopwords=language, stemmer=stemmer)
    retriever = bm25s.BM25()
    retriever.index(tokens)
    return BM25Index(retriever=retriever, chunk_ids=list(chunk_ids), language=language)


def save_index(idx: BM25Index, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    idx.retriever.save(str(dest_dir / "bm25"))
    (dest_dir / "bm25_meta.json").write_text(
        json.dumps({"chunk_ids": idx.chunk_ids, "language": idx.language})
    )


def load_index(src_dir: Path) -> BM25Index:
    retriever = bm25s.BM25.load(str(src_dir / "bm25"))
    meta = json.loads((src_dir / "bm25_meta.json").read_text())
    return BM25Index(retriever=retriever, chunk_ids=meta["chunk_ids"], language=meta["language"])


def query_bm25(idx: BM25Index, query: str, top_k: int = 50) -> list[tuple[int, float]]:
    stemmer = _stemmer_for(idx.language)
    q_tokens = bm25s.tokenize([query], stopwords=idx.language, stemmer=stemmer)
    docs, scores = idx.retriever.retrieve(q_tokens, k=min(top_k, len(idx.chunk_ids)))
    out: list[tuple[int, float]] = []
    for doc_idx, score in zip(docs[0], scores[0]):
        out.append((idx.chunk_ids[int(doc_idx)], float(score)))
    return out
