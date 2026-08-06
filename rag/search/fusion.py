"""Reciprocal Rank Fusion for combining dense and sparse retrieval rankings."""
from __future__ import annotations


def reciprocal_rank_fusion(
    rankings: list[list[tuple[int, float]]], top_k: int = 30, k: int = 60
) -> list[tuple[int, float]]:
    """Standard RRF: score = sum(1 / (k + rank_i)). 1-indexed ranks."""
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, (item_id, _orig_score) in enumerate(ranking, start=1):
            scores[item_id] = scores.get(item_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
