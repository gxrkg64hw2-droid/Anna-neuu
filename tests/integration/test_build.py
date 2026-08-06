import shutil
import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from rag.config import Config
from rag.indexer.build import build_index
from tests.fixtures.make_test_pdf import build_simple_pdf


@pytest.fixture
def fake_thesis(tmp_path):
    thesis = tmp_path / "thesen" / "demo"
    (thesis / "pdfs").mkdir(parents=True)
    (thesis / "index").mkdir()
    pdf = thesis / "pdfs" / "rogers.pdf"
    build_simple_pdf(pdf, [
        "Rogers (1983) introduced the diffusion of innovations theory.",
        "The S-shaped curve describes adoption over time.",
        "Innovations have five attributes: relative advantage, compatibility, complexity, trialability, observability.",  # noqa: E501
    ])
    cfg = Config(
        repo_root=tmp_path,
        openrouter_api_key="sk-or-test",
        google_api_key=None,
    )
    return cfg, "demo"


@patch("rag.indexer.build.EmbeddingClient")
def test_build_index_creates_db_with_chunks(mock_client_cls, fake_thesis):
    cfg, thesis_name = fake_thesis
    fake_client = MagicMock()
    fake_client.embed_batch.side_effect = lambda texts: [[0.0] * 3072 for _ in texts]
    mock_client_cls.return_value = fake_client

    result = build_index(cfg, thesis_name, rebuild=False, only=None,
                        skip_ocr=True, vision_ocr=None)

    assert result["indexed"]["new_pdfs"] == 1
    assert result["indexed"]["total_chunks"] >= 1

    db = cfg.thesis_corpus_db(thesis_name)
    assert db.exists()


@patch("rag.indexer.build.EmbeddingClient")
def test_build_replaces_changed_pdf(mock_client_cls, fake_thesis):
    cfg, thesis_name = fake_thesis
    fake_client = MagicMock()
    fake_client.embed_batch.side_effect = lambda texts: [[0.0] * 3072 for _ in texts]
    mock_client_cls.return_value = fake_client

    # First build
    build_index(cfg, thesis_name, rebuild=False, only=None,
                skip_ocr=True, vision_ocr=None)

    import sqlite3

    # Modify the PDF (different content -> different SHA)
    pdf = cfg.thesis_pdfs_dir(thesis_name) / "rogers.pdf"
    from tests.fixtures.make_test_pdf import build_simple_pdf
    build_simple_pdf(pdf, ["Completely different content now."])

    # Second build
    result = build_index(cfg, thesis_name, rebuild=False, only=None,
                         skip_ocr=True, vision_ocr=None)
    assert result["indexed"]["new_pdfs"] == 1  # re-indexed
    assert result["indexed"]["unchanged_pdfs"] == 0

    conn = sqlite3.connect(str(cfg.thesis_corpus_db(thesis_name)))
    sources_count = conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    chunks_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    conn.close()
    assert sources_count == 1, "Should have exactly one source after re-index"
    # Chunks should reflect the NEW content (different from chunks_before is fine)
    assert chunks_count >= 1


def test_overrides_toml_print_offset(tmp_path):
    """overrides.toml should override page-offset detection."""
    thesis = tmp_path / "thesen" / "ovr"
    (thesis / "pdfs").mkdir(parents=True)
    (thesis / "index").mkdir()
    pdf = thesis / "pdfs" / "scan.pdf"
    build_simple_pdf(pdf, ["random text page A", "random text page B", "random text page C"])
    # No chapter marker, normally returns offset=0 confidence=0.5
    (thesis / "overrides.toml").write_text(
        '[pdf."scan.pdf"]\nprint_offset = 2\nprint_offset_confidence = 1.0\n'
    )

    cfg = Config(repo_root=tmp_path, openrouter_api_key="sk-or-test", google_api_key=None)
    with patch("rag.indexer.build.EmbeddingClient") as mock_cls:
        client = MagicMock()
        client.embed_batch.side_effect = lambda texts: [[0.1] * 3072 for _ in texts]
        mock_cls.return_value = client
        result = build_index(cfg, "ovr", rebuild=False, only=None,
                             skip_ocr=True, vision_ocr=None)

    # Override should suppress the low-confidence warning
    page_warnings = [w for w in result["warnings"] if w["issue"] == "page_offset_low_confidence"]
    assert page_warnings == []

    # Verify the override landed in the DB
    conn = sqlite3.connect(str(cfg.thesis_corpus_db("ovr")))
    row = conn.execute("SELECT print_offset, print_offset_confidence FROM sources").fetchone()
    conn.close()
    assert row[0] == 2
    assert row[1] == 1.0


@pytest.mark.skipif(shutil.which("ocrmypdf") is None, reason="ocrmypdf not installed")
def test_ocr_runs_on_low_quality_pages(tmp_path):
    """Build a synthetic image-only PDF and verify the OCR pipeline wiring runs."""
    import pymupdf

    pdf_path = tmp_path / "image.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    # Insert a blank white pixmap to simulate a scan with no extractable text
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 200, 100))
    pix.clear_with(255)  # white
    page.insert_image(pymupdf.Rect(72, 72, 272, 172), pixmap=pix)
    doc.save(str(pdf_path))
    doc.close()

    from rag.parsers.pdf import extract_pages
    from rag.parsers.quality import score_page

    pages = extract_pages(pdf_path)
    if score_page(pages[0].text) >= 0.4:
        pytest.skip("Synthetic image-only PDF unexpectedly extracted text; OCR path not exercised")

    from rag.parsers.ocr import needs_ocr, run_ocr_on_pdf

    low = needs_ocr([0.0])
    out_path = tmp_path / "ocred.pdf"
    result = run_ocr_on_pdf(pdf_path, out_path, low, languages="eng")
    assert result["skipped"] is False
    assert out_path.exists()
