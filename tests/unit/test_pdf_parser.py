import pymupdf

from rag.parsers.pdf import extract_arxiv_id, extract_pages, extract_title_candidates
from tests.fixtures.make_test_pdf import build_simple_pdf


def test_extract_pages_returns_one_entry_per_page(tmp_path):
    pdf = tmp_path / "demo.pdf"
    build_simple_pdf(pdf, ["Hello world.", "Second page text."])
    pages = extract_pages(pdf)
    assert len(pages) == 2
    assert "Hello world" in pages[0].text
    assert "Second page" in pages[1].text


def test_extract_pages_uses_1_indexed_numbering(tmp_path):
    pdf = tmp_path / "demo.pdf"
    build_simple_pdf(pdf, ["A", "B", "C"])
    pages = extract_pages(pdf)
    assert [p.pdf_page for p in pages] == [1, 2, 3]


def test_extract_pages_preserves_word_count(tmp_path):
    pdf = tmp_path / "demo.pdf"
    build_simple_pdf(pdf, ["one two three four five six"])
    pages = extract_pages(pdf)
    assert pages[0].word_count == 6


def test_extract_title_candidates_returns_largest_font_first(tmp_path):
    """Build a PDF with a large title and small body text. Title should rank first."""
    pdf_path = tmp_path / "titled.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "The Big Important Title", fontsize=20)
    page.insert_text((72, 120), "Some Author Name and Another Author", fontsize=11)
    page.insert_text((72, 160), "Body text body text body text " * 5, fontsize=10)
    doc.save(str(pdf_path))
    doc.close()

    cands = extract_title_candidates(pdf_path, top_n=3)
    assert "The Big Important Title" in cands[0]


def test_extract_arxiv_id():
    assert extract_arxiv_id("foo arXiv:2507.09089 bar") == "2507.09089"
    assert extract_arxiv_id("arXiv:2410.18334v1") == "2410.18334"
    assert extract_arxiv_id("no arxiv here") is None


def test_extract_pages_raises_on_encrypted(tmp_path):
    """Build a password-protected PDF and verify EncryptedPDFError is raised."""
    import pytest

    from rag.parsers.pdf import EncryptedPDFError

    pdf_path = tmp_path / "encrypted.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "secret content", fontsize=11)
    doc.save(
        str(pdf_path),
        encryption=pymupdf.PDF_ENCRYPT_AES_256,
        user_pw="secret",
        owner_pw="secret_owner",
    )
    doc.close()

    with pytest.raises(EncryptedPDFError):
        extract_pages(pdf_path)
