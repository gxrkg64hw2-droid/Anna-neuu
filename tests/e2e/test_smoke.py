"""End-to-end smoke test: index -> search -> verify-quote -> extract-citations."""
from unittest.mock import MagicMock, patch

import pytest

from rag.config import Config
from rag.indexer.build import build_index
from rag.search.query import search_corpus
from rag.tools.extract_citations import audit
from rag.tools.verify_quote import verify_quote
from tests.fixtures.make_test_pdf import build_simple_pdf


def _fake_embed(texts):
    return [[(hash(t) % 1000) / 1000.0] * 3072 for t in texts]


@pytest.fixture
def real_thesis(tmp_path):
    thesis_root = tmp_path / "thesen" / "smoke"
    (thesis_root / "pdfs").mkdir(parents=True)
    (thesis_root / "index").mkdir()
    (thesis_root / "tex").mkdir()
    pdfs = [
        ("rogers.pdf", [
            "Rogers (1983) introduced the diffusion of innovations theory.",
            "The S-shaped curve describes adoption over time.",
        ]),
        ("lewis.pdf", [
            "Lewis et al. introduced retrieval-augmented generation in 2020.",
            "RAG combines parametric and non-parametric memory."
        ]),
        ("scheuer.pdf", [
            "Scheuer 2020 entwickelt das KI-Akzeptanzmodell KIAM.",
            "Vertrauen und Transparenz sind zentrale Faktoren."
        ]),
        ("davis.pdf", [
            "Davis 1989 proposed the Technology Acceptance Model.",
            "Perceived usefulness predicts adoption.",
        ]),
        ("markham.pdf", [
            "Markham 2010 frames the Valley of Death in product innovation.",
            "Research-to-practice transitions often fail at scaling.",
        ]),
    ]
    for fname, pages in pdfs:
        build_simple_pdf(thesis_root / "pdfs" / fname, pages)

    bib = thesis_root / "bibliography.bib"
    bib.write_text(
        "@article{rogersDiffusion1983,\n  title={Diffusion of Innovations},\n  year={1983}\n}\n"
        "@article{lewisRetrievalAugmented2020,\n  title={Retrieval-Augmented Generation},"
        "\n  year={2020}\n}\n"
    )

    cfg = Config(repo_root=tmp_path, openrouter_api_key="sk-or-test", google_api_key=None)
    return cfg, "smoke", thesis_root


@patch("rag.indexer.build.EmbeddingClient")
@patch("rag.search.query.EmbeddingClient")
@patch("rag.tools.verify_quote.EmbeddingClient")
def test_smoke_full_pipeline(mock_vq, mock_search, mock_idx, real_thesis):
    cfg, thesis, root = real_thesis
    for mock in (mock_idx, mock_search, mock_vq):
        c = MagicMock()
        c.embed_batch.side_effect = _fake_embed
        mock.return_value = c

    # 1. Index
    idx_result = build_index(cfg, thesis, rebuild=False, only=None,
                              skip_ocr=True, vision_ocr=None)
    assert idx_result["indexed"]["new_pdfs"] == 5

    # 2. Search
    sr = search_corpus(cfg, thesis, query="diffusion of innovations",
                        top=3, window=2, mode="auto",
                        filter_source=None, filter_year=None, rerank=False)
    assert sr["total_hits"] >= 1

    # 3. Verify-quote
    vq = verify_quote(
        cfg, thesis,
        text="Rogers (1983) introduced the diffusion of innovations theory.",
        threshold_strict=0.65, threshold_fuzzy=0.82, top=10,
    )
    assert vq["verdict"] in ("STRICT_MATCH", "FUZZY_MATCH")

    # 4. Extract-citations on a fake .tex
    tex = root / "tex" / "section.tex"
    tex.write_text(r"As Rogers \parencite[S. 21]{rogersDiffusion1983} notes...")
    ec = audit(cfg, thesis, tex=tex,
                check_bib=True, check_pages=False, check_orphans=True)
    assert ec["total_citations"] == 1
