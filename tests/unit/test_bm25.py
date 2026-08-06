from rag.indexer.bm25 import build_bm25_index, load_index, query_bm25, save_index


def test_bm25_indexes_and_queries(tmp_path):
    chunks = [
        "Retrieval-Augmented Generation combines parametric and non-parametric memory.",
        "The diffusion of innovations follows an S-shaped curve.",
        "Likert scales are commonly used in survey methodology.",
    ]
    chunk_ids = [10, 20, 30]
    idx = build_bm25_index(chunk_ids, chunks)
    save_index(idx, tmp_path)

    loaded = load_index(tmp_path)
    hits = query_bm25(loaded, "RAG memory parametric", top_k=2)
    assert hits[0][0] == 10  # chunk 10 wins


def test_bm25_german_text(tmp_path):
    chunks = [
        "Die Diffusion von Innovationen folgt einer S-foermigen Kurve.",
        "Akzeptanz ist eine positive Einstellung gegenueber neuer Technologie.",
    ]
    chunk_ids = [1, 2]
    idx = build_bm25_index(chunk_ids, chunks, language="german")
    save_index(idx, tmp_path)
    loaded = load_index(tmp_path)
    hits = query_bm25(loaded, "Akzeptanz Technologie", top_k=2)
    assert hits[0][0] == 2
