"""Test adding entries to the knowledgebase."""

import json
import pathlib
import pytest
import git
from unittest.mock import patch

from kbmd.subcommands.init import init_kb
from kbmd.subcommands.add import add_entry, _generate_slug
from kbmd.models import DatasetMetadata, ProjectMetadata


def test_generate_slug():
    """Test slug generation from names."""
    assert _generate_slug("My Dataset Name") == "my-dataset-name"
    assert (
        _generate_slug("Project with (special) chars!") == "project-with-special-chars"
    )
    assert _generate_slug("  Spaces  and--dashes  ") == "spaces-and-dashes"


@pytest.fixture
def initialized_repo(tmp_path, monkeypatch):
    """Create a git repo with initialized kbmd."""
    git.Repo.init(tmp_path)
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)
    init_kb()
    return tmp_path


def test_add_dataset_success(initialized_repo, monkeypatch):
    """Test successfully adding a dataset."""
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: initialized_repo)

    # Mock user input
    user_inputs = [
        "Test Dataset",  # name
        "A test dataset for unit testing",  # description
        "100 MB",  # size
        "CSV",  # file_type
        "50",  # file_count
        "gzip",  # compression
        "Laboratory experiment",  # data_source
        "Requires special access",  # access_notes
        "test, csv, experiment",  # tags
    ]

    with patch("builtins.input", side_effect=user_inputs):
        add_entry(".", "dataset")

    # Check that the dataset was created
    dataset_file = (
        initialized_repo / ".kbmd" / "data" / "datasets" / "test-dataset.json"
    )
    assert dataset_file.exists()

    # Validate the dataset content
    dataset_data = json.loads(dataset_file.read_text())
    dataset = DatasetMetadata(**dataset_data)

    assert dataset.name == "Test Dataset"
    assert dataset.slug == "test-dataset"
    assert dataset.description == "A test dataset for unit testing"
    assert dataset.size == "100 MB"
    assert dataset.file_type == "CSV"
    assert dataset.file_count == 50
    assert dataset.compression == "gzip"
    assert dataset.data_source == "Laboratory experiment"
    assert dataset.access_notes == "Requires special access"
    assert dataset.tags == ["test", "csv", "experiment"]


def test_add_project_success(initialized_repo, monkeypatch):
    """Test successfully adding a project."""
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: initialized_repo)

    # Mock user input
    user_inputs = [
        "Test Project",  # name
        "A test project for unit testing",  # description
        "Test the functionality of the kbmd system",  # objectives
        "active",  # status
        "2024-01-01",  # date_started
        "",  # date_completed (empty)
        "Dr. Jane Smith",  # principal_investigator
        "/results/test-project",  # results_path
        "Preliminary results show promise",  # results_description
        "testing, development",  # tags
    ]

    with patch("builtins.input", side_effect=user_inputs):
        add_entry(".", "project")

    # Check that the project was created
    project_file = (
        initialized_repo / ".kbmd" / "data" / "projects" / "test-project.json"
    )
    assert project_file.exists()

    # Validate the project content
    project_data = json.loads(project_file.read_text())
    project = ProjectMetadata(**project_data)

    assert project.name == "Test Project"
    assert project.slug == "test-project"
    assert project.description == "A test project for unit testing"
    assert project.objectives == "Test the functionality of the kbmd system"
    assert project.status == "active"
    assert project.principal_investigator == "Dr. Jane Smith"
    assert project.results_path == "/results/test-project"
    assert project.tags == ["testing", "development"]


def test_add_entry_no_kbmd_fails(tmp_path, monkeypatch):
    """Test that adding entries fails when no .kbmd directory exists."""
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: tmp_path)

    with pytest.raises(RuntimeError, match="No .kbmd directory found"):
        add_entry(".", "dataset")


def test_add_entry_invalid_type_fails(initialized_repo, monkeypatch):
    """Test that adding entries fails with invalid type."""
    monkeypatch.setattr(pathlib.Path, "cwd", lambda: initialized_repo)

    with pytest.raises(ValueError, match="Unknown entry type"):
        add_entry(".", "invalid_type")
