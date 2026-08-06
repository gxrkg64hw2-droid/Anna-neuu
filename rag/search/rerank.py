"""Cross-encoder reranker stage using bge-reranker-v2-m3.

Lazy-loads the model on first use. Cached on disk by sentence-transformers.
"""
from __future__ import annotations

_MODEL = None


def _get_model():
    global _MODEL
    if _MODEL is None:
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as exc:
            raise RuntimeError(
                "Reranker requires the 'rerank' extra. Install with: uv sync --extra rerank"
            ) from exc
        _MODEL = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=512)
    return _MODEL


def rerank_pairs(query: str, candidates: list[str]) -> list[float]:
    model = _get_model()
    pairs = [[query, c] for c in candidates]
    scores = model.predict(pairs)
    return [float(s) for s in scores]
