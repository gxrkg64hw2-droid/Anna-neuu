import pytest

from rag.tools.extract_citations import parse_page_number, parse_tex_citations


def test_parse_textcite(tmp_path):
    f = tmp_path / "x.tex"
    f.write_text(r"\textcite[S. 12]{rogers1983} introduced the diffusion theory.")
    cites = list(parse_tex_citations(f))
    assert cites[0].bibkey == "rogers1983"
    assert cites[0].pages == "S. 12"
    assert cites[0].cmd == "textcite"


def test_parse_parencite_no_pages(tmp_path):
    f = tmp_path / "x.tex"
    f.write_text(r"This idea \parencite{lewis2020} is influential.")
    cites = list(parse_tex_citations(f))
    assert cites[0].bibkey == "lewis2020"
    assert cites[0].pages is None


def test_parse_multiple_keys(tmp_path):
    f = tmp_path / "x.tex"
    f.write_text(r"\parencite[S. 1-3]{lewis2020,rogers1983}")
    cites = list(parse_tex_citations(f))
    assert {c.bibkey for c in cites} == {"lewis2020", "rogers1983"}


# --- parse_page_number tests ---

@pytest.mark.parametrize("pages_str,expected", [
    ("S. 23", 23),
    ("vgl. S. 23", 23),
    ("S. 23 f.", 23),
    ("S. 23-25", 23),
    ("S. 23ff.", 23),
    ("s. 5", 5),
    ("pp. 42", 42),
    ("p. 7", 7),
    ("S. 100-110", 100),
])
def test_parse_page_number_valid(pages_str, expected):
    assert parse_page_number(pages_str) == expected


@pytest.mark.parametrize("pages_str", [
    None,
    "",
    "vgl.",
    "ebd.",
    "Kap. 3",
])
def test_parse_page_number_no_page(pages_str):
    assert parse_page_number(pages_str) is None
