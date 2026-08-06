# CLAUDE.md (Thesis Brief)

> Copy this folder to `thesen/<your-name>/` and edit this file.
>
> See repo-root `CLAUDE.md` for the full system reference. This file is for thesis-specific context.

## Thesis topic

(One paragraph: research question, scope, why it matters. Keep it short, this is a brief.)

## Mode

Pick one and remove the other. Mode determines the bib workflow.

- [ ] **Premium**: User exports their Zotero collection to `bibliography.bib` via Better BibTeX with "Export with Auto-Update". Better BibTeX writes `file = {filename.pdf}` fields automatically; the indexer auto-links bibkeys/title/authors/year on every `python -m rag index` run.
- [ ] **Lean**: User drops only PDFs. Run `python -m rag bib --thesis <name> --build` to assemble the bib via DOI/OpenAlex/Crossref/title-search. Auto-linking happens at the end of the build.

## Profile

This thesis uses the `<profil>` LaTeX profile. See `templates/latex/<profil>/README.md` for the chapter structure and profile-specific helpers.

## Writing skills

When you (Claude) write content in this thesis folder, the bridge skill `bachelorarbeit-arbeitsweise` activates automatically and enforces:
- `python -m rag search` before every claim
- `python -m rag verify-quote` after every paragraph
- `python -m rag extract-citations --strict` before every commit
- Brave/Firecrawl MCPs only for material outside the corpus, always with URL + Stand-Datum

## Chapter structure

1. Introduction
2. Theoretical Foundations
3. Methodology
4. Results
5. Discussion
6. Conclusion

## Status

- Chapter 1: not started
- Chapter 2: not started
- Chapter 3: not started

## Conventions

- **Citation style:** APA 7th in BibLaTeX. `\parencite[S. X]{key}` for German page references. `\textcite[S. X]{key}` for narrative.
- **Language:** German prose, English source citations are fine.
- **Quotation marks:** German `,,quote''`.
- **Special advisor preferences:** none yet.

## Source notes

Use `overrides.toml` (in this folder) for per-PDF corrections that the indexer should pick up. Examples:

```toml
[pdf."rogers-1983.pdf"]
print_offset = 14
print_offset_confidence = 1.0
```

Add a TOML entry whenever `corpus --pretty` shows `print_offset_confidence` below 0.7 for a PDF you care about.

## Active TODO

- (List what is in flight right now. Update as you go.)

## Specific instructions for Claude

(Anything unusual, e.g. "use only post-2020 sources", "advisor wants empirical, not theoretical citations", "do not cite blog posts even when they are in the corpus".)

## Useful commands for this thesis

```bash
# Inventory
uv run python -m rag corpus --thesis <name> --pretty

# Search (replace concept)
uv run python -m rag search "your concept" --thesis <name> --top 8 --pretty

# Verify a sentence you just wrote
uv run python -m rag verify-quote --text "..." --thesis <name>

# Audit citations before any commit to .tex
uv run python -m rag extract-citations \
  --tex tex/main.tex --thesis <name> \
  --check-bib --check-corpus --check-orphans --pretty
```
