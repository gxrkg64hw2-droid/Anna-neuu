# Known Issues

## Closed in v0.1.1 (2026-05-06)

- **Bib-build title-search misclassified PDFs to wrong papers** (Bug A). Fixed in commit `9e88624`. Title extraction now uses PyMuPDF font-size analysis. arXiv-ID short-circuits to deterministic DOI lookup.
- **Bib-build dropped PDFs silently on bibkey collision** (Bug B). Fixed in commit `9e88624`. Collisions now disambiguate with `a`/`b`/`c` suffixes plus an explicit warning entry.
- **No mapping mechanism between bibliography.bib and sources table** (Bug C). Fixed in commits `9e88624`+`515d634`. New `link_bibkeys_to_sources` runs automatically after `bib --build` and `index`, also populates title, authors, year.
- **Placeholder DOIs (`10.1145/nnnnnnn.nnnnnnn` etc.) caused wrong matches** (follow-up to Bug A). Fixed in commit `a9ea61e`. Extractor now rejects DOIs with runs of 4+ repeated letters.
- **OCR fallback never auto-triggered in build pipeline.** Fixed in commit `7ab35c7`. Pages with quality < 0.4 now go through `ocrmypdf` automatically (skippable with `--skip-ocr`); `ocr_pages` counter is real.
- **`overrides.toml` documented but never read.** Fixed in commit `7ab35c7`. Per-PDF overrides for `print_offset` and `print_offset_confidence` now apply at index time. Suppresses low-confidence warning when override is present.
- **verify-quote thresholds practically unreachable** (Bug D). Fixed in commit `3da0aa1`. Sentence-level matching within candidate chunks; thresholds recalibrated (`--threshold-strict 0.40`, `--threshold-fuzzy 0.45`); internal `cosine` field renamed to `dense_score` to stop misleading.

End-to-end real-world test now produces 0 warnings on the test corpus and correctly flags near-identical sentences as STRICT_MATCH.

## Open (deferred to v0.2)

### Filters applied after top-k cut in search

**Severity:** UX issue.
**Where:** `rag/search/query.py`
**Symptom:** `--filter-source` and `--filter-year` are applied AFTER fusion truncates to top-30. If all 30 fail the filter, the search returns empty even though matching results exist deeper in the ranking.
**Fix plan:** Apply filters before the top-k cut, or expand the candidate pool when filters are active.

### L2-distance vs cosine-similarity threshold semantics

**Severity:** Cosmetic semantics.
**Where:** `rag/search/query.py`, public `score_dense` field.
**Symptom:** Score is `1.0 / (1.0 + L2_distance)`, labeled `score_dense`. For OpenAI embeddings (L2-normalized), L2 and cosine are monotonically related, so ranking is correct, but the absolute value is not a true cosine.
**Fix plan:** Switch sqlite-vec to inner-product distance (returns cosine for normalized vectors) and rename consistently. Low priority: ranking quality unaffected.

### Page-content mismatch detection

**Status: CLOSED** (implemented in v0.2.1).
**Where:** `rag/tools/extract_citations.py`
**Implementation:** `--check-page-content` flag. Uses per-page text from the `pages` table (not chunks) to get precise page-level content. Embeds the surrounding paragraph and the cited page text, computes cosine similarity, flags if below threshold (default 0.30, configurable via `--page-content-threshold`). Deduplication note: relies on correct `print_offset` calibration in corpus. If a source has a miscalibrated offset, false positives or false negatives can occur; fix via `overrides.toml`.

### Synonym-aware verify-quote stage 3

**Severity:** Spec promised, partially implemented.
**Where:** `rag/tools/verify_quote.py`
**Symptom:** Spec section 5 describes a 4-stage pipeline. Stages 1 (embedding broad-net), 2 (Jaccard/LCS at sentence level), and 4 (structural similarity) are implemented. Stage 3 (synonym substitution via WordNet/word-embedding) is not.
**Fix plan:** Add WordNet-based synonym substitution before re-running Jaccard/LCS for borderline cases.

### `--pretty` flag

**Severity:** Cosmetic.
**Where:** All CLI commands.
**Symptom:** All commands accept `--pretty` but it is currently a no-op (JSON is always pretty-printed with indent=2).
**Fix plan:** Implement table-oriented human-readable output for the most-used commands (search, corpus, extract-citations).

### Vision-OCR (Gemini Flash fallback)

**Severity:** v2 feature, explicitly deferred per spec section 12.

## Code hygiene (any version)

### Unused dependencies

`pydantic` and `rich` are listed in `pyproject.toml` but not imported anywhere in `rag/`. Either start using them (rich is the obvious candidate for `--pretty`) or remove from `pyproject.toml`.

### Duplicate dev-dep declarations

Both `[project.optional-dependencies] dev` and `[dependency-groups] dev` exist in `pyproject.toml`. Pick one (PEP 735 `dependency-groups` is the modern way).

### Quality-score weights sum to 0.90

`rag/parsers/quality.py` weights add to 0.40 + 0.30 + 0.20 = 0.90. A perfectly clean text caps at 0.90. Either add a 0.10 weight to one of the existing factors, or normalize to 0.0-1.0 explicitly.

### Page-offset regex misses `Ü`

`rag/parsers/page_offset.py` ASCII pattern `[A-ZAOU]` does not match `Ü`. Edge case for German chapter titles like `1 Übersicht`. Other patterns (`Kapitel 1`, `1 Introduction`) usually compensate.

### `build.log` referenced but not written

`CLAUDE.md` mentions `thesen/<name>/index/build.log`. Indexer writes `parse_quality.json` only.

## Closed in writing-extension v0.2.0 (this iteration)

- Skill layer added: 10 vendored K-Dense skills (DACH-adapted) + 1 bridge skill `bachelorarbeit-arbeitsweise`.
- LaTeX template library added: 5 profiles (technisch-informatik, empirisch-quantitativ, theoretisch-konzeptionell, marketing-case-study, mixed-methods-mayring) with `_common/` layer.
- New CLI subcommand: `python -m rag thesis init`.
- Sync tooling: `tools/skills-sync.sh` re-vendors at a pinned commit.

## Open after writing-extension v0.2.0

### Hochschul-specific style classes

Some universities mandate `.cls` files (e.g., `unimannheim.cls`). Currently a manual override path: drop the `.cls` into `_common/` and adjust `main.tex`. Could be productized as a "profile + university overlay" pattern in a later iteration.

### TikZ chart auto-generation skill

Templates ship with TikZ + pgfplots ready and Porter/SWOT/BCG TikZ macros for the marketing-case-study profile, but no skill that synthesizes a chart from a verbal description. Out of scope for v0.2.0.

### LaTeX linter integration

`chktex`, `latexindent` not integrated. User can run them manually.

### MCP-availability degradation

If Brave or Firecrawl MCPs are unavailable, the bridge skill falls back to "ask the user". A more graceful degradation (e.g., direct WebSearch via WebFetch) could be added later.
