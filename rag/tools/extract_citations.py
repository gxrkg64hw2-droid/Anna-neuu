"""Audit citations in .tex against bibliography.bib and the corpus."""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path

from rag.cli import emit_json
from rag.config import Config, load_config

CITE_RE = re.compile(
    r"\\(text|paren|foot)?cite\*?(?:\[(?P<pages>[^\]]*)\])?\{(?P<keys>[^}]+)\}"
)

# Matches a page number preceded by page-indicator tokens:
# "S.", "s.", "pp.", "p." — but NOT inside words like "Kap." (K-a-p => excluded by \b)
# Optional "vgl." prefix allowed. The page-indicator must be at a word boundary
# or directly after "vgl. ".
_PAGE_RE = re.compile(
    r"(?:(?:vgl\.|cf\.)\s*)?"        # optional qualifier
    r"(?:(?<!\w)[Ss]\.\s*|(?<!\w)pp?\.\s*)"  # "S." / "s." / "p." / "pp." not inside word
    r"(\d+)"
)


@dataclass
class Citation:
    file: Path
    line: int
    cmd: str
    pages: str | None
    bibkey: str
    # Character offset of the match start in the full file text (used for paragraph extraction)
    char_offset: int = 0


def parse_tex_citations(path: Path):
    text = path.read_text()
    for m in CITE_RE.finditer(text):
        cmd = (m.group(1) or "") + "cite"
        line = text[: m.start()].count("\n") + 1
        for key in (k.strip() for k in m.group("keys").split(",")):
            yield Citation(
                file=path,
                line=line,
                cmd=cmd,
                pages=m.group("pages"),
                bibkey=key,
                char_offset=m.start(),
            )


def parse_page_number(pages_str: str | None) -> int | None:
    """Extract the first page number from a LaTeX optional argument.

    Handles forms like 'S. 23 f.', 'vgl. S. 23-25', 'pp. 42', etc.
    Returns None when no page number can be parsed.
    """
    if not pages_str:
        return None
    m = _PAGE_RE.search(pages_str)
    if m:
        return int(m.group(1))
    return None


def parse_bib_keys(bib_path: Path) -> set[str]:
    if not bib_path.exists():
        return set()
    text = bib_path.read_text()
    return {m.group(1) for m in re.finditer(r"@\w+\{([^,]+),", text)}


