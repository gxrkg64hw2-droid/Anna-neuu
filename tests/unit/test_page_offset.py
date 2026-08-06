from rag.parsers.page_offset import detect_print_offset


def test_no_frontmatter_offset_zero():
    pages = [
        "Title page",
        "Abstract",
        "1 Introduction\nThis paper introduces...",
    ]
    offset, conf = detect_print_offset(pages)
    assert offset == 2
    assert conf > 0.7


def test_book_with_chapter_one_marker():
    pages = ["Cover", "Frontispiece", "TOC ...", "Preface ...", "Acknowledgements",
             "Chapter 1\n\nIntroduction", "more text"]
    offset, conf = detect_print_offset(pages)
    assert offset == 5
    assert conf > 0.7


def test_no_marker_returns_zero_low_confidence():
    pages = ["random", "more random"]
    offset, conf = detect_print_offset(pages)
    assert offset == 0
    assert conf < 0.7


def test_german_kapitel_marker():
    pages = ["Deckblatt", "Inhalt", "Kapitel 1\nEinleitung"]
    offset, conf = detect_print_offset(pages)
    assert offset == 2
    assert conf > 0.7


def test_german_umlaut_chapter_marker():
    """Regex must match chapter headings starting with Umlaute like Ü, Ö, Ä."""
    pages = ["Cover", "Inhalt", "1 Übersicht"]
    offset, conf = detect_print_offset(pages)
    assert offset == 2
    assert conf > 0.7
