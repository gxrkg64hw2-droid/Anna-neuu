"""BibTeX generation in Better-BibTeX style: <lastname><Title><year>."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from rag.cli import emit_json
from rag.config import load_config
from rag.metadata.crossref import lookup_by_doi as crossref_doi
from rag.metadata.doi_extract import extract_doi_from_text
from rag.metadata.openalex import lookup_by_doi, search_by_title
from rag.parsers.pdf import extract_arxiv_id, extract_pages, extract_title_candidates

STOPWORDS_TITLE = set("a an the of and or in on for to from at by with into".split())


def _last_name(author: str) -> str:
    if "," in author:
        return author.split(",")[0].strip()
    parts = author.split()
    return parts[-1] if parts else ""


def make_bibkey(meta: dict) -> str:
    authors = meta.get("authors") or []
    last = _last_name(authors[0]) if authors else "anon"
    last = re.sub(r"[^A-Za-z]", "", last).lower()
    # Take up to 2 title words; first word needs >= 3 chars, second >= 4
    words = []
    for w in re.findall(r"[A-Za-z]+", meta.get("title", "")):
        min_len = 3 if len(words) == 0 else 4
        if w.lower() not in STOPWORDS_TITLE and len(w) >= min_len:
            words.append(w[:1].upper() + w[1:])
        if len(words) == 2:
            break
    title_part = "".join(words) or "Work"
    year = meta.get("year") or "nd"
    return f"{last}{title_part}{year}"


def render_bibtex(key: str, meta: dict, filename: str | None = None) -> str:
    _article_types = (None, "article", "article-journal", "journal-article")
    bib_type = "article" if meta.get("type") in _article_types else "misc"
    fields = []
    if meta.get("title"):
        fields.append(f"  title = {{{meta['title']}}}")
    if meta.get("authors"):
        fields.append(f"  author = {{{ ' and '.join(meta['authors']) }}}")
    if meta.get("year"):
        fields.append(f"  year = {{{meta['year']}}}")
    if meta.get("venue"):
        fields.append(f"  journal = {{{meta['venue']}}}")
    if meta.get("doi"):
        fields.append(f"  doi = {{{meta['doi']}}}")
    if filename:
        fields.append(f"  file = {{{filename}}}")
    body = ",\n".join(fields)
    return f"@{bib_type}{{{key},\n{body}\n}}"


def _disambiguate_key(base_key: str, existing_keys: set[str]) -> str:
    """If base_key collides, append 'a', 'b', ... until unique."""
    if base_key not in existing_keys:
        return base_key
    for suffix in "abcdefghijklmnopqrstuvwxyz":
        candidate = f"{base_key}{suffix}"
        if candidate not in existing_keys:
            return candidate
    raise RuntimeError(f"More than 26 collisions for bibkey base {base_key}")


def parse_existing_keys(bib_path):
    if not bib_path.exists():
        return set()
    return {m.group(1) for m in re.finditer(r"@\w+\{([^,]+),", bib_path.read_text())}


def build_bibliography(cfg, thesis: str) -> dict:
    pdfs_dir = cfg.thesis_pdfs_dir(thesis)
    bib_path = cfg.thesis_dir(thesis) / "bibliography.bib"
    existing_keys = parse_existing_keys(bib_path)
    counts = {"openalex_by_doi": 0, "crossref_fallback": 0, "title_search": 0,
              "manual_review_required": 0}
    new_entries = []
    warnings = []

    for pdf in sorted(pdfs_dir.glob("*.pdf")):
        pages = extract_pages(pdf)
        head_text = " ".join(p.text for p in pages[:3])
        doi = extract_doi_from_text(head_text)
        meta = None
        if doi:
            meta = lookup_by_doi(doi)
            if meta:
                counts["openalex_by_doi"] += 1
            else:
                meta = crossref_doi(doi)
                if meta:
                    counts["crossref_fallback"] += 1
        if not meta:
            # Try arXiv ID first (very common for preprints, deterministic lookup)
            arxiv_id = extract_arxiv_id(head_text)
            if arxiv_id:
                meta = lookup_by_doi(f"10.48550/arxiv.{arxiv_id}")
                if meta:
                    counts["openalex_by_doi"] += 1

        if not meta:
            # Try title candidates from page 1, largest font first
            candidates = extract_title_candidates(pdf, top_n=3)
            for cand in candidates:
                if len(cand) < 15:  # too short to be a title
                    continue
                results = search_by_title(cand, top=1)
                if results:
                    meta = results[0]
                    counts["title_search"] += 1
                    break

        if not meta:
            counts["manual_review_required"] += 1
            warnings.append({
                "pdf": pdf.name, "issue": "no_doi_no_title_match",
                "action": "needs_manual_review",
            })
            continue

        key = make_bibkey(meta)
        original_key = key
        key = _disambiguate_key(key, existing_keys)
        if key != original_key:
            warnings.append({
                "pdf": pdf.name,
                "issue": "bibkey_collision",
                "original_key": original_key,
                "assigned_key": key,
                "note": "Bibkey was already taken by another entry; assigned with suffix.",
            })
        new_entries.append(render_bibtex(key, meta, filename=pdf.name))
        existing_keys.add(key)

    if new_entries:
        with bib_path.open("a") as f:
            f.write("\n% Auto-generated by rag bib --build\n")
            for entry in new_entries:
                f.write(entry + "\n\n")

    return {
        "thesis": thesis,
        "pdfs_processed": sum(1 for _ in pdfs_dir.glob("*.pdf")),
        "matched": counts,
        "bibliography_entries_added": len(new_entries),
        "warnings": warnings,
    }


def link_bibkeys_to_sources(cfg, thesis: str) -> dict:
    """Read bibliography.bib, parse `file` fields, update sources.bibkey, .title,
    .authors, .year by filename. Best-effort field extraction from each bib entry."""
    import json as _json
    import sqlite3
    bib_path = cfg.thesis_dir(thesis) / "bibliography.bib"
    db_path = cfg.thesis_corpus_db(thesis)
    if not bib_path.exists() or not db_path.exists():
        return {"linked": 0, "skipped": "missing bib or db"}

    text = bib_path.read_text()
    entries = re.finditer(r"@\w+\{([^,]+),(.+?)^\}", text, re.DOTALL | re.MULTILINE)
    # filename -> {bibkey, title, authors, year}
    mapping: dict[str, dict] = {}
    for m in entries:
        key = m.group(1).strip()
        body = m.group(2)
        file_match = re.search(r"file\s*=\s*\{([^}]+)\}", body)
        if not file_match:
            continue
        fname_raw = file_match.group(1).strip()
        target_fname = None
        for f in fname_raw.split(";"):
            f = f.strip()
            if f.lower().endswith(".pdf"):
                target_fname = Path(f).name
                break
        if not target_fname:
            continue

        title_match = re.search(r"title\s*=\s*\{([^}]+)\}", body)
        author_match = re.search(r"author\s*=\s*\{([^}]+)\}", body)
        year_match = re.search(r"year\s*=\s*\{(\d{4})\}", body)
        title = title_match.group(1).strip() if title_match else None
        authors_str = author_match.group(1).strip() if author_match else ""
        authors = (
            [a.strip() for a in authors_str.split(" and ") if a.strip()]
            if authors_str else []
        )
        year = int(year_match.group(1)) if year_match else None
        mapping[target_fname] = {
            "bibkey": key, "title": title, "authors": authors, "year": year,
        }

    if not mapping:
        return {
            "linked": 0,
            "note": "No 'file' fields found in bib (Zotero Better BibTeX adds them automatically)",
        }

    conn = sqlite3.connect(str(db_path))
    linked = 0
    not_found = []
    for fname, fields in mapping.items():
        cur = conn.execute(
            "UPDATE sources SET bibkey=?, title=?, authors=?, year=? WHERE filename=?",
            (fields["bibkey"], fields["title"], _json.dumps(fields["authors"]),
             fields["year"], fname),
        )
        if cur.rowcount > 0:
            linked += 1
        else:
            not_found.append(fname)
    conn.commit()
    conn.close()
    return {"linked": linked, "not_found": not_found, "mapped_pairs": len(mapping)}


def run_bib(args: argparse.Namespace) -> int:
    cfg = load_config()
    if args.build:
        result = build_bibliography(cfg, args.thesis)
        # If an index exists, also link the bibkeys
        if cfg.thesis_corpus_db(args.thesis).exists():
            link_result = link_bibkeys_to_sources(cfg, args.thesis)
            result["bibkey_linking"] = link_result
    elif args.check:
        bib_path = cfg.thesis_dir(args.thesis) / "bibliography.bib"
        result = {"thesis": args.thesis, "bib_keys": sorted(parse_existing_keys(bib_path))}
    else:
        result = {"thesis": args.thesis, "note": "reconcile not implemented in v1"}
    # --pretty table output for bib is deferred to v0.2
    emit_json(result)
    return 0
