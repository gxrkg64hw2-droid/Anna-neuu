"""Crossref API client. Polite, no key needed."""
from __future__ import annotations

import httpx

BASE = "https://api.crossref.org"
TIMEOUT = 15.0


def lookup_by_doi(doi: str) -> dict | None:
    url = f"{BASE}/works/{doi}"
    try:
        resp = httpx.get(url, timeout=TIMEOUT, headers={"User-Agent": "rag-toolkit/0.1"})
    except httpx.RequestError:
        return None
    if resp.status_code != 200:
        return None
    msg = resp.json().get("message", {})
    return _normalize(msg)


def _normalize(msg: dict) -> dict:
    title = (msg.get("title") or [None])[0]
    authors = [
        f"{a.get('given', '')} {a.get('family', '')}".strip()
        for a in msg.get("author", [])
        if a
    ]
    year = None
    issued = msg.get("issued", {}).get("date-parts", [])
    if issued and issued[0]:
        year = issued[0][0]
    venue = (msg.get("container-title") or [None])[0]
    return {
        "title": title,
        "year": year,
        "authors": [a for a in authors if a],
        "doi": msg.get("DOI"),
        "venue": venue,
        "type": msg.get("type"),
    }
