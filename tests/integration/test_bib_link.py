"""Test that bib --build also populates sources.bibkey when an index exists."""
from __future__ import annotations

import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from rag.config import Config
from rag.indexer.build import build_index
from rag.metadata.bib import link_bibkeys_to_sources
from tests.fixtures.make_test_pdf import build_simple_pdf


@pytest.fixture
def indexed_thesis(tmp_path):
    thesis = tmp_path / "thesen" / "demo"
    (thesis / "pdfs").mkdir(parents=True)
    (thesis / "index").mkdir()
    pdf = thesis / "pdfs" / "test.pdf"
    build_simple_pdf(pdf, ["Some content here."])
    cfg = Config(repo_root=tmp_path, openrouter_api_key="sk-or-test", google_api_key=None)
    with patch("rag.indexer.build.EmbeddingClient") as mock_cls:
        client = MagicMock()
        client.embed_batch.side_effect = lambda texts: [[0.1] * 3072 for _ in texts]
        mock_cls.return_value = client
        build_index(cfg, "demo", rebuild=False, only=None, skip_ocr=True, vision_ocr=None)
    return cfg, "demo", thesis


def test_link_bibkeys_to_sources_via_file_field(indexed_thesis):
    cfg, thesis_name, thesis_root = indexed_thesis
    bib = thesis_root / "bibliography.bib"
    bib.write_text(
        "@article{myKey2024,\n"
        "  title = {Test},\n"
        "  year = {2024},\n"
        "  file = {test.pdf}\n"
        "}\n"
    )
    result = link_bibkeys_to_sources(cfg, thesis_name)
    assert result["linked"] == 1

    # Verify in db
    conn = sqlite3.connect(str(cfg.thesis_corpus_db(thesis_name)))
    row = conn.execute("SELECT bibkey FROM sources WHERE filename=?", ("test.pdf",)).fetchone()
    conn.close()
    assert row[0] == "myKey2024"
