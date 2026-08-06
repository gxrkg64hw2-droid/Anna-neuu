"""OpenAlex API client. No API key required.

https://api.openalex.org/works/doi:<doi>
"""
from __future__ import annotations

import httpx

BASE = "https://api.openalex.org"
TIMEOUT = 15.0


def lookup_by_doi(doi: str) -> dict | None:
    url = f"{BASE}/works/doi:{doi}"
    try:
        resp = httpx.get(url, timeout=TIMEOUT, headers={"User-Agent": "rag-toolkit/0.1"})
    except httpx.RequestError:
        return None
    if resp.status_code != 200:
        return None
    data = resp.json()
    return _normalize(data)


def search_by_title(title: str, top: int = 3) -> list[dict]:
    url = f"{BASE}/works"
    params = {"search": title, "per-page": str(top)}
    try:
        resp = httpx.get(
            url,
            params=params,
            timeout=TIMEOUT,
            headers={"User-Agent": "rag-toolkit/0.1"},
        )
    except httpx.RequestError:
        return []
    if resp.status_code != 200:
        return []
    return [_normalize(r) for r in resp.json().get("results", [])]


def _normalize(data: dict) -> dict:
    authors = [
        a.get("author", {}).get("display_name")
        for a in data.get("authorships", [])
        if a.get("author")
    ]
    venue = ((data.get("primary_location") or {}).get("source") or {}).get("display_name")
    doi = data.get("doi")
    if doi and doi.startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    return {
        "openalex_id": data.get("id"),
        "title": data.get("title"),
        "year": data.get("publication_year"),
        "doi": doi,
        "authors": [a for a in authors if a],
        "venue": venue,
        "type": data.get("type"),
    }
