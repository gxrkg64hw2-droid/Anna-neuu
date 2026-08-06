from rag.parsers.quality import score_page


def test_score_clean_text_high():
    text = (
        "Retrieval-Augmented Generation combines parametric and non-parametric memory"
        " in modern LLM systems."
    )
    s = score_page(text)
    assert s > 0.85


def test_score_empty_zero():
    assert score_page("") == 0.0


def test_score_garbage_low():
    text = "!!!1234@@@!!!" * 5
    assert score_page(text) < 0.3


def test_score_short_but_clean_okay():
    text = "Short page."
    s = score_page(text)
    assert 0.3 < s < 1.0
