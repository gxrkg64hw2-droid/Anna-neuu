from rag.metadata.bib import _disambiguate_key, make_bibkey, render_bibtex


def test_bibkey_lewis_2020():
    meta = {"title": "Retrieval Augmented Generation",
            "authors": ["Patrick Lewis", "Ethan Perez"], "year": 2020}
    assert make_bibkey(meta) == "lewisRetrievalAugmented2020"


def test_bibkey_strips_special_chars():
    meta = {"title": "A: Multi-Stage Approach!", "authors": ["Doe, Jane"], "year": 2024}
    assert make_bibkey(meta) == "doeMultiStage2024"


def test_render_bibtex_minimum():
    meta = {
        "title": "Foo Bar", "authors": ["Doe, Jane"], "year": 2024,
        "doi": "10.123/abc", "venue": "Conf",
    }
    rendered = render_bibtex(make_bibkey(meta), meta)
    assert "@article{doeFoo2024," in rendered
    assert "title = {Foo Bar}" in rendered
    assert "doi = {10.123/abc}" in rendered


def test_render_bibtex_with_filename():
    meta = {"title": "Foo", "authors": ["Doe, J."], "year": 2024}
    rendered = render_bibtex("doeFoo2024", meta, filename="doe2024.pdf")
    assert "file = {doe2024.pdf}" in rendered


def test_disambiguate_key_no_collision():
    assert _disambiguate_key("foo2024", set()) == "foo2024"


def test_disambiguate_key_with_collision():
    assert _disambiguate_key("foo2024", {"foo2024"}) == "foo2024a"
    assert _disambiguate_key("foo2024", {"foo2024", "foo2024a"}) == "foo2024b"
