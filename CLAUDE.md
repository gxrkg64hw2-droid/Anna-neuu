# CLAUDE.md (System Brief)

You are operating the **Bachelorarbeits-System**: a CLI toolkit that extends your retrieval and citation capabilities for academic thesis writing. **You operate it. The user does not.**

## ⛔ Pflicht-Skills laden, sobald an einer Thesis gearbeitet wird ⛔

Sobald in dieser Session an einer Bachelorarbeit gearbeitet wird (Anzeichen: das Wort „Bachelorarbeit" oder „Thesis" im User-Prompt; das Editieren einer `.tex`-Datei unter `thesen/<name>/tex/`; das Anlegen einer neuen Thesis mit `python -m rag thesis init`), MUSS die folgende Skill-Hierarchie aktiv sein und befolgt werden:

| Skill | Zweck | Wann zwingend |
|---|---|---|
| `bachelorarbeit-arbeitsweise` | Bridge-Skill, orchestriert das System (rag search vor jeder Aussage, verify-quote nach jedem Absatz, extract-citations vor jedem Commit, Pflicht-Reviews nach jedem Kapitel). Enthält die harten Regeln und Eskalations-Kriterien. | Immer, wenn `.tex`-Inhalt geschrieben oder überarbeitet wird |
| `bachelorarbeit-review-citations` | Review-Skill A. Prüft Bibkeys, Seitenzahlen und semantischen Inhaltsabgleich pro Citation. Nutzt automatisch `extract-citations --check-page-content`. | Nach jedem fertigen Kapitel |
| `bachelorarbeit-review-style` | Review-Skill B. Prüft deutsche Typographie (Umlaute, keine Em-/En-Dashes, deutsche Anführungszeichen), Gendering-Konsistenz, Satzlänge, wissenschaftlicher Ton. | Nach jedem fertigen Kapitel |
| `bachelorarbeit-review-structure` | Review-Skill C. Prüft Argumentationsfaden, Konsistenz zwischen Kapiteln, Vollständigkeit gegen den Plan, methodische Substanz. | Nach jedem fertigen Kapitel |
| Vendored K-Dense-Skills (`scientific-writing`, `literature-review`, `hypothesis-generation`, `statistical-analysis`, `scientific-critical-thinking`, `scientific-visualization`, `scientific-brainstorming`, `peer-review`, `scholar-evaluation`, `market-research-reports`) | Wissenschaftliches Schreibhandwerk. Werden je nach Kapiteltyp aktiviert (Tabelle in der Bridge-Skill). | Je nach Kapiteltyp |

**Verbindliche Reihenfolge beim Schreiben:**

1. Bridge-Skill `bachelorarbeit-arbeitsweise` aktivieren und Schritt 1 bis 7 des Sieben-Schritt-Rituals strikt einhalten.
2. Pro Aussage frischer `python -m rag search`-Aufruf, `citation_suggestion` verbatim einsetzen. NIEMALS aus dem Gedächtnis zitieren. Verstoß = Eskalation an den Nutzer.
3. Pro Absatz `python -m rag verify-quote`. STRICT_MATCH/FUZZY_MATCH ernst nehmen.
4. Nach jedem fertigen Kapitel die drei Review-Skills (A, B, C) parallel als Subagents dispatchen. Findings abarbeiten, bevor das nächste Kapitel angefasst wird oder ein Commit erfolgt.
5. Vor jedem Commit: `python -m rag extract-citations --check-bib --check-corpus --check-orphans --check-page-content --strict`. Exit-Code 1 = Issues fixen, dann erst commit.

**Verboten:**

- Skill-Inhalte ignorieren oder „kurz übergehen", weil der Nutzer wartet.
- Reviews überspringen, weil das Kapitel „eh nur ein Entwurf" ist.
- Citations aus früheren Absätzen oder aus dem Gedächtnis kopieren.

**Bei Konflikten zwischen Skills:** die Bridge-Skill `bachelorarbeit-arbeitsweise` hat Vorrang vor allen vendored Skills, und das vorliegende `CLAUDE.md` hat Vorrang vor der Bridge-Skill, wo es ausdrücklich Regeln vorgibt.

## Repository layout

