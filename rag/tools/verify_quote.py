"""Plagiarism self-check tool.

Pipeline:
1. Embedding broad-net: top-N nearest chunks
2. Sentence-level token diff: Jaccard, LCS-ratio (best sentence within each chunk)
3. Semantic check: dense_score = 1/(1+L2) via embeddings
4. Severity classification
"""
from __future__ import annotations

import argparse
import difflib
import re
import sqlite3
import struct
import sys
from pathlib import Path

import sqlite_vec

from rag.cli import emit_json
from rag.config import Config, load_config
from rag.indexer.embeddings import EmbeddingClient

WORD = re.compile(r"\b\w+\b", re.UNICODE)
STOPWORDS = set("""the a an of and or but to in on at for from is are was were be been
                  being have has had do does did this that these those it its as by with""".split())

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _split_sentences(text: str) -> list[str]:
    """Split a chunk into sentences. Drops very short fragments."""
    return [s.strip() for s in _SENTENCE_SPLIT.split(text) if len(s.strip()) > 15]


def _tokenize(text: str) -> list[str]:
    return [w.lower() for w in WORD.findall(text) if w.lower() not in STOPWORDS and len(w) > 2]


def _jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def _lcs_ratio(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    sm = difflib.SequenceMatcher(a=a, b=b)
    return sm.ratio()


def _vec_blob(values: list[float]) -> bytes:
    return struct.pack(f"{len(values)}f", *values)


def _open_db(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def _classify(
    jaccard: float,
    lcs: float,
    dense_score: float,
    structural: float,
    t_strict: float,
    t_fuzzy: float,
) -> str:
    if jaccard >= t_strict or lcs >= t_strict:
        return "STRICT_MATCH"
    if dense_score >= t_fuzzy and structural >= 0.40:
        return "FUZZY_MATCH"
    if dense_score >= t_fuzzy:
        return "THEMATIC_MATCH"
    return "NO_MATCH"


def verify_quote(
    cfg: Config,
    thesis: str,
    *,
    text: str,
    threshold_strict: float,
    threshold_fuzzy: float,
    top: int,
) -> dict:
    db_path = cfg.thesis_corpus_db(thesis)
    if not db_path.exists():
        raise FileNotFoundError(f"No index. Run: python -m rag index --thesis {thesis}")

    client = EmbeddingClient(api_key=cfg.openrouter_api_key, model=cfg.embedding_model)
    qv = client.embed_batch([text])[0]
    conn = _open_db(db_path)

    rows = conn.execute(
        """SELECT chunk_id, distance FROM vec_chunks
           WHERE embedding MATCH ? AND k=? ORDER BY distance""",
        (_vec_blob(qv), top),
    ).fetchall()

    matches: list[dict] = []
    q_tokens = _tokenize(text)
    overall = "NO_MATCH"

    for cid, dist in rows:
        chunk_row = conn.execute(
            """SELECT c.text, c.printed_page_start, s.bibkey, s.filename
               FROM chunks c JOIN sources s ON s.source_id=c.source_id
               WHERE c.chunk_id=?""",
            (int(cid),),
        ).fetchone()
        if not chunk_row:
            continue
        chunk_text, pps, bibkey, filename = chunk_row

        # Sentence-level matching: compute Jaccard/LCS against each sentence,
        # take the best score across all sentences to avoid granularity mismatch.
        sentences = _split_sentences(chunk_text)
        if not sentences:
            sentences = [chunk_text]

        best_jac = 0.0
        best_lcs = 0.0
        best_structural = 0.0
        best_sentence = chunk_text[:200]

        for sent in sentences:
            s_tokens = _tokenize(sent)
            j = _jaccard(q_tokens, s_tokens)
            lc = _lcs_ratio(q_tokens, s_tokens)
            st = _lcs_ratio(text.split(), sent.split())
            if max(j, lc, st) > max(best_jac, best_lcs, best_structural):
                best_jac, best_lcs, best_structural, best_sentence = j, lc, st, sent

        jac, lcs, structural = best_jac, best_lcs, best_structural
        matched_sentence = best_sentence

        # dense_score: 1/(1+L2). Not cosine similarity, but a monotone proxy.
        # For L2-normalized embeddings (text-embedding-3-large), realistic range is 0.42-0.67.
        dense_score = 1.0 / (1.0 + float(dist))

        verdict = _classify(jac, lcs, dense_score, structural, threshold_strict, threshold_fuzzy)
        if verdict != "NO_MATCH":
            diff = "".join(difflib.ndiff(text.split(), matched_sentence.split()))[:300]
            matches.append(
                {
                    "severity": verdict,
                    "jaccard": round(jac, 3),
                    "dense_score": round(dense_score, 3),
                    "lcs_ratio": round(lcs, 3),
                    "structural_similarity": round(structural, 3),
                    "source": {
                        "bibkey": bibkey,
                        "filename": filename,
                        "printed_page_start": pps,
                    },
                    "matched_text": matched_sentence,
                    "diff_preview": diff,
                    "recommendation": (
                        f"Cite as: \\parencite[S. {pps}]{{{bibkey}}}"
                        if bibkey and pps is not None
                        else f"Cite as: \\parencite{{{bibkey}}} (page unknown)"
                        if bibkey
                        else "Manual review (no bibkey)"
                    ),
                }
            )
            if verdict == "STRICT_MATCH":
                overall = "STRICT_MATCH"
            elif verdict == "FUZZY_MATCH" and overall != "STRICT_MATCH":
                overall = "FUZZY_MATCH"
            elif verdict == "THEMATIC_MATCH" and overall == "NO_MATCH":
                overall = "THEMATIC_MATCH"

    conn.close()
    return {
        "thesis": thesis,
        "input_text": text,
        "verdict": overall,
        "matches": matches[:5],
        "total_inspected": len(rows),
    }


def run_verify_quote(args: argparse.Namespace) -> int:
    cfg = load_config()
    if args.text:
        try:
            result = verify_quote(
                cfg,
                args.thesis,
                text=args.text,
                threshold_strict=args.threshold_strict,
                threshold_fuzzy=args.threshold_fuzzy,
                top=args.top,
            )
        except FileNotFoundError as e:
            sys.stderr.write(f"{e}\n")
            return 2
        # --pretty table output for verify-quote is deferred to v0.2
        emit_json(result)
        return 0
    else:
        from rag.tools.tex_split import iter_sentences

        results = []
        for sentence in iter_sentences(Path(args.tex)):
            res = verify_quote(
                cfg,
                args.thesis,
                text=sentence,
                threshold_strict=args.threshold_strict,
                threshold_fuzzy=args.threshold_fuzzy,
                top=args.top,
            )
            if res["verdict"] != "NO_MATCH":
                results.append(res)
        emit_json({"thesis": args.thesis, "tex": args.tex, "flagged_sentences": results})
        return 0
