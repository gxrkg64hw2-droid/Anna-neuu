from rag.metadata.doi_extract import extract_doi_from_text


def test_extract_doi_simple():
    text = "Lewis et al. 2020. https://doi.org/10.48550/arXiv.2005.11401"
    assert extract_doi_from_text(text) == "10.48550/arXiv.2005.11401"


def test_extract_doi_no_match():
    assert extract_doi_from_text("no doi here") is None


def test_extract_first_match_only():
    text = "10.1000/xyz and later 10.1001/abc"
    assert extract_doi_from_text(text) == "10.1000/xyz"


def test_skip_placeholder_acm_template_doi():
    """ACM template leaves '10.1145/nnnnnnn.nnnnnnn' in submitted preprints."""
    text = "https://doi.org/10.1145/nnnnnnn.nnnnnnn and the real one 10.48550/arxiv.2511.09268"
    assert extract_doi_from_text(text) == "10.48550/arxiv.2511.09268"


def test_skip_placeholder_xxxx():
    text = "stub: 10.1234/xxxxxxxx then real: 10.1145/3456789"
    assert extract_doi_from_text(text) == "10.1145/3456789"
