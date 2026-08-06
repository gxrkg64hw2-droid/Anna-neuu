from unittest.mock import MagicMock, patch

from rag.metadata.crossref import lookup_by_doi


@patch("rag.metadata.crossref.httpx.get")
def test_crossref_doi_returns_metadata(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "message": {
                "title": ["Retrieval Augmented Generation"],
                "author": [{"given": "Patrick", "family": "Lewis"}],
                "issued": {"date-parts": [[2020]]},
                "DOI": "10.123/abc",
                "container-title": ["NeurIPS"],
            }
        },
    )
    meta = lookup_by_doi("10.123/abc")
    assert meta["title"] == "Retrieval Augmented Generation"
    assert meta["year"] == 2020
    assert meta["authors"] == ["Patrick Lewis"]


@patch("rag.metadata.crossref.httpx.get")
def test_crossref_not_found(mock_get):
    mock_get.return_value = MagicMock(status_code=404)
    assert lookup_by_doi("10.999/x") is None
