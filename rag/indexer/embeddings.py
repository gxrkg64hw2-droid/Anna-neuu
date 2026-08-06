"""Embedding client routed through OpenRouter to OpenAI text-embedding-3-large."""
from __future__ import annotations

import time

from openai import OpenAI


class EmbeddingClient:
    def __init__(
        self,
        api_key: str,
        model: str = "openai/text-embedding-3-large",
        base_url: str = "https://openrouter.ai/api/v1",
        batch_size: int = 256,
        max_retries: int = 5,
    ) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.batch_size = batch_size
        self.max_retries = max_retries

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        out: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            out.extend(self._embed_with_retry(batch))
        return out

    def _embed_with_retry(self, batch: list[str]) -> list[list[float]]:
        backoff = 1.0
        for attempt in range(self.max_retries):
            try:
                resp = self.client.embeddings.create(model=self.model, input=batch)
                return [d.embedding for d in resp.data]
            except Exception:
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(backoff)
                backoff = min(60.0, backoff * 2)
        raise RuntimeError("unreachable")
