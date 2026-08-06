"""Config loading for the rag toolkit."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    repo_root: Path
    openrouter_api_key: str
    google_api_key: str | None = None
    embedding_model: str = "openai/text-embedding-3-large"
    embedding_dimensions: int = 3072
    chunk_target_tokens: int = 512
    chunk_overlap_tokens: int = 80
    bm25_language: str = "english"

    def thesis_dir(self, name: str) -> Path:
        return self.repo_root / "thesen" / name

    def thesis_index_dir(self, name: str) -> Path:
        return self.thesis_dir(name) / "index"

    def thesis_pdfs_dir(self, name: str) -> Path:
        return self.thesis_dir(name) / "pdfs"

    def thesis_corpus_db(self, name: str) -> Path:
        return self.thesis_index_dir(name) / "corpus.db"


def load_config(repo_root: Path | None = None) -> Config:
    if repo_root is None:
        repo_root = Path(__file__).resolve().parent.parent
    repo_root = Path(repo_root).resolve()
    load_dotenv(repo_root / ".env", override=False)
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENROUTER_API_KEY not set. Copy .env.example to .env and fill it in."
        )
    return Config(
        repo_root=repo_root,
        openrouter_api_key=key,
        google_api_key=os.environ.get("GOOGLE_API_KEY") or None,
        bm25_language=os.environ.get("BM25_LANGUAGE", "english"),
    )
