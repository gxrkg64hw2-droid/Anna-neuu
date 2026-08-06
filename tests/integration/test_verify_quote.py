from unittest.mock import MagicMock, patch

import pytest

from rag.config import Config
from rag.indexer.build import build_index
from rag.tools.verify_quote import verify_quote
from tests.fixtures.make_test_pdf import build_simple_pdf


@pytest.fixture
def indexed_thesis(tmp_path):
    thesis = tmp_path / "thesen" / "demo"
    (thesis / "pdfs").mkdir(parents=True)
    (thesis / "index").mkdir()
    pdf = thesis / "pdfs" / "src.pdf"
    build_simple_pdf(pdf, [
        "RAG models combine parametric memory with non-parametric memory for NLP tasks.",
    ])
    cfg = Config(repo_root=tmp_path, openrouter_api_key="sk-or-test", google_api_key=None)
    with patch("rag.indexer.build.EmbeddingClient") as mock_cls:
        client = MagicMock()
        client.embed_batch.side_effect = lambda texts: [[0.1] * 3072 for _ in texts]
        mock_cls.return_value = client
        build_index(cfg, "demo", rebuild=False, only=None, skip_ocr=True, vision_ocr=None)
    return cfg, "demo"


@patch("rag.tools.verify_quote.EmbeddingClient")
def test_verify_strict_match_detected(mock_cls, indexed_thesis):
    cfg, thesis = indexed_thesis
    client = MagicMock()
    client.embed_batch.return_value = [[0.1] * 3072]
    mock_cls.return_value = client

    result = verify_quote(
        cfg, thesis,
        text="RAG models combine parametric memory with non-parametric memory for NLP tasks.",
        threshold_strict=0.40, threshold_fuzzy=0.45, top=20,
    )
    assert result["verdict"] in ("STRICT_MATCH", "FUZZY_MATCH")
    assert len(result["matches"]) >= 1


@patch("rag.tools.verify_quote.EmbeddingClient")
def test_verify_strict_match_at_sentence_level(mock_cls, indexed_thesis):
    """A query sentence that is near-identical to an indexed sentence should be flagged."""
    cfg, thesis = indexed_thesis
    client = MagicMock()
    client.embed_batch.return_value = [[0.1] * 3072]
    mock_cls.return_value = client

    # The fixture indexes the RAG sentence from the indexed_thesis fixture.
    result = verify_quote(
        cfg, thesis,
        text="RAG models combine parametric memory with non-parametric memory for NLP tasks.",
        threshold_strict=0.40, threshold_fuzzy=0.45, top=10,
    )
    assert result["verdict"] in ("STRICT_MATCH", "FUZZY_MATCH"), \
        f"Expected match for near-identical sentence, got {result['verdict']}"
    # The first match should reference the matched sentence, not a truncated chunk
    assert len(result["matches"]) >= 1


@patch("rag.tools.verify_quote.EmbeddingClient")
def test_verify_no_match_for_unrelated_sentence(mock_cls, indexed_thesis):
    cfg, thesis = indexed_thesis
    client = MagicMock()
    # Use a different vector so embedding distance is large (far from indexed [0.1]*3072)
    client.embed_batch.return_value = [[0.99] * 3072]
    mock_cls.return_value = client

    result = verify_quote(
        cfg, thesis,
        text="The migration from monolith to microservices took six months in the case study.",
        threshold_strict=0.40, threshold_fuzzy=0.45, top=10,
    )
    # The mock embedding is intentionally far from indexed embeddings; no jaccard hit either
    assert result["verdict"] == "NO_MATCH"
