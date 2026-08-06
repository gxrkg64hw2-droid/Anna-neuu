from rag.parsers.ocr import needs_ocr, run_ocr_on_pdf


def test_needs_ocr_below_threshold():
    page_qualities = [0.95, 0.20, 0.92, 0.10]
    assert needs_ocr(page_qualities, threshold=0.4) == [2, 4]  # 1-indexed


def test_needs_ocr_all_clean():
    assert needs_ocr([0.9, 0.95, 0.88], threshold=0.4) == []


def test_run_ocr_skipped_when_no_pages_need_it(tmp_path):
    pdf = tmp_path / "in.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")  # invalid but unused
    out = tmp_path / "out.pdf"
    result = run_ocr_on_pdf(pdf, out, pages_to_ocr=[])
    assert result == {"ocred_pages": [], "skipped": True}
