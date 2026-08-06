import pytest

from rag.cli import build_parser


def test_parser_has_index_subcommand():
    parser = build_parser()
    args = parser.parse_args(["index", "--thesis", "demo"])
    assert args.command == "index"
    assert args.thesis == "demo"


def test_parser_has_search_subcommand():
    parser = build_parser()
    args = parser.parse_args(["search", "RAG embeddings", "--thesis", "demo", "--top", "5"])
    assert args.command == "search"
    assert args.query == "RAG embeddings"
    assert args.top == 5


def test_parser_default_top_is_8():
    parser = build_parser()
    args = parser.parse_args(["search", "x", "--thesis", "demo"])
    assert args.top == 8


def test_parser_version():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--version"])
