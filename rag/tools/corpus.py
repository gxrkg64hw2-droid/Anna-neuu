"""Corpus inventory: list indexed sources, page counts, quality flags."""
from __future__ import annotations

import argparse
import sqlite3
import sys

from rag.cli import emit_json
from rag.config import load_config


def run_corpus(args: argparse.Namespace) -> int:
    cfg = load_config()
    db = cfg.thesis_corpus_db(args.thesis)
    if not db.exists():
        sys.stderr.write(f"No index for thesis '{args.thesis}'. "
                         f"Run: python -m rag index --thesis {args.thesis}\n")
        return 2
    conn = sqlite3.connect(str(db))
    rows = conn.execute(
        """SELECT s.source_id, s.filename, s.bibkey, s.title, s.year,
                  s.page_count_pdf, s.page_count_printed, s.print_offset,
                  s.print_offset_confidence,
                  (SELECT COUNT(*) FROM chunks WHERE source_id=s.source_id) AS chunk_count,
                  (SELECT AVG(quality_score) FROM pages WHERE source_id=s.source_id) AS avg_quality
           FROM sources s ORDER BY s.filename"""
    ).fetchall()
    conn.close()

    sources = []
    for r in rows:
        sources.append({
            "source_id": r[0], "filename": r[1], "bibkey": r[2], "title": r[3], "year": r[4],
            "page_count_pdf": r[5], "page_count_printed": r[6],
            "print_offset": r[7], "print_offset_confidence": r[8],
            "chunk_count": r[9],
            "avg_quality": round(r[10], 3) if r[10] is not None else None,
        })
    result = {"thesis": args.thesis, "total_sources": len(sources), "sources": sources}
    if args.pretty:
        from rag.tools.format import render_corpus_pretty
        render_corpus_pretty(result)
        return 0
    emit_json(result)
    return 0
