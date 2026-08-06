from rag.search.fusion import reciprocal_rank_fusion


def test_rrf_combines_two_rankings():
    dense = [(10, 0.9), (20, 0.8), (30, 0.7)]
    sparse = [(20, 5.0), (40, 3.0), (10, 1.0)]
    fused = reciprocal_rank_fusion([dense, sparse], top_k=3)
    ids = [cid for cid, _ in fused]
    assert 20 in ids
    assert 10 in ids


def test_rrf_handles_empty_list():
    fused = reciprocal_rank_fusion([[], [(1, 1.0)]], top_k=5)
    assert fused == [(1, 1 / (60 + 1))]


def test_rrf_top_k_caps_results():
    dense = [(i, 1.0 / i) for i in range(1, 100)]
    fused = reciprocal_rank_fusion([dense], top_k=5)
    assert len(fused) == 5
