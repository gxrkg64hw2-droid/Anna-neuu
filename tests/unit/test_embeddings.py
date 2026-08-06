from unittest.mock import MagicMock, patch

from rag.indexer.embeddings import EmbeddingClient


@patch("rag.indexer.embeddings.OpenAI")
def test_embed_batch_calls_openai_with_model(mock_openai):
    fake = MagicMock()
    fake.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=[0.1, 0.2]), MagicMock(embedding=[0.3, 0.4])]
    )
    mock_openai.return_value = fake
    client = EmbeddingClient(api_key="sk-or-test", model="openai/text-embedding-3-large")
    out = client.embed_batch(["hello", "world"])
    assert out == [[0.1, 0.2], [0.3, 0.4]]
    call_args = fake.embeddings.create.call_args
    assert call_args.kwargs["model"] == "openai/text-embedding-3-large"
    assert call_args.kwargs["input"] == ["hello", "world"]


@patch("rag.indexer.embeddings.OpenAI")
def test_embed_batch_chunks_to_max_size(mock_openai):
    fake = MagicMock()
    fake.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=[0.0]) for _ in range(2)]
    )
    mock_openai.return_value = fake
    client = EmbeddingClient(
        api_key="sk-or-test", model="openai/text-embedding-3-large", batch_size=2
    )
    client.embed_batch(["a", "b", "c", "d"])
    assert fake.embeddings.create.call_count == 2
