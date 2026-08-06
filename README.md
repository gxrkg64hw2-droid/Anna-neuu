# Bachelorarbeits-System

> # ⚠️ NOTICE TO GITHUB TRUST & SAFETY / GITHUB MODERATION ⚠️
>
> **This repository is PRIVATE. It is a personal academic-backup of in-progress thesis work.**
>
> - The repository owner (`nicremo`) is a Bachelor student at DHBW Mannheim, Germany.
> - The PDF files under `thesen/*/pdfs/` and `_Luana/.../Literatur/` are research literature accessed under a legitimate university library license (DHBW campus license, EBSCO, Springer, JSTOR via institutional access).
> - These PDFs are used solely as a personal corpus for retrieval-augmented citation work during the writing of one Bachelor thesis. They are not redistributed, not shared with the public, and not made accessible to any third party outside the repository owner. The repository is set to PRIVATE on GitHub for exactly this reason.
> - Personal data appearing in `thesen/*/PROJEKTUEBERSICHT.md` and `thesen/*/quelldokumente/` (matriculation numbers, addresses, phone numbers, names of students and supervisors) is used with the consent of the persons involved and serves only as working metadata for the thesis tooling.
> - This repository has no public access, no GitHub Pages site, no published GitHub Actions output, and no tagged releases that contain the literature PDFs as downloadable artifacts.
>
> **Please do not initiate a takedown without first contacting the repository owner (GitHub: @nicremo, email: see commit metadata). The repository can be made PDF-free within minutes upon request, while preserving the open-source CLI tooling that lives independently of any specific thesis.**
>
> _End of notice._

---

A CLI toolkit that extends Claude Code's capabilities for academic thesis writing. Hybrid semantic+lexical search over a PDF corpus, plagiarism self-check, citation auditing, automatic BibTeX generation. Designed to be operated by Claude, not by the user directly.

## What it does

- **Index** a folder of PDFs into a single SQLite + sqlite-vec file: PyMuPDF text extraction, automatic OCR fallback for scans, sentence-aware 512-token chunking, OpenAI text-embedding-3-large via OpenRouter, bm25s sparse index built in parallel.
- **Search** by hybrid retrieval: dense (sqlite-vec) + sparse (bm25s) merged via Reciprocal Rank Fusion, with an optional bge-reranker-v2-m3 cross-encoder stage. Returns ranked hits with exact printed-page numbers and ready-to-paste `\parencite` strings.
- **Verify-quote** a sentence you just wrote against the whole corpus: sentence-level Jaccard, LCS, dense similarity, structural similarity. Catches paraphrases that differ by a few words.
- **Extract-citations** scans `.tex` files: missing bibkeys, orphaned bib entries, bibkeys that have no source in the corpus.
- **Bib build** assembles a `bibliography.bib` from PDFs alone: DOI extraction → OpenAlex → Crossref → arXiv-ID → title-search via PyMuPDF font-size analysis → manual review fallback.
- **Auto-link** the resulting bibkeys, titles, authors, and years to the corpus DB so search hits return real citation suggestions.
- **Per-thesis isolation**: each thesis lives under `thesen/<name>/` with its own PDFs, bib, index, and CLAUDE.md brief.

## Setup

```bash
brew install uv tesseract
uv sync                              # runtime deps
uv sync --extra rerank               # optional bge-reranker (570 MB model)
uv sync --group dev                  # pytest + ruff
cp .env.example .env                 # add OPENROUTER_API_KEY=sk-or-v1-...
```

## Usage

The toolkit is operated by a Claude Code session. Read [`CLAUDE.md`](./CLAUDE.md) for the full operator manual: every command, every flag, every JSON output schema, the two operating modes, the workflow for writing thesis prose with live citation lookup.

```bash
uv run python -m rag --help                                          # usage
uv run python -m rag index --thesis <name>                           # build index
uv run python -m rag search "<query>" --thesis <name> --pretty       # find sources
uv run python -m rag verify-quote --text "..." --thesis <name>       # plagiarism check
uv run python -m rag extract-citations --tex main.tex --thesis <name> --check-bib
```

## Architecture in one paragraph

`rag/` is a single Python package. CLI subcommands lazy-import their dependencies so cold start stays fast. Per-thesis storage is a single SQLite file (`corpus.db`) with `sqlite-vec` for vector similarity, plus a sidecar bm25s index. Embeddings are produced via OpenRouter routing to OpenAI text-embedding-3-large, batched and retried with exponential backoff. PyMuPDF handles page text and font-size analysis; ocrmypdf wraps Tesseract for low-quality pages. RRF fuses dense and sparse rankings, an optional bge-reranker-v2-m3 cross-encoder reorders the top candidates. Verify-quote operates at sentence granularity within candidate chunks. Extract-citations parses `\parencite[…]{…}` family commands with regex.

## Writing Extension (since v0.2.0)

Beyond retrieval and citation, the system now ships a writing-skill layer and five LaTeX thesis templates.

**Skill library** under `.claude/skills/`: ten K-Dense scientific-writing skills (vendored, MIT, DACH-adapted) plus a German bridge skill `bachelorarbeit-arbeitsweise` that enforces source-traceability on every paragraph.

**LaTeX profiles** under `templates/latex/`: five thesis archetypes (technisch-informatik, empirisch-quantitativ, theoretisch-konzeptionell, marketing-case-study, mixed-methods-mayring) sharing a `_common/` layer with KOMA-Script + biblatex (APA-DE) + csquotes + lualatex setup.

**One new CLI command:**

```
python -m rag thesis init --name <slug> --template <profil> [--mode premium|lean]
```

scaffolds a new thesis folder ready for `latexmk -lualatex main.tex`.

See `docs/superpowers/specs/2026-05-06-thesis-writing-extension-design.md` for the design rationale.

## Releases

- **v0.1.0**: initial MVP, all commands functional.
- **v0.1.1**: real-world bug fixes: title extraction via font-size, bibkey auto-linking, sentence-level verify-quote, OCR wiring, overrides.toml.
- **v0.1.2**: quick wins: `--pretty` Rich tables, filter-before-top-k, encrypted PDF handling, German umlaut chapter markers, quality-score normalization to 0-1, deps cleanup.

## Documentation tree

- [`CLAUDE.md`](./CLAUDE.md) - full operator manual for Claude (commands, flags, JSON schemas, modes, troubleshooting)
- [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md) - open items, deferred features
- [`thesen/_template/CLAUDE.md`](./thesen/_template/CLAUDE.md) - per-thesis brief template
- [`docs/superpowers/specs/2026-05-06-bachelor-thesis-citation-system-design.md`](./docs/superpowers/specs/) - full design spec
- [`docs/superpowers/plans/2026-05-06-bachelor-thesis-citation-toolkit.md`](./docs/superpowers/plans/) - implementation plan

## License

PyMuPDF is AGPL. Acceptable for personal academic use. For commercial reuse, swap to `pypdfium2` (BSD) at the parser interface in `rag/parsers/pdf.py`.
