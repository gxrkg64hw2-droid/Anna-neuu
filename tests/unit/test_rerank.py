from unittest.mock import MagicMock, patch


def test_rerank_pairs_returns_score_per_candidate():
    with patch("rag.search.rerank._get_model") as mock_model:
        encoder = MagicMock()
        encoder.predict.return_value = [0.9, 0.5, 0.7]
        mock_model.return_value = encoder
        from rag.search.rerank import rerank_pairs
        scores = rerank_pairs("query text", ["candidate A", "candidate B", "candidate C"])
        assert len(scores) == 3
        assert scores == [0.9, 0.5, 0.7]