def _extract_paragraph(text: str, char_offset: int, window: int = 500) -> str:
    """Return ~`window` chars before/after char_offset, bounded by paragraph breaks."""
    # Find paragraph start: walk back from offset until double-newline or section command
    start = max(0, char_offset - window)
    # Look for paragraph break or section boundary in the window before
    para_break = re.search(r"\n\n|\\(?:chapter|section|subsection)\*?\{", text[start:char_offset])
    if para_break:
        # Use the end of the match as the effective start
        start = start + para_break.end()

    # Find paragraph end: walk forward from end of citation until double-newline or section command
    end = min(len(text), char_offset + window)
    para_break_after = re.search(
        r"\n\n|\\(?:chapter|section|subsection)\*?\{", text[char_offset:end]
    )
    if para_break_after:
        end = char_offset + para_break_after.start()

    return text[start:end].strip()


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def check_page_content(
    cfg: Config,
    thesis: str,
    citations: list[Citation],
    tex_texts: dict[Path, str],
    *,
    threshold: float = 0.30,
) -> list[dict]:
    """Embed each cited paragraph and compare against the cited page's text.

    Uses the per-page text from the `pages` table (not chunks) so that the
    comparison is scoped exactly to the cited printed page rather than to
    potentially multi-page spanning chunks.

    Returns a list of PAGE_CONTENT_MISMATCH issue dicts.
    """
    from rag.indexer.embeddings import EmbeddingClient

    db_path = cfg.thesis_corpus_db(thesis)
    if not db_path.exists():
        sys.stderr.write(
            f"warning: --check-page-content: no corpus DB found for {thesis}, "
            "skipping.\n"
        )
        return []

    # Regular connection suffices here; vec extension only needed for chunk fallback
    conn = sqlite3.connect(str(db_path))

    # Gather paragraphs for all citations that have a page number
    to_check: list[tuple[Citation, int, str]] = []  # (citation, page_num, paragraph)
    for c in citations:
        page_num = parse_page_number(c.pages)
        if page_num is None:
            continue  # no page to check
        file_text = tex_texts.get(c.file, "")
        paragraph = _extract_paragraph(file_text, c.char_offset)
        if not paragraph:
            continue
        to_check.append((c, page_num, paragraph))

    if not to_check:
        conn.close()
        return []

    # Resolve source_ids and fetch page texts for all citations in one pass
    # Build a list of (citation, page_num, paragraph, source_id, page_text) tuples
    enriched: list[tuple[Citation, int, str, int, str]] = []
    for c, page_num, paragraph in to_check:
        src_row = conn.execute(
            "SELECT source_id FROM sources WHERE bibkey=?", (c.bibkey,)
        ).fetchone()
        if not src_row:
            continue  # No source in corpus; skip (check_corpus handles this)
        source_id = src_row[0]

        # Primary: look up the exact printed page in the pages table
        page_row = conn.execute(
            "SELECT text FROM pages WHERE source_id=? AND printed_page=?",
            (source_id, page_num),
        ).fetchone()
        if page_row:
            page_text = page_row[0]
        else:
            # Fallback: use the smallest chunk that covers this page
            chunk_row = conn.execute(
                """SELECT text FROM chunks
                   WHERE source_id=?
                     AND printed_page_start <= ?
                     AND printed_page_end >= ?
                   ORDER BY (printed_page_end - printed_page_start) ASC
                   LIMIT 1""",
                (source_id, page_num, page_num),
            ).fetchone()
            if not chunk_row:
                continue  # Nothing indexed for this page
            page_text = chunk_row[0]

        enriched.append((c, page_num, paragraph, source_id, page_text))

    if not enriched:
        conn.close()
        return []

    # Embed all paragraphs and page texts in a single batch call
    client = EmbeddingClient(api_key=cfg.openrouter_api_key, model=cfg.embedding_model)
    texts_to_embed = [item[2] for item in enriched] + [item[4] for item in enriched]
    all_embeddings = client.embed_batch(texts_to_embed)
    n = len(enriched)
    para_embeddings = all_embeddings[:n]
    page_embeddings = all_embeddings[n:]

    issues: list[dict] = []
    for (c, page_num, paragraph, _sid, page_text), para_emb, page_emb in zip(
        enriched, para_embeddings, page_embeddings
    ):
        sim = _cosine_similarity(para_emb, page_emb)
        if sim < threshold:
            issues.append(
                {
                    "type": "PAGE_CONTENT_MISMATCH",
                    "file": str(c.file),
                    "line": c.line,
                    "bibkey": c.bibkey,
                    "cited_page": page_num,
                    "max_similarity": round(sim, 3),
                    "threshold": threshold,
                    "paragraph_excerpt": paragraph[:200],
                    "page_excerpt": page_text[:200],
                    "note": (
                        f"Cited page {page_num} of '{c.bibkey}' has low semantic "
                        f"overlap with the surrounding paragraph "
                        f"(similarity {sim:.3f} < {threshold})."
                    ),
                }
            )

    conn.close()
    return issues


