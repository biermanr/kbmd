"""Test initialization of markdown knowledgebases."""

import pytest
import pathlib
import git

from kbmd.subcommands.init import init_kb


def test_init_in_git_repo_success(tmp_path, monkeypatch):
    """Test that initializing a knowledgebase in a git-managed folder succeeds."""
    git.Repo.init(tmp_path)
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)

    init_kb()

    assert (tmp_path / ".kbmd").exists()
    assert tmp_path.joinpath(".kbmd", "root.jinja").exists()


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
