"""Test building the knowledgebase."""

import json
import pathlib
import pytest
import git
from datetime import datetime, date

from kbmd.subcommands.init import init_kb
from kbmd.subcommands.build import build_kb
from kbmd.models import DatasetMetadata, ProjectMetadata, ProjectStatus


@pytest.fixture
def initialized_repo_with_data(tmp_path, monkeypatch):
    """Create a git repo with initialized kbmd and sample data."""
    git.Repo.init(tmp_path)
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)
    init_kb()

    # Create sample dataset
    dataset = DatasetMetadata(
        name="Sample Dataset",
        slug="sample-dataset",
        path="/data/sample",
        description="A sample dataset for testing",
        size="500 MB",
        file_type="CSV",
        file_count=100,
        data_source="Test lab",
        last_modified=datetime.now(),
        tags=["test", "sample"],
    )

    dataset_file = tmp_path / ".kbmd" / "data" / "datasets" / "sample-dataset.json"
    dataset_file.write_text(dataset.model_dump_json(indent=2))

    # Create sample project
    project = ProjectMetadata(
        name="Sample Project",
        slug="sample-project",
        path="/projects/sample",
        description="A sample project for testing",
        objectives="Test project objectives",
        status=ProjectStatus.ACTIVE,
        date_started=date.today(),
        principal_investigator="Dr. Test",
        tags=["research", "testing"],
    )

    project_file = tmp_path / ".kbmd" / "data" / "projects" / "sample-project.json"
    project_file.write_text(project.model_dump_json(indent=2))

    return tmp_path


def test_build_kb_success(initialized_repo_with_data, monkeypatch, capsys):
    """Test successfully building the knowledgebase."""
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: initialized_repo_with_data)

    build_kb()

    # Capture output
    captured = capsys.readouterr()
    assert "Building knowledgebase..." in captured.out
    assert "Generated 1 dataset pages" in captured.out
    assert "Generated 1 project pages" in captured.out
    assert "Generated 2 index pages" in captured.out
    assert "Generated main README.md" in captured.out
    assert "✓ Build completed successfully!" in captured.out

    kbmd_dir = initialized_repo_with_data / ".kbmd"

    # Check that dataset markdown was generated
    dataset_md = kbmd_dir / "generated" / "datasets" / "sample-dataset.md"
    assert dataset_md.exists()
    content = dataset_md.read_text()
    assert "# Sample Dataset" in content
    assert "A sample dataset for testing" in content
    assert "500 MB" in content

    # Check that project markdown was generated
    project_md = kbmd_dir / "generated" / "projects" / "sample-project.md"
    assert project_md.exists()
    content = project_md.read_text()
    assert "# Sample Project" in content
    assert "A sample project for testing" in content
    assert "Dr. Test" in content

    # Check that index files were generated
    fs_index = kbmd_dir / "generated" / "indices" / "by-filesystem.md"
    assert fs_index.exists()
    content = fs_index.read_text()
    assert "Browse by Filesystem Location" in content

    topic_index = kbmd_dir / "generated" / "indices" / "by-topic.md"
    assert topic_index.exists()
    content = topic_index.read_text()
    assert "Browse by Research Topic" in content

    # Check that main README was generated
    readme = kbmd_dir / "generated" / "README.md"
    assert readme.exists()
    content = readme.read_text()
    assert "knowledgebase" in content.lower()


def test_build_kb_no_kbmd_fails(tmp_path, monkeypatch):
    """Test that building fails when no .kbmd directory exists."""
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)

    with pytest.raises(RuntimeError, match="No .kbmd directory found"):
        build_kb()


def test_build_kb_empty_data(tmp_path, monkeypatch, capsys):
    """Test building with no datasets or projects."""
    git.Repo.init(tmp_path)
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)
    init_kb()

    build_kb()

    # Should still complete successfully
    captured = capsys.readouterr()
    assert "Generated 0 dataset pages" in captured.out
    assert "Generated 0 project pages" in captured.out
    assert "✓ Build completed successfully!" in captured.out


def test_indices_updated_correctly(initialized_repo_with_data, monkeypatch):
    """Test that indices are updated with current data."""
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: initialized_repo_with_data)

    build_kb()

    kbmd_dir = initialized_repo_with_data / ".kbmd"

    # Check filesystem index was updated
    fs_index_data = json.loads(
        (kbmd_dir / "data" / "indices" / "by-filesystem.json").read_text()
    )
    assert fs_index_data["title"] == "Browse by Filesystem Location"
    assert len(fs_index_data["entries"]) > 0

    # Check topic index was updated
    topic_index_data = json.loads(
        (kbmd_dir / "data" / "indices" / "by-topic.json").read_text()
    )
    assert topic_index_data["title"] == "Browse by Research Topic"
    assert len(topic_index_data["entries"]) > 0