def audit(
    cfg: Config,
    thesis: str,
    *,
    tex: Path,
    check_bib: bool,
    check_pages: bool,
    check_orphans: bool,
    do_check_page_content: bool = False,
    page_content_threshold: float = 0.30,
) -> dict:
    files = [tex] if tex.is_file() else list(tex.rglob("*.tex"))

    # Read all file texts up front so paragraph extraction can work on them
    tex_texts: dict[Path, str] = {}
    for f in files:
        try:
            tex_texts[f] = f.read_text()
        except Exception:
            tex_texts[f] = ""

    citations: list[Citation] = []
    for f in files:
        citations.extend(parse_tex_citations(f))

    bib_path = cfg.thesis_dir(thesis) / "bibliography.bib"
    bib_keys = parse_bib_keys(bib_path)

    issues: list[dict] = []
    if check_bib:
        for c in citations:
            if c.bibkey not in bib_keys:
                from difflib import get_close_matches

                near = get_close_matches(c.bibkey, bib_keys, n=1)
                issues.append(
                    {
                        "type": "MISSING_BIBKEY",
                        "file": str(c.file),
                        "line": c.line,
                        "bibkey": c.bibkey,
                        "suggestion": (
                            f"Closest match: {near[0]}" if near else "No close match"
                        ),
                    }
                )

    if check_orphans:
        used = {c.bibkey for c in citations}
        for k in bib_keys - used:
            issues.append(
                {
                    "type": "ORPHAN_BIB",
                    "bibkey": k,
                    "note": "Present in bibliography.bib but never cited",
                }
            )

    if check_pages:
        db = cfg.thesis_corpus_db(thesis)
        if db.exists():
            conn = sqlite3.connect(str(db))
            for c in citations:
                row = conn.execute(
                    "SELECT source_id FROM sources WHERE bibkey=?", (c.bibkey,)
                ).fetchone()
                if not row:
                    issues.append(
                        {
                            "type": "BIBKEY_NOT_IN_CORPUS",
                            "file": str(c.file),
                            "line": c.line,
                            "bibkey": c.bibkey,
                            "note": "Citation key has no matching source in the corpus index",
                        }
                    )
            conn.close()

    if do_check_page_content:
        pc_issues = check_page_content(
            cfg,
            thesis,
            citations,
            tex_texts,
            threshold=page_content_threshold,
        )
        issues.extend(pc_issues)

    summary = {
        "missing_bibkeys": sum(1 for i in issues if i["type"] == "MISSING_BIBKEY"),
        "orphan_bib_entries": sum(1 for i in issues if i["type"] == "ORPHAN_BIB"),
        "bibkey_not_in_corpus": sum(1 for i in issues if i["type"] == "BIBKEY_NOT_IN_CORPUS"),
        "page_content_mismatches": sum(
            1 for i in issues if i["type"] == "PAGE_CONTENT_MISMATCH"
        ),
    }
    return {
        "thesis": thesis,
        "tex_files_scanned": len(files),
        "total_citations": len(citations),
        "unique_sources": len({c.bibkey for c in citations}),
        "issues": issues,
        "summary": summary,
    }


def run_extract_citations(args: argparse.Namespace) -> int:
    cfg = load_config()
    tex = Path(args.tex)
    if not tex.exists():
        sys.stderr.write(f"Tex path does not exist: {tex}\n")
        return 2
    # check_pages is a deprecated alias for check_corpus;
    # for semantic matching use --check-page-content
    check_corpus = getattr(args, "check_corpus", False) or args.check_pages
    if args.check_pages:
        sys.stderr.write(
            "warning: --check-pages currently checks corpus presence only, not page "
            "content. Use --check-corpus going forward. For semantic page-content "
            "verification use --check-page-content.\n"
        )
    result = audit(
        cfg,
        args.thesis,
        tex=tex,
        check_bib=args.check_bib,
        check_pages=check_corpus,
        check_orphans=args.check_orphans,
        do_check_page_content=getattr(args, "check_page_content", False),
        page_content_threshold=getattr(args, "page_content_threshold", 0.30),
    )
    if args.pretty:
        from rag.tools.format import render_extract_citations_pretty
        render_extract_citations_pretty(result)
        return 1 if (args.strict and result["issues"]) else 0
    emit_json(result)
    return 1 if (args.strict and result["issues"]) else 0
