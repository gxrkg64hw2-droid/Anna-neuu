"""Hybrid retrieval over a thesis corpus."""
from __future__ import annotations

import argparse
import json
import sqlite3
import struct
import sys
import time
from pathlib import Path

import sqlite_vec

from rag.cli import emit_json
from rag.config import Config, load_config
from rag.indexer.bm25 import load_index, query_bm25
from rag.indexer.embeddings import EmbeddingClient
from rag.search.fusion import reciprocal_rank_fusion


def _open_db(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def _vec_blob(values: list[float]) -> bytes:
    return struct.pack(f"{len(values)}f", *values)


def _dense_search(
    conn: sqlite3.Connection, query_vec: list[float], top: int
) -> list[tuple[int, float]]:
    rows = conn.execute(
        """SELECT chunk_id, distance FROM vec_chunks
           WHERE embedding MATCH ? AND k=?
           ORDER BY distance""",
        (_vec_blob(query_vec), top),
    ).fetchall()
    return [(int(cid), 1.0 / (1.0 + float(d))) for cid, d in rows]


def _expand_context(conn: sqlite3.Connection, chunk_id: int, window: int) -> tuple[str, str]:
    row = conn.execute(
        """SELECT source_id, pdf_page_start, pdf_page_end FROM chunks WHERE chunk_id=?""",
        (chunk_id,),
    ).fetchone()
    if not row:
        return "", ""
    source_id, p_start, p_end = row
    before_row = conn.execute(
        "SELECT text FROM pages WHERE source_id=? AND pdf_page=?",
        (source_id, max(1, p_start - 1)),
    ).fetchone()
    after_row = conn.execute(
        "SELECT text FROM pages WHERE source_id=? AND pdf_page=?",
        (source_id, p_end + 1),
    ).fetchone()
    before = (before_row[0] if before_row else "")[-300:]
    after = (after_row[0] if after_row else "")[:300]
    return before, after


def search_corpus(
    cfg: Config, thesis: str, *, query: str,
    top: int = 8, window: int = 5, mode: str = "auto",
    filter_source: str | None = None, filter_year: str | None = None,
    rerank: bool = False,
) -> dict:
    db_path = cfg.thesis_corpus_db(thesis)
    if not db_path.exists():
        raise FileNotFoundError(f"No index found. Run: python -m rag index --thesis {thesis}")
    t0 = time.time()
    conn = _open_db(db_path)

    # Dense
    dense_hits: list[tuple[int, float]] = []
    if mode in ("auto", "dense"):
        client = EmbeddingClient(api_key=cfg.openrouter_api_key, model=cfg.embedding_model)
        qv = client.embed_batch([query])[0]
        dense_hits = _dense_search(conn, qv, top=50)

    # Sparse
    sparse_hits: list[tuple[int, float]] = []
    if mode in ("auto", "bm25"):
        bm25_idx = load_index(cfg.thesis_index_dir(thesis))
        sparse_hits = query_bm25(bm25_idx, query, top_k=50)

    rankings = [r for r in (dense_hits, sparse_hits) if r]
    fused = reciprocal_rank_fusion(rankings, top_k=30) if rankings else []

    # Optional rerank
    score_rerank_map: dict[int, float] = {}
    if rerank and fused:
        from rag.search.rerank import rerank_pairs
        candidate_ids = [cid for cid, _ in fused]
        candidate_texts = []
        for cid in candidate_ids:
            row = conn.execute("SELECT text FROM chunks WHERE chunk_id=?", (cid,)).fetchone()
            candidate_texts.append(row[0] if row else "")
        scored = rerank_pairs(query, candidate_texts)
        score_rerank_map = {candidate_ids[i]: s for i, s in enumerate(scored)}
        fused = sorted(fused, key=lambda x: score_rerank_map.get(x[0], 0.0), reverse=True)

    # Filter-before-top-k: apply source/year filters on the full fused list so that
    # the requested top-k count reflects only matching results (not skipped rows).
    filtered_fused: list[tuple[int, float]] = []
    for cid, fused_score in fused:
        chunk_row_filter = conn.execute(
            "SELECT source_id FROM chunks WHERE chunk_id=?", (cid,)
        ).fetchone()
        if not chunk_row_filter:
            continue
        src_row_filter = conn.execute(
            "SELECT bibkey, year FROM sources WHERE source_id=?", (chunk_row_filter[0],)
        ).fetchone()
        bibkey_f = src_row_filter[0] if src_row_filter else None
        year_f = src_row_filter[1] if src_row_filter else None
        if filter_source and bibkey_f != filter_source:
            continue
        if filter_year and year_f is not None:
            try:
                if filter_year.startswith("<") and not year_f < int(filter_year[1:]):
                    continue
                if filter_year.startswith(">") and not year_f > int(filter_year[1:]):
                    continue
                is_range = (
                    "-" in filter_year
                    and not filter_year.startswith("<")
                    and not filter_year.startswith(">")
                )
                if is_range:
                    lo, hi = (int(x) for x in filter_year.split("-"))
                    if not (lo <= year_f <= hi):
                        continue
            except ValueError:
                pass
        filtered_fused.append((cid, fused_score))
        if len(filtered_fused) >= top:
            break

    # Build hits
    hits: list[dict] = []
    dense_score_map = dict(dense_hits)
    sparse_score_map = dict(sparse_hits)
    for rank_idx, (cid, fused_score) in enumerate(filtered_fused[:top], start=1):
        chunk_row = conn.execute(
            """SELECT c.source_id, c.text, c.token_count,
                      c.pdf_page_start, c.pdf_page_end,
                      c.printed_page_start, c.printed_page_end,
                      c.quality_score, c.ocr_origin
               FROM chunks c WHERE c.chunk_id=?""", (cid,),
        ).fetchone()
        if not chunk_row:
            continue
        source_id, text, _tok, ps, pe, pps, ppe, qs, ocr = chunk_row
        src_row = conn.execute(
            """SELECT bibkey, title, authors, year, filename, print_offset_confidence
               FROM sources WHERE source_id=?""", (source_id,),
        ).fetchone()
        bibkey, title, authors_json, year, filename, conf = (
            src_row or (None, None, "[]", None, "?.pdf", 1.0)
        )
        authors = json.loads(authors_json or "[]")

        before, after = _expand_context(conn, cid, window)
        cite = f"\\parencite[S. {pps}]{{{bibkey}}}" if (bibkey and pps) else None
        hits.append({
            "rank": rank_idx,
            "score_fused": round(fused_score, 4),
            "score_dense": round(dense_score_map.get(cid, 0.0), 4),
            "score_bm25": round(sparse_score_map.get(cid, 0.0), 4),
            "score_rerank": round(score_rerank_map[cid], 4) if cid in score_rerank_map else None,
            "source": {
                "bibkey": bibkey, "title": title, "authors": authors,
                "year": year, "filename": filename,
            },
            "location": {
                "pdf_page_start": ps, "pdf_page_end": pe,
                "printed_page_start": pps, "printed_page_end": ppe,
                "print_offset_confidence": conf,
            },
            "quality_score": round(qs, 3),
            "ocr_origin": {0: "native", 1: "tesseract", 2: "vision"}[ocr],
            "chunk_text": text,
            "context_before": before,
            "context_after": after,
            "citation_suggestion": cite,
        })

    conn.close()
    return {
        "query": query,
        "thesis": thesis,
        "mode": mode,
        "reranked": rerank,
        "total_hits": len(hits),
        "hits": hits,
        "duration_ms": int((time.time() - t0) * 1000),
    }


def run_search(args: argparse.Namespace) -> int:
    cfg = load_config()
    try:
        result = search_corpus(
            cfg, args.thesis, query=args.query, top=args.top, window=args.window,
            mode=args.mode, filter_source=args.filter_source,
            filter_year=args.filter_year, rerank=args.rerank,
        )
    except FileNotFoundError as e:
        sys.stderr.write(f"{e}\n")
        return 2
    if args.pretty:
        from rag.search.format import render_search_pretty
        render_search_pretty(result)
        return 0
    emit_json(result)
    return 0
