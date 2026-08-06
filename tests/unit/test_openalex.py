from unittest.mock import MagicMock, patch

from rag.metadata.openalex import lookup_by_doi


@patch("rag.metadata.openalex.httpx.get")
def test_lookup_by_doi_returns_metadata(mock_get):
    mock_resp = MagicMock(status_code=200)
    mock_resp.json.return_value = {
        "id": "https://openalex.org/W123",
        "title": "Retrieval Augmented Generation",
        "publication_year": 2020,
        "doi": "https://doi.org/10.123/abc",
        "authorships": [
            {"author": {"display_name": "Patrick Lewis"}},
            {"author": {"display_name": "Ethan Perez"}},
        ],
        "primary_location": {"source": {"display_name": "NeurIPS"}},
    }
    mock_get.return_value = mock_resp
    meta = lookup_by_doi("10.123/abc")
    assert meta["title"] == "Retrieval Augmented Generation"
    assert meta["year"] == 2020
    assert meta["authors"] == ["Patrick Lewis", "Ethan Perez"]
    assert meta["venue"] == "NeurIPS"


@patch("rag.metadata.openalex.httpx.get")
def test_lookup_by_doi_not_found(mock_get):
    mock_get.return_value = MagicMock(status_code=404)
    assert lookup_by_doi("10.999/missing") is None