| Path | Purpose |
|---|---|
| `rag/` | Single Python package, entry point `python -m rag <cmd>` |
| `rag/parsers/` | PDF text extraction, quality scoring, page-offset detection, chunking, OCR |
| `rag/indexer/` | SQLite + sqlite-vec store, OpenAI embeddings via OpenRouter, bm25s, build pipeline |
| `rag/search/` | Hybrid retrieval, RRF fusion, optional bge-reranker, formatters |
| `rag/tools/` | verify-quote, extract-citations, corpus inventory |
| `rag/metadata/` | DOI extraction, OpenAlex, Crossref, BibTeX writer with auto-linking |
| `thesen/` | Per-thesis corpora. Always read `thesen/<name>/CLAUDE.md` before working on a specific thesis |
| `thesen/_template/` | Copy this for new theses |
| `docs/superpowers/specs/` | Design spec (full architecture rationale) |
| `docs/superpowers/plans/` | Implementation plan (TDD-style task list) |
| `KNOWN_ISSUES.md` | Open gaps and deferred items. Read before assuming a feature works. |
| `Archiv-PA2-System/` | Old PA2 generation, reference only |

## Setup (one-time per machine)

```bash
brew install uv tesseract            # uv = Python toolchain, tesseract powers OCR
uv sync                              # installs runtime deps
uv sync --extra rerank               # optionally adds bge-reranker-v2-m3 (570 MB model)
uv sync --group dev                  # adds pytest + ruff for development
cp .env.example .env                 # add OPENROUTER_API_KEY=sk-or-v1-...
```

The `.env` is the only place secrets live. `OPENROUTER_API_KEY` is required (used for OpenAI text-embedding-3-large via OpenRouter at $0.13/1M tokens). `BM25_LANGUAGE=german` for German-language theses (default `english`).

## The two operating modes

A thesis runs in one of two modes:

**Premium mode (recommended when available):**
- User exports their Zotero collection via Better BibTeX with "Export with Auto-Update" + "Keep updated".
- The exported `.bib` lands at `thesen/<name>/bibliography.bib`. Better BibTeX automatically writes `file = {filename.pdf}` fields linking each entry to its source PDF.
- After `python -m rag index` runs, the auto-linker reads those `file =` fields and populates `sources.bibkey`, `sources.title`, `sources.authors`, `sources.year` in the corpus DB.
- Search hits return real bibkeys and ready-to-paste `\parencite[S. X]{key}` citation suggestions.

**Lean mode (when no bib is available):**
- User drops only PDFs into `thesen/<name>/pdfs/`.
- Run `python -m rag bib --thesis <name> --build` to assemble a `bibliography.bib` from scratch via DOI extraction, OpenAlex lookup, then Crossref fallback, then title-search via PyMuPDF font-size analysis.
- The `--build` step also auto-links bibkeys to the corpus DB if the index already exists.

The thesis-level `CLAUDE.md` should mark which mode is active.

## Available commands

All commands take `--thesis <name>` (required) and `--pretty` (human-readable output where supported, else JSON-pretty). JSON to stdout, errors to stderr, stable exit codes (0 success, 1 audit-strict failure, 2 environment/index missing).

### `index` — build or refresh the corpus index

```
python -m rag index --thesis <name> [options]
  --rebuild                  Drop existing index and rebuild from scratch
  --only <pdf-glob>          Index only matching PDFs (e.g. "rogers*.pdf")
  --skip-ocr                 Skip Tesseract OCR fallback even on low-quality pages
  --vision-ocr <pdf-glob>    Reserved for v2 Gemini Flash escalation (currently no-op)
  --pretty                   JSON pretty-print (full --pretty rendering deferred to v0.2)
```

**What happens:**
1. Hash each PDF (SHA-256). Unchanged PDFs are skipped.
2. Changed PDFs (same filename, different SHA) trigger `delete_source` so old chunks/embeddings are purged before re-indexing.
3. PyMuPDF extracts text per page, computes quality score per page.
4. If a page's quality is below 0.4 and `--skip-ocr` is not set, ocrmypdf runs Tesseract on those specific pages and re-extracts.
5. Page-offset is auto-detected (PDF page → printed page). `overrides.toml` per-PDF entries take precedence.
6. Recursive 512-token chunking with 80-token overlap, sentence-aware boundaries.
7. OpenAI text-embedding-3-large via OpenRouter, batches of 256 chunks, exponential backoff on 429s.
8. bm25s sparse index built over the whole corpus.
9. SQLite write in a single transaction. `parse_quality.json` quality report saved.
10. If `bibliography.bib` exists: auto-link bibkeys/title/authors/year to `sources` rows via `file = {…}` field matching.

**Output JSON schema:**
```json
{
  "thesis": "<name>",
  "indexed": {"new_pdfs": N, "unchanged_pdfs": N, "total_chunks": N, "ocr_pages": N, "vision_ocr_pages": N},
  "warnings": [{"pdf": "x.pdf", "issue": "page_offset_low_confidence|ocr_failed|encrypted_pdf|...", "...": "..."}],
  "cost_usd": 0.0151,
  "duration_seconds": 7.22,
  "bibkey_linking": {"linked": N, "not_found": [...], "mapped_pairs": N}
}
```

