"""Test data models."""

from datetime import datetime, date

from kbmd.models import (
    DatasetMetadata,
    ProjectMetadata,
    ProjectStatus,
    CollaboratorRole,
    Collaborator,
    RelatedProject,
    IndexMetadata,
    IndexEntry,
    IndexCategory,
    KnowledgebaseConfig,
)


def test_dataset_metadata_creation():
    """Test creating dataset metadata with required fields."""
    dataset = DatasetMetadata(
        name="Test Dataset",
        slug="test-dataset",
        path="/data/test",
        description="A test dataset",
        size="100 MB",
        file_type="CSV",
        data_source="Lab experiment",
        last_modified=datetime.now(),
    )

    assert dataset.name == "Test Dataset"
    assert dataset.slug == "test-dataset"
    assert dataset.path == "/data/test"
    assert dataset.size == "100 MB"
    assert dataset.file_type == "CSV"
    assert dataset.data_source == "Lab experiment"
    assert isinstance(dataset.date_added, datetime)
    assert dataset.related_projects == []
    assert dataset.tags == []


def test_dataset_metadata_with_optional_fields():
    """Test creating dataset metadata with optional fields."""
    related_project = RelatedProject(name="Test Project", slug="test-project")

    dataset = DatasetMetadata(
        name="Test Dataset",
        slug="test-dataset",
        path="/data/test",
        description="A test dataset",
        size="100 MB",
        size_bytes=104857600,
        file_type="CSV",
        file_count=50,
        compression="gzip",
        data_source="Lab experiment",
        last_modified=datetime.now(),
        related_projects=[related_project],
        access_notes="Requires permission",
        tags=["test", "csv"],
    )

    assert dataset.size_bytes == 104857600
    assert dataset.file_count == 50
    assert dataset.compression == "gzip"
    assert len(dataset.related_projects) == 1
    assert dataset.related_projects[0].name == "Test Project"
    assert dataset.access_notes == "Requires permission"
    assert dataset.tags == ["test", "csv"]


def test_project_metadata_creation():
    """Test creating project metadata with required fields."""
    project = ProjectMetadata(
        name="Test Project",
        slug="test-project",
        path="/projects/test",
        description="A test project",
        objectives="Test objectives",
        status=ProjectStatus.ACTIVE,
        date_started=date.today(),
        principal_investigator="Dr. Test",
    )

    assert project.name == "Test Project"
    assert project.status == ProjectStatus.ACTIVE
    assert project.principal_investigator == "Dr. Test"
    assert isinstance(project.date_added, datetime)
    assert project.collaborators == []
    assert project.datasets == []
    assert project.scripts == []
    assert project.publications == []


def test_project_metadata_with_collaborators():
    """Test creating project metadata with collaborators."""
    collaborator = Collaborator(
        name="Dr. Jane Smith",
        role=CollaboratorRole.RESEARCHER,
        email="jane@example.com",
    )

    project = ProjectMetadata(
        name="Test Project",
        slug="test-project",
        path="/projects/test",
        description="A test project",
        objectives="Test objectives",
        status=ProjectStatus.ACTIVE,
        date_started=date.today(),
        principal_investigator="Dr. Test",
        collaborators=[collaborator],
    )

    assert len(project.collaborators) == 1
    assert project.collaborators[0].name == "Dr. Jane Smith"
    assert project.collaborators[0].role == CollaboratorRole.RESEARCHER


def test_project_status_enum():
    """Test project status enum values."""
    assert ProjectStatus.ACTIVE == "active"
    assert ProjectStatus.COMPLETED == "completed"
    assert ProjectStatus.ON_HOLD == "on_hold"
    assert ProjectStatus.ARCHIVED == "archived"


def test_collaborator_role_enum():
    """Test collaborator role enum values."""
    assert CollaboratorRole.PI == "Principal Investigator"
    assert CollaboratorRole.RESEARCHER == "Researcher"
    assert CollaboratorRole.STUDENT == "Student"


def test_index_metadata_creation():
    """Test creating index metadata."""
    entry = IndexEntry(
        name="Test Entry", link="test-entry.md", description="A test entry"
    )

    category = IndexCategory(category="Test Category", entries=[entry])

    index = IndexMetadata(
        title="Test Index", description="A test index", entries=[category]
    )

    assert index.title == "Test Index"
    assert len(index.entries) == 1
    assert index.entries[0].category == "Test Category"
    assert len(index.entries[0].entries) == 1
    assert index.entries[0].entries[0].name == "Test Entry"


def test_knowledgebase_config_creation():
    """Test creating knowledgebase configuration."""
    config = KnowledgebaseConfig(
        name="Test KB",
        description="A test knowledgebase",
        git_repo_path="/path/to/repo",
    )

    assert config.name == "Test KB"
    assert config.description == "A test knowledgebase"
    assert config.git_repo_path == "/path/to/repo"
    assert isinstance(config.created, datetime)
    assert config.custom_templates is False
    assert config.auto_update_indices is True
