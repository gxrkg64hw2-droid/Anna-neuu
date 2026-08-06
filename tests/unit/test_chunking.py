from rag.parsers.chunking import chunk_text


def test_short_text_one_chunk():
    chunks = chunk_text("Short sentence.", target_tokens=512, overlap_tokens=80)
    assert len(chunks) == 1
    assert chunks[0].text == "Short sentence."


def test_long_text_splits_with_overlap():
    sentence = "This is a sentence with several words. "
    text = sentence * 200  # ~1600 tokens
    chunks = chunk_text(text, target_tokens=512, overlap_tokens=80)
    assert len(chunks) >= 3


def test_chunk_records_token_count():
    chunks = chunk_text("Hello world. " * 200, target_tokens=512, overlap_tokens=80)
    for c in chunks:
        assert c.token_count > 0
        assert c.token_count <= 512 + 50  # tolerance for sentence-boundary respect


def test_empty_text_returns_empty():
    assert chunk_text("", target_tokens=512, overlap_tokens=80) == []