### `search` — hybrid retrieval over a thesis corpus

```
python -m rag search "<query>" --thesis <name> [options]
  --top <k>                  Final result count. Default 8.
  --window <n>               Sentences of context before/after each hit. Default 5.
  --filter-source <bibkey>   Restrict to one source (e.g. only rogers1983)
  --filter-year <range>      "2020-2026" or "<2010" or ">2020"
  --rerank                   Apply bge-reranker-v2-m3 cross-encoder stage
  --mode <auto|dense|bm25>   Force retrieval mode. Default auto (hybrid).
  --pretty                   Rich-table output instead of JSON
```

**Pipeline:** Embed query → dense top-50 from sqlite-vec + sparse top-50 from bm25s → RRF fusion to top-30 → filters applied (BEFORE the top-k cut, so filters don't accidentally empty results) → optional reranker on remaining → context expansion from `pages` table → BibKey resolution → JSON.

**Output JSON schema:**
```json
{
  "query": "...", "thesis": "<name>", "mode": "auto", "reranked": false,
  "total_hits": 8,
  "hits": [{
    "rank": 1, "score_fused": 0.89, "score_dense": 0.91, "score_bm25": 12.4, "score_rerank": null,
    "source": {"bibkey": "...", "title": "...", "authors": [...], "year": 2025, "filename": "..."},
    "location": {"pdf_page_start": 3, "pdf_page_end": 4,
                 "printed_page_start": 3, "printed_page_end": 4,
                 "print_offset_confidence": 1.0},
    "quality_score": 0.94, "ocr_origin": "native|tesseract|vision",
    "chunk_text": "...", "context_before": "...", "context_after": "...",
    "citation_suggestion": "\\parencite[S. 3]{rogersDiffusion1983}"
  }],
  "duration_ms": 412
}
```

The `citation_suggestion` field is the killer feature: ready-to-paste LaTeX with the printed page (not PDF page) already substituted. If `bibkey` is null (corpus not bib-linked yet), `citation_suggestion` is also null.

`score_dense` is `1/(1+L2_distance)`, monotonic with cosine for L2-normalized OpenAI embeddings but not equal to cosine. Use it for ranking only, not as a similarity threshold.

### `verify-quote` — plagiarism self-check

```
python -m rag verify-quote --thesis <name> [--text "<sentence>" | --tex <file>]
  --threshold-strict <f>   Jaccard/LCS threshold for STRICT_MATCH. Default 0.40.
  --threshold-fuzzy <f>    Dense-score threshold for FUZZY/THEMATIC_MATCH. Default 0.45.
  --top <k>                Embedding-broad-net candidate count. Default 20.
  --pretty                 Currently JSON pretty-print (table output deferred to v0.2)
```

**Pipeline:** Embed input → top-20 nearest chunks → for each chunk, split into sentences and compute best Jaccard, LCS, structural similarity against any sentence in the chunk → classify per-match.

**Severity classes (since v0.1.1, sentence-level matching):**
- `STRICT_MATCH`: jaccard ≥ 0.40 OR lcs ≥ 0.40 → near-quote, must be in quotation marks
- `FUZZY_MATCH`: dense_score ≥ 0.45 AND structural ≥ 0.40 → too-close paraphrase, rewrite or cite
- `THEMATIC_MATCH`: dense_score ≥ 0.45 only → same idea, cite the source for the concept
- `NO_MATCH`: nothing fired

**Output JSON schema:**
```json
{
  "thesis": "<name>", "input_text": "...", "verdict": "STRICT_MATCH|FUZZY_MATCH|THEMATIC_MATCH|NO_MATCH",
  "matches": [{
    "severity": "...", "jaccard": 0.4, "dense_score": 0.5, "lcs_ratio": 0.6, "structural_similarity": 0.6,
    "source": {"bibkey": "...", "filename": "...", "printed_page_start": 2},
    "matched_text": "<best matching sentence from the chunk>",
    "diff_preview": "<difflib ndiff of query vs match>",
    "recommendation": "Cite as: \\parencite[S. 2]{key}"
  }],
  "total_inspected": 20
}
```

### `extract-citations` — audit `\cite` commands in `.tex`

```
python -m rag extract-citations --thesis <name> --tex <file-or-dir> [options]
  --check-bib                Verify each cited bibkey exists in bibliography.bib
  --check-corpus             Verify each cited bibkey has an indexed source in the corpus DB
  --check-pages              DEPRECATED alias for --check-corpus, prints stderr warning
  --check-orphans            List bib entries that are never cited
  --strict                   Exit code 1 if any issue found
  --pretty                   Rich-table output instead of JSON
```

**Issue types reported:**
- `MISSING_BIBKEY`: cited key not in `.bib`. Includes `suggestion` with closest match.
- `BIBKEY_NOT_IN_CORPUS`: cited key in `.bib` but no source row in the corpus DB.
- `ORPHAN_BIB`: bib entry that is never cited.

`PAGE_CONTENT_MISMATCH` (semantic check whether the cited page actually contains the claimed content) is a spec promise deferred to v0.2.

### `corpus` — inventory of indexed sources

```
python -m rag corpus --thesis <name> [--pretty]
```

Lists every source with: bibkey, title, year, page count (PDF and printed), print_offset, print_offset_confidence, chunk count, average page-quality.

### `bib` — build or check `bibliography.bib`

```
python -m rag bib --thesis <name> [--build | --check | --reconcile] [--interactive] [--pretty]
  --build                    Lean-mode: assemble bibliography.bib from PDFs
  --check                    List bibkeys currently in bibliography.bib
  --reconcile                Reserved for v0.2 (currently a no-op stub)
  --interactive              Reserved for v0.2 (currently a no-op stub)
```

`--build` pipeline: extract DOI from PDF first 3 pages → reject placeholder DOIs (e.g. `10.1145/nnnnnnn.nnnnnnn`) → OpenAlex lookup → Crossref fallback → arXiv-ID lookup → title-search via PyMuPDF font-size analysis → manual_review fallback. Bibkeys collide-disambiguated with `a/b/c` suffix and a warning entry. After build, if a corpus DB exists, auto-link bibkeys to source rows.

## `overrides.toml` per-PDF manual corrections

When auto-detection fails for a PDF, place corrections in `thesen/<name>/overrides.toml`:

```toml
[pdf."rogers-1983.pdf"]
print_offset = 14
print_offset_confidence = 1.0

[pdf."some-scan.pdf"]
vision_ocr = true             # reserved for v2
```

The indexer reads these at build time. When a `print_offset` override is present, the auto-detection result is overridden and the low-confidence warning is suppressed (the override is treated as authoritative).

## Workflow when asked to write thesis content

1. Confirm which thesis (e.g. `fabian-rag-chatbot`). If unclear, ask.
2. Read `thesen/<name>/CLAUDE.md` for thesis-specific topic, mode, conventions, and TODOs.
3. Run `python -m rag corpus --thesis <name> --pretty` to know what is in the corpus.
4. For every concept you write about: `python -m rag search "<concept>" --thesis <name>`. Use the `citation_suggestion` strings directly.
5. After every paragraph that paraphrases a source: `python -m rag verify-quote --text "<sentence>" --thesis <name>`. If `STRICT_MATCH`: rewrite or quote. If `FUZZY_MATCH`: rewrite or add cite. If `THEMATIC_MATCH`: add cite for the idea, no quotation needed.
6. Before saving any `.tex` edits: `python -m rag extract-citations --tex tex/main.tex --thesis <name> --check-bib --check-corpus --check-orphans`.
7. If the user is in Lean mode and adds new PDFs: re-run `index` (incremental, fast) and re-run `bib --build` for the new entries.

## What NOT to do

- Do **not** edit anything inside `thesen/<name>/index/`. That is generated. Re-run `index` if it gets out of sync.
- Do **not** add bib entries by hand if the bib was auto-generated (Lean mode). Use `python -m rag bib`. In Premium mode the user owns the bib via Zotero.
- Do **not** read entire PDFs into your context. Use `search`. That is the whole point of this system.
- Do **not** invent citations. If `verify-quote` returns `NO_MATCH` and `search` returns no relevant hit, the claim has no source in the corpus. Tell the user.
- Do **not** trust a `citation_suggestion` with `print_offset_confidence < 0.7` blindly. The printed page may be off. Spot-check by comparing `chunk_text` content against the source.

## Installed extras and how to enable

- **Reranker** (`bge-reranker-v2-m3`, ~570 MB model, lazy-downloaded on first use): `uv sync --extra rerank`. Then call `search` with `--rerank`.
- **OCR** (Tesseract): comes via `brew install tesseract` plus the Python wrapper installed by default. Triggered automatically on low-quality pages.
- **Dev tools** (pytest, ruff): `uv sync --group dev`.

## Running tests and lint

```bash
uv run pytest -q                     # 70 tests, ~2s, no API calls (mocked)
uv run ruff check rag/ tests/        # 0 expected issues
```

## When things break

| Symptom | Fix |
|---|---|
| `OPENROUTER_API_KEY not set` | `cp .env.example .env`, add the key |
| `No index found. Run: python -m rag index --thesis <name>` | Just do that |
| `ocrmypdf not found` | `brew install ocrmypdf tesseract` |
| `Reranker requires the 'rerank' extra` | `uv sync --extra rerank` |
| Search returns `bibkey: null`, `citation_suggestion: null` | Bib not linked. In Lean mode: `python -m rag bib --thesis <name> --build`. In Premium mode: ensure your Zotero export has `file = {…}` fields (Better BibTeX writes them automatically). |
| Search returns 0 hits despite the corpus having the concept | Try `--mode bm25` (better for exact terms) or `--mode dense` (better for paraphrases). Try a different query phrasing. |
| `verify-quote` returns `NO_MATCH` for a sentence you know is in the corpus | The corpus may be stale. Re-run `index`. Check the page where you expect the match: `python -m rag search "<key phrase from sentence>" --thesis <name>`. |
| `EncryptedPDFError` warning during index | The PDF is password-protected. Decrypt with `qpdf --decrypt input.pdf output.pdf` and re-place. |
| Page-offset confidence is 0.5 with no override | Add `[pdf."<filename>"]\nprint_offset = N` to `overrides.toml`. Re-run `index`. |
| Wrong title or author on a Lean-mode bib entry | Edit `bibliography.bib` by hand. Re-run `python -m rag bib --thesis <name> --build` will not overwrite existing entries (idempotent). |

## Known limitations and open work

See `KNOWN_ISSUES.md` for the current list. v0.1.2 is the latest tag. Things explicitly NOT in v0.1.2 that downstream code may want to assume:
- `PAGE_CONTENT_MISMATCH` in `extract-citations` (semantic verification of cited pages)
- WordNet synonym stage in `verify-quote`
- `--pretty` for `index`, `verify-quote`, `bib` (still JSON pretty-printed)
- Vision-OCR via Gemini Flash
- Multi-thesis search (cross-corpus retrieval)
- MCP server wrapper

## Writing extension: skill layer + LaTeX templates

The system ships with a vendored skill library and five LaTeX thesis profiles. Skills live under `.claude/skills/` and auto-activate when Claude works in this repo. The bridge skill `bachelorarbeit-arbeitsweise` enforces the source-traceable workflow whenever you edit `thesen/<name>/tex/*.tex`.

**Available skills (auto-discovered):**

| Skill | When to use |
|---|---|
| `bachelorarbeit-arbeitsweise` (bridge, German) | Always when writing thesis content. Orchestrates rag search + verify-quote + extract-citations + Brave/Firecrawl |
| `scientific-writing` | Einleitung, Theorie, Fazit |
| `scientific-critical-thinking` | Diskussion, Limitationen |
| `literature-review` | Theoretischer Rahmen, Stand der Forschung |
| `hypothesis-generation` | Hypothesenkapitel (empirisch) |
| `statistical-analysis` | Methodik + Ergebnisse (quantitativ) |
| `market-research-reports` | Marktanalyse-Kapitel (Marketing/BWL) |
| `scientific-visualization` | Charts und Abbildungen |
| `scholar-evaluation` | Selbst-Audit vor Abgabe |
| `scientific-brainstorming` | Forschungsfrage-Phase |
| `peer-review` | Selbst-Review vor Abgabe |

Each vendored skill ships with `references/` (universal English content from K-Dense) plus a German anchor `DEUTSCHE-KONVENTIONEN.md` covering DACH conventions specific to that skill. The bridge skill is repo-native and never overwritten by sync.

**LaTeX profiles** in `templates/latex/<profil>/` (with shared `_common/` layer):

- `technisch-informatik`
- `empirisch-quantitativ`
- `theoretisch-konzeptionell`
- `marketing-case-study`
- `mixed-methods-mayring`

Initialize a new thesis with:

```
python -m rag thesis init --name <slug> --template <profil> [--mode premium|lean]
```

Compile with `cd thesen/<slug>/tex && latexmk -lualatex main.tex` (requires MacTeX or equivalent).

**K-Dense skill updates:** `tools/skills-sync.sh` re-vendors at a pinned commit. Update `PINNED_COMMIT` in the script and re-run. Manual conflict resolution if upstream restructures.

## Output conventions recap

- Exit code: 0 success, 1 audit-strict failure (only `extract-citations --strict`), 2 environment/index missing.
- JSON to stdout, human errors to stderr.
- Logs land in `thesen/<name>/index/parse_quality.json` (NOT `build.log` despite some older docs).
- All commands are idempotent. `index` and `bib --build` re-run safely.
