import pytest

from rag.config import load_config


def test_load_config_reads_openrouter_key(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    cfg = load_config(repo_root=tmp_path)
    assert cfg.openrouter_api_key == "sk-or-test"


def test_load_config_thesis_path(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    (tmp_path / "thesen" / "demo").mkdir(parents=True)
    cfg = load_config(repo_root=tmp_path)
    assert cfg.thesis_dir("demo") == tmp_path / "thesen" / "demo"


def test_load_config_missing_key_raises(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        load_config(repo_root=tmp_path)
