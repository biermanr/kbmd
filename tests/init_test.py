"""Test initialization of markdown knowledgebases."""

import json
import pytest
import pathlib
import git

from kbmd.subcommands.init import init_kb


def test_init_in_git_repo_success(tmp_path, monkeypatch):
    """Test that initializing a knowledgebase in a git-managed folder succeeds."""
    git.Repo.init(tmp_path)
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)

    init_kb()

    # Check basic structure
    kbmd_dir = tmp_path / ".kbmd"
    assert kbmd_dir.exists()

    # Check directory structure
    assert (kbmd_dir / "templates").exists()
    assert (kbmd_dir / "data").exists()
    assert (kbmd_dir / "data" / "datasets").exists()
    assert (kbmd_dir / "data" / "projects").exists()
    assert (kbmd_dir / "data" / "indices").exists()
    assert (kbmd_dir / "generated").exists()
    assert (kbmd_dir / "generated" / "datasets").exists()
    assert (kbmd_dir / "generated" / "projects").exists()
    assert (kbmd_dir / "generated" / "indices").exists()

    # Check templates were copied
    assert (kbmd_dir / "templates" / "root.jinja").exists()
    assert (kbmd_dir / "templates" / "dataset.jinja").exists()
    assert (kbmd_dir / "templates" / "project.jinja").exists()
    assert (kbmd_dir / "templates" / "index.jinja").exists()

    # Check config file was created
    config_file = kbmd_dir / "config.json"
    assert config_file.exists()
    config_data = json.loads(config_file.read_text())
    assert "name" in config_data
    assert "git_repo_path" in config_data

    # Check initial index files were created
    assert (kbmd_dir / "data" / "indices" / "by-filesystem.json").exists()
    assert (kbmd_dir / "data" / "indices" / "by-topic.json").exists()


def test_init_not_git_fails(tmp_path, monkeypatch):
    """Test that initializing a knowledgebase in a non-git folder fails."""
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)

    with pytest.raises(
        RuntimeError, match="Current directory is not a git repository."
    ):
        init_kb()


def test_init_already_exists_fails(tmp_path, monkeypatch):
    """Test that initializing a knowledgebase when .kbmd already exists fails."""
    git.Repo.init(tmp_path)
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)

    (tmp_path / ".kbmd").mkdir()

    with pytest.raises(RuntimeError, match=r"\.kbmd directory already exists"):
        init_kb()
