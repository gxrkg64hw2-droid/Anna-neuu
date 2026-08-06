from rag.indexer.store import Store


def test_store_initializes_schema(tmp_path):
    db = tmp_path / "test.db"
    store = Store.create(db)
    cur = store.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur}
    assert "sources" in tables
    assert "chunks" in tables
    assert "pages" in tables
    store.close()


def test_store_inserts_source_and_chunk(tmp_path):
    db = tmp_path / "test.db"
    store = Store.create(db)
    src_id = store.add_source(
        filename="demo.pdf", sha256="abc", page_count_pdf=10,
        title="Demo", authors=["Doe, J."], year=2024, doi=None,
    )
    chunk_id = store.add_chunk(
        source_id=src_id, text="Hello world.", token_count=3,
        pdf_page_start=1, pdf_page_end=1,
        printed_page_start=1, printed_page_end=1,
        quality_score=0.9, ocr_origin=0,
    )
    embedding = [0.1] * 3072
    store.add_embedding(chunk_id, embedding)
    store.conn.commit()

    rows = list(store.conn.execute("SELECT chunk_id, source_id FROM chunks"))
    assert len(rows) == 1
    assert rows[0][1] == src_id
    store.close()


def test_store_idempotent_by_sha256(tmp_path):
    db = tmp_path / "test.db"
    store = Store.create(db)
    sha = "abc123"
    s1 = store.add_source(filename="x.pdf", sha256=sha, page_count_pdf=1,
                          title=None, authors=[], year=None, doi=None)
    assert store.find_source_by_sha256(sha) == s1
    store.close()


def test_store_delete_source_cascades_chunks(tmp_path):
    db = tmp_path / "test.db"
    store = Store.create(db)
    sid = store.add_source(filename="x.pdf", sha256="aaa", page_count_pdf=1,
                           title=None, authors=[], year=None, doi=None)
    cid = store.add_chunk(source_id=sid, text="t", token_count=1,
                          pdf_page_start=1, pdf_page_end=1,
                          printed_page_start=None, printed_page_end=None,
                          quality_score=0.9, ocr_origin=0)
    store.add_embedding(cid, [0.0] * 3072)
    store.conn.commit()
    store.delete_source(sid)
    store.conn.commit()
    assert store.conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0] == 0
    assert store.conn.execute("SELECT COUNT(*) FROM vec_chunks").fetchone()[0] == 0
    store.close()
