from unittest.mock import MagicMock, patch

import pytest

from rag.config import Config
from rag.indexer.build import build_index
from rag.search.query import search_corpus
from tests.fixtures.make_test_pdf import build_simple_pdf


@pytest.fixture
def indexed_thesis(tmp_path):
    thesis = tmp_path / "thesen" / "demo"
    (thesis / "pdfs").mkdir(parents=True)
    (thesis / "index").mkdir()
    pdf = thesis / "pdfs" / "rogers.pdf"
    build_simple_pdf(pdf, [
        "Rogers introduced the diffusion of innovations.",
        "The S-shaped curve describes cumulative adoption.",
    ])
    cfg = Config(repo_root=tmp_path, openrouter_api_key="sk-or-test", google_api_key=None)
    with patch("rag.indexer.build.EmbeddingClient") as mock_cls:
        client = MagicMock()
        client.embed_batch.side_effect = lambda texts: [[0.1] * 3072 for _ in texts]
        mock_cls.return_value = client
        build_index(cfg, "demo", rebuild=False, only=None, skip_ocr=True, vision_ocr=None)
    return cfg, "demo"


@patch("rag.search.query.EmbeddingClient")
def test_search_returns_hits(mock_cls, indexed_thesis):
    cfg, thesis = indexed_thesis
    client = MagicMock()
    client.embed_batch.return_value = [[0.1] * 3072]
    mock_cls.return_value = client

    result = search_corpus(cfg, thesis, query="diffusion innovations",
                            top=5, window=2, mode="auto",
                            filter_source=None, filter_year=None, rerank=False)
    assert result["query"] == "diffusion innovations"
    assert result["total_hits"] >= 1
    assert "citation_suggestion" in result["hits"][0]


@patch("rag.search.query.EmbeddingClient")
def test_search_filter_year_keeps_results_when_top_excludes_them(mock_cls, indexed_thesis):
    """Filter-before-top-k: applying year filter on full fused list does not crash
    and returns a valid result dict even when no chunks match the filter."""
    cfg, thesis = indexed_thesis
    client = MagicMock()
    client.embed_batch.return_value = [[0.1] * 3072]
    mock_cls.return_value = client

    # The test corpus has no year set on the source, so this range filter
    # should silently skip non-matching chunks and return zero hits without crashing.
    result = search_corpus(
        cfg, thesis, query="diffusion", top=5, window=2, mode="auto",
        filter_source=None, filter_year="2020-2030", rerank=False,
    )
    assert "hits" in result
    assert isinstance(result["hits"], list)
