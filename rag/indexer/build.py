"""Index builder pipeline: PDFs -> chunks -> embeddings + BM25 -> SQLite."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
import tempfile
import time
import tomllib
from pathlib import Path

from rag.cli import emit_json
from rag.config import Config, load_config
from rag.indexer.bm25 import build_bm25_index, save_index
from rag.indexer.embeddings import EmbeddingClient
from rag.indexer.store import Store
from rag.parsers.chunking import chunk_text
from rag.parsers.ocr import needs_ocr, run_ocr_on_pdf
from rag.parsers.page_offset import detect_print_offset
from rag.parsers.pdf import EncryptedPDFError, extract_pages
from rag.parsers.quality import score_page


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for blk in iter(lambda: fh.read(65536), b""):
            h.update(blk)
    return h.hexdigest()


def _load_overrides(thesis_dir: Path) -> dict:
    """Read overrides.toml if present. Returns dict keyed by filename."""
    p = thesis_dir / "overrides.toml"
    if not p.exists():
        return {}
    try:
        data = tomllib.loads(p.read_text())
    except tomllib.TOMLDecodeError as e:
        print(f"WARN: overrides.toml parse error: {e}", file=sys.stderr)
        return {}
    return data.get("pdf", {})


def build_index(
    cfg: Config,
    thesis: str,
    *,
    rebuild: bool,
    only: str | None,
    skip_ocr: bool,
    vision_ocr: str | None,
) -> dict:
    pdf_dir = cfg.thesis_pdfs_dir(thesis)
    if not pdf_dir.exists():
        raise FileNotFoundError(f"No pdfs/ folder for thesis '{thesis}': {pdf_dir}")

    overrides = _load_overrides(cfg.thesis_dir(thesis))

    db_path = cfg.thesis_corpus_db(thesis)
    if rebuild and db_path.exists():
        db_path.unlink()
    store = Store.create(db_path)

    pdfs = sorted(p for p in pdf_dir.glob("*.pdf"))
    if only:
        pdfs = [p for p in pdfs if fnmatch.fnmatch(p.name, only)]

    embed_client = EmbeddingClient(api_key=cfg.openrouter_api_key, model=cfg.embedding_model)

    new_pdfs = 0
    unchanged_pdfs = 0
    total_chunks = 0
    ocr_pages_total = 0
    warnings: list[dict] = []

    all_chunk_ids: list[int] = []
    all_chunk_texts: list[str] = []
    new_chunks_for_embed: list[tuple[int, str]] = []
    t0 = time.time()

    for pdf in pdfs:
        sha = _sha256(pdf)
        # Detect changed PDFs (same filename, different content) and clean stale data
        existing_by_name = store.conn.execute(
            "SELECT source_id, sha256 FROM sources WHERE filename=?", (pdf.name,)
        ).fetchone()
        if existing_by_name is not None and existing_by_name[1] != sha:
            store.delete_source(existing_by_name[0])
        existing = store.find_source_by_sha256(sha)
        if existing is not None and not rebuild:
            unchanged_pdfs += 1
            cur = store.conn.execute(
                "SELECT chunk_id, text FROM chunks WHERE source_id=?", (existing,)
            )
            for cid, txt in cur:
                all_chunk_ids.append(cid)
                all_chunk_texts.append(txt)
            continue

        # Parse
        try:
            pages = extract_pages(pdf)
        except EncryptedPDFError as e:
            warnings.append({
                "pdf": pdf.name, "issue": "encrypted_pdf",
                "note": str(e),
            })
            continue
        page_qualities = [score_page(p.text) for p in pages]
        offset, conf = detect_print_offset([p.text for p in pages])

        # Apply per-PDF override if present; otherwise warn on low confidence
        override = overrides.get(pdf.name, {})
        if "print_offset" in override:
            offset = int(override["print_offset"])
            conf = float(override.get("print_offset_confidence", 1.0))
        elif conf < 0.7:
            warnings.append({
                "pdf": pdf.name,
                "issue": "page_offset_low_confidence",
                "detected": offset,
                "confidence": conf,
            })

        # OCR fallback: re-extract low-quality pages via ocrmypdf
        ocred_pages: set[int] = set()
        if not skip_ocr:
            low_q_pages = needs_ocr(page_qualities, threshold=0.4)
            if low_q_pages:
                try:
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        tmp_path = Path(tmp.name)
                    run_ocr_on_pdf(pdf, tmp_path, low_q_pages, languages="deu+eng")
                    ocred_pages_obj = extract_pages(tmp_path)
                    # Replace text for affected pages
                    for i in low_q_pages:
                        if i <= len(ocred_pages_obj):
                            pages[i - 1] = ocred_pages_obj[i - 1]
                            page_qualities[i - 1] = score_page(ocred_pages_obj[i - 1].text)
                            ocred_pages.add(i)
                    tmp_path.unlink(missing_ok=True)
                except RuntimeError as e:
                    warnings.append({
                        "pdf": pdf.name,
                        "issue": "ocr_failed",
                        "low_quality_pages": low_q_pages,
                        "error": str(e),
                    })

        ocr_pages_total += len(ocred_pages)

        # Source row
        src_id = store.add_source(
            filename=pdf.name,
            sha256=sha,
            page_count_pdf=len(pages),
            title=None,
            authors=[],
            year=None,
            doi=None,
            page_count_printed=len(pages) - offset if offset else len(pages),
            print_offset=offset,
            print_offset_confidence=conf,
        )

        # Pages
        for p, q in zip(pages, page_qualities):
            printed = p.pdf_page - offset if (p.pdf_page - offset) >= 1 else None
            store.add_page(
                source_id=src_id,
                pdf_page=p.pdf_page,
                printed_page=printed,
                text=p.text,
                quality_score=q,
                ocr_origin=1 if p.pdf_page in ocred_pages else 0,
            )

        # Chunks per PDF (chunk concatenated text, track page span)
        full_text = "\n\n".join(p.text for p in pages)
        chunks = chunk_text(
            full_text,
            target_tokens=cfg.chunk_target_tokens,
            overlap_tokens=cfg.chunk_overlap_tokens,
        )

        # Naive page-span attribution: walk chars cumulatively
        page_char_offsets: list[tuple[int, int, int]] = []  # (start_char, end_char, pdf_page)
        cursor = 0
        for p in pages:
            page_char_offsets.append((cursor, cursor + len(p.text), p.pdf_page))
            cursor += len(p.text) + 2  # +2 for the "\n\n" join

        for c in chunks:
            page_start = next(
                (pp for s, e, pp in page_char_offsets if s <= c.char_start < e),
                pages[0].pdf_page,
            )
            page_end = next(
                (pp for s, e, pp in reversed(page_char_offsets) if s < c.char_end <= e),
                pages[-1].pdf_page,
            )
            quality_avg = sum(page_qualities[max(0, page_start - 1) : page_end]) / max(
                1, page_end - page_start + 1
            )
            chunk_id = store.add_chunk(
                source_id=src_id,
                text=c.text,
                token_count=c.token_count,
                pdf_page_start=page_start,
                pdf_page_end=page_end,
                printed_page_start=(page_start - offset if page_start > offset else None),
                printed_page_end=(page_end - offset if page_end > offset else None),
                quality_score=quality_avg,
                ocr_origin=0,
            )
            all_chunk_ids.append(chunk_id)
            all_chunk_texts.append(c.text)
            new_chunks_for_embed.append((chunk_id, c.text))
            total_chunks += 1
        new_pdfs += 1

    # Embed new chunks
    if new_chunks_for_embed:
        texts = [t for _, t in new_chunks_for_embed]
        vectors = embed_client.embed_batch(texts)
        for (cid, _), vec in zip(new_chunks_for_embed, vectors):
            store.add_embedding(cid, vec)

    store.conn.commit()

    # Build BM25 over the whole corpus (not just new)
    if all_chunk_ids:
        bm25_idx = build_bm25_index(all_chunk_ids, all_chunk_texts, language=cfg.bm25_language)
        save_index(bm25_idx, cfg.thesis_index_dir(thesis))

    duration = time.time() - t0
    result = {
        "thesis": thesis,
        "indexed": {
            "new_pdfs": new_pdfs,
            "unchanged_pdfs": unchanged_pdfs,
            "total_chunks": total_chunks if total_chunks else len(all_chunk_ids),
            "ocr_pages": ocr_pages_total,
            "vision_ocr_pages": 0,
        },
        "warnings": warnings,
        "cost_usd": round(
            0.13 / 1_000_000 * sum(len(t) // 4 for t in all_chunk_texts), 4
        ),
        "duration_seconds": round(duration, 2),
    }
    # Auto-link bibkeys if a bibliography.bib exists (Premium mode workflow)
    bib_path = cfg.thesis_dir(thesis) / "bibliography.bib"
    if bib_path.exists():
        from rag.metadata.bib import link_bibkeys_to_sources
        link_result = link_bibkeys_to_sources(cfg, thesis)
        result["bibkey_linking"] = link_result

    quality_path = cfg.thesis_index_dir(thesis) / "parse_quality.json"
    quality_path.write_text(json.dumps(result, indent=2))
    store.close()
    return result


def run_index(args: argparse.Namespace) -> int:
    cfg = load_config()
    result = build_index(
        cfg,
        args.thesis,
        rebuild=args.rebuild,
        only=args.only,
        skip_ocr=args.skip_ocr,
        vision_ocr=args.vision_ocr,
    )
    # --pretty table output for index is deferred to v0.2
    emit_json(result)
    return 0
