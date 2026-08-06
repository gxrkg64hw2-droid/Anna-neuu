"""CLI dispatcher for `python -m rag <command>`."""
from __future__ import annotations

import argparse
import json
import sys

from rag import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rag",
        description="Bachelor thesis citation toolkit",
    )
    parser.add_argument("--version", action="version", version=f"rag {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    # index
    p_index = sub.add_parser("index", help="Build or refresh corpus index")
    p_index.add_argument("--thesis", required=True)
    p_index.add_argument("--rebuild", action="store_true")
    p_index.add_argument("--only", default=None, help="PDF glob filter")
    p_index.add_argument("--skip-ocr", action="store_true")
    p_index.add_argument("--vision-ocr", default=None)
    p_index.add_argument("--pretty", action="store_true")

    # search
    p_search = sub.add_parser("search", help="Hybrid retrieval over a thesis corpus")
    p_search.add_argument("query")
    p_search.add_argument("--thesis", required=True)
    p_search.add_argument("--top", type=int, default=8)
    p_search.add_argument("--window", type=int, default=5)
    p_search.add_argument("--filter-source", default=None)
    p_search.add_argument("--filter-year", default=None)
    p_search.add_argument("--rerank", action="store_true")
    p_search.add_argument("--mode", choices=["auto", "dense", "bm25"], default="auto")
    p_search.add_argument("--pretty", action="store_true")

    # verify-quote
    p_vq = sub.add_parser("verify-quote", help="Plagiarism self-check")
    p_vq.add_argument("--thesis", required=True)
    src = p_vq.add_mutually_exclusive_group(required=True)
    src.add_argument("--text")
    src.add_argument("--tex")
    p_vq.add_argument("--threshold-strict", type=float, default=0.40)
    p_vq.add_argument("--threshold-fuzzy", type=float, default=0.45)
    p_vq.add_argument("--top", type=int, default=20)
    p_vq.add_argument("--pretty", action="store_true")

    # extract-citations
    p_ec = sub.add_parser("extract-citations", help="Audit citations in .tex against .bib")
    p_ec.add_argument("--thesis", required=True)
    p_ec.add_argument("--tex", required=True)
    p_ec.add_argument("--check-bib", action="store_true")
    p_ec.add_argument("--check-pages", action="store_true",
                      help="Deprecated alias for --check-corpus (use --check-corpus going forward)")
    p_ec.add_argument("--check-corpus", action="store_true",
                      help="Verify each cited bibkey has a source in the corpus index")
    p_ec.add_argument("--check-orphans", action="store_true")
    p_ec.add_argument(
        "--check-page-content",
        action="store_true",
        help=(
            "Semantic check: verify that the cited page actually matches "
            "the surrounding paragraph"
        ),
    )
    p_ec.add_argument(
        "--page-content-threshold",
        type=float,
        default=0.30,
        metavar="THRESHOLD",
        help=(
            "Cosine similarity threshold below which a citation is flagged as "
            "PAGE_CONTENT_MISMATCH (default: 0.30)"
        ),
    )
    p_ec.add_argument("--strict", action="store_true")
    p_ec.add_argument("--pretty", action="store_true")

    # corpus
    p_corpus = sub.add_parser("corpus", help="List indexed sources")
    p_corpus.add_argument("--thesis", required=True)
    p_corpus.add_argument("--pretty", action="store_true")

    # bib
    p_bib = sub.add_parser("bib", help="Build or check bibliography.bib")
    p_bib.add_argument("--thesis", required=True)
    bibgrp = p_bib.add_mutually_exclusive_group(required=True)
    bibgrp.add_argument("--build", action="store_true")
    bibgrp.add_argument("--check", action="store_true")
    bibgrp.add_argument("--reconcile", action="store_true")
    p_bib.add_argument("--interactive", action="store_true")
    p_bib.add_argument("--pretty", action="store_true")

    # thesis
    p_thesis = sub.add_parser("thesis", help="Thesis scaffolding (init, etc.)")
    thesis_sub = p_thesis.add_subparsers(dest="thesis_cmd", required=True)

    p_thesis_init = thesis_sub.add_parser(
        "init",
        help="Initialize a new thesis folder from template + LaTeX profile",
    )
    p_thesis_init.add_argument("--name", required=True, help="thesis slug, e.g. fabian-rag-chatbot")
    p_thesis_init.add_argument(
        "--template",
        required=True,
        choices=[
            "technisch-informatik",
            "empirisch-quantitativ",
            "theoretisch-konzeptionell",
            "marketing-case-study",
            "mixed-methods-mayring",
        ],
        help="LaTeX profile to scaffold",
    )
    p_thesis_init.add_argument(
        "--mode",
        choices=["premium", "lean"],
        default="lean",
        help="Mode marker recorded in thesis CLAUDE.md (default: lean)",
    )
    p_thesis_init.add_argument("--pretty", action="store_true", help="JSON pretty-print")

    return parser


def emit_json(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Lazy imports so commands only load what they need
    if args.command == "index":
        from rag.indexer.build import run_index
        return run_index(args)
    if args.command == "search":
        from rag.search.query import run_search
        return run_search(args)
    if args.command == "verify-quote":
        from rag.tools.verify_quote import run_verify_quote
        return run_verify_quote(args)
    if args.command == "extract-citations":
        from rag.tools.extract_citations import run_extract_citations
        return run_extract_citations(args)
    if args.command == "corpus":
        from rag.tools.corpus import run_corpus
        return run_corpus(args)
    if args.command == "bib":
        from rag.metadata.bib import run_bib
        return run_bib(args)
    if args.command == "thesis":
        if args.thesis_cmd == "init":
            from rag.thesis.init import run_thesis_init
            return run_thesis_init(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
