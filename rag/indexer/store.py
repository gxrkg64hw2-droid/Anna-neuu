"""SQLite + sqlite-vec storage layer for the corpus index."""
from __future__ import annotations

import json
import sqlite3
import struct
from datetime import datetime, timezone
from pathlib import Path

import sqlite_vec

PARSER_VERSION = "0.1.0"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    source_id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL UNIQUE,
    sha256 TEXT NOT NULL,
    bibkey TEXT,
    title TEXT,
    authors TEXT,
    year INTEGER,
    doi TEXT,
    page_count_pdf INTEGER NOT NULL,
    page_count_printed INTEGER,
    print_offset INTEGER DEFAULT 0,
    print_offset_confidence REAL DEFAULT 1.0,
    indexed_at TEXT NOT NULL,
    parser_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(source_id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    token_count INTEGER NOT NULL,
    pdf_page_start INTEGER NOT NULL,
    pdf_page_end INTEGER NOT NULL,
    printed_page_start INTEGER,
    printed_page_end INTEGER,
    quality_score REAL NOT NULL,
    ocr_origin INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pages (
    source_id INTEGER NOT NULL REFERENCES sources(source_id) ON DELETE CASCADE,
    pdf_page INTEGER NOT NULL,
    printed_page INTEGER,
    text TEXT NOT NULL,
    quality_score REAL NOT NULL,
    ocr_origin INTEGER DEFAULT 0,
    PRIMARY KEY (source_id, pdf_page)
);

CREATE INDEX IF NOT EXISTS idx_chunks_source ON chunks(source_id);
CREATE INDEX IF NOT EXISTS idx_pages_source ON pages(source_id);
"""

VEC_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(
    chunk_id INTEGER PRIMARY KEY,
    embedding FLOAT[3072]
);
"""


def _vec_blob(values: list[float]) -> bytes:
    return struct.pack(f"{len(values)}f", *values)


class Store:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    @classmethod
    def create(cls, path: Path) -> "Store":
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(path))
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA)
        conn.executescript(VEC_SCHEMA)
        conn.commit()
        return cls(conn)

    def close(self) -> None:
        self.conn.close()

    # --- sources

    def find_source_by_sha256(self, sha: str) -> int | None:
        cur = self.conn.execute("SELECT source_id FROM sources WHERE sha256=?", (sha,))
        row = cur.fetchone()
        return row[0] if row else None

    def add_source(
        self,
        *,
        filename: str,
        sha256: str,
        page_count_pdf: int,
        title: str | None,
        authors: list[str],
        year: int | None,
        doi: str | None,
        bibkey: str | None = None,
        page_count_printed: int | None = None,
        print_offset: int = 0,
        print_offset_confidence: float = 1.0,
    ) -> int:
        cur = self.conn.execute(
            """INSERT INTO sources (filename, sha256, bibkey, title, authors, year, doi,
               page_count_pdf, page_count_printed, print_offset, print_offset_confidence,
               indexed_at, parser_version)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(filename) DO UPDATE SET sha256=excluded.sha256""",
            (
                filename,
                sha256,
                bibkey,
                title,
                json.dumps(authors),
                year,
                doi,
                page_count_pdf,
                page_count_printed,
                print_offset,
                print_offset_confidence,
                datetime.now(timezone.utc).isoformat(),
                PARSER_VERSION,
            ),
        )
        return cur.lastrowid or self._lookup_id("sources", "filename", filename, "source_id")

    def _lookup_id(self, table: str, key_col: str, key_val, id_col: str) -> int:
        cur = self.conn.execute(
            f"SELECT {id_col} FROM {table} WHERE {key_col}=?", (key_val,)
        )
        return cur.fetchone()[0]

    def delete_source(self, source_id: int) -> None:
        self.conn.execute(
            "DELETE FROM vec_chunks WHERE chunk_id IN "
            "(SELECT chunk_id FROM chunks WHERE source_id=?)",
            (source_id,),
        )
        self.conn.execute("DELETE FROM sources WHERE source_id=?", (source_id,))

    # --- chunks & pages

    def add_chunk(
        self,
        *,
        source_id: int,
        text: str,
        token_count: int,
        pdf_page_start: int,
        pdf_page_end: int,
        printed_page_start: int | None,
        printed_page_end: int | None,
        quality_score: float,
        ocr_origin: int,
    ) -> int:
        cur = self.conn.execute(
            """INSERT INTO chunks (source_id, text, token_count,
               pdf_page_start, pdf_page_end, printed_page_start, printed_page_end,
               quality_score, ocr_origin) VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                source_id,
                text,
                token_count,
                pdf_page_start,
                pdf_page_end,
                printed_page_start,
                printed_page_end,
                quality_score,
                ocr_origin,
            ),
        )
        return cur.lastrowid

    def add_page(
        self,
        *,
        source_id: int,
        pdf_page: int,
        printed_page: int | None,
        text: str,
        quality_score: float,
        ocr_origin: int,
    ) -> None:
        self.conn.execute(
            """INSERT OR REPLACE INTO pages
               (source_id, pdf_page, printed_page, text, quality_score, ocr_origin)
               VALUES (?,?,?,?,?,?)""",
            (source_id, pdf_page, printed_page, text, quality_score, ocr_origin),
        )

    def add_embedding(self, chunk_id: int, embedding: list[float]) -> None:
        self.conn.execute(
            "INSERT INTO vec_chunks(chunk_id, embedding) VALUES (?, ?)",
            (chunk_id, _vec_blob(embedding)),
        )
