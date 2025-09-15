"""Data models for kbmd knowledgebase entries."""

import datetime
from typing import Optional, List
from enum import Enum

import pydantic


class ProjectStatus(str, Enum):
    """Enum for project status values."""

    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    ARCHIVED = "archived"


class CollaboratorRole(str, Enum):
    """Enum for collaborator roles."""

    PI = "Principal Investigator"
    RESEARCHER = "Researcher"
    STUDENT = "Student"
    TECHNICIAN = "Technician"
    COLLABORATOR = "Collaborator"


class RelatedProject(pydantic.BaseModel):
    """Reference to a related project."""

    name: str
    slug: str
    description: Optional[str] = None


class RelatedDataset(pydantic.BaseModel):
    """Reference to a related dataset."""

    name: str
    slug: str
    description: Optional[str] = None


class Script(pydantic.BaseModel):
    """Information about a script or code file."""

    path: str
    description: str
    language: Optional[str] = None


class Collaborator(pydantic.BaseModel):
    """Information about a project collaborator."""

    name: str
    role: CollaboratorRole
    email: Optional[str] = None
    affiliation: Optional[str] = None


class Publication(pydantic.BaseModel):
    """Information about a related publication."""

    title: str
    journal: str
    year: int
    doi: Optional[str] = None
    url: Optional[str] = None


class DatasetMetadata(pydantic.BaseModel):
    """Metadata for a dataset entry."""

    # Basic information
    name: str
    slug: str = pydantic.Field(description="URL-friendly identifier")
    path: str = pydantic.Field(description="Filesystem path to the dataset")
    description: str

    # File information
    size: str = pydantic.Field(description="Human-readable size (e.g., '2.5 GB')")
    size_bytes: Optional[int] = None
    file_type: str = pydantic.Field(description="Primary file format")
    file_count: Optional[int] = None
    compression: Optional[str] = None

    # Metadata
    data_source: str = pydantic.Field(description="Where the data came from")
    last_modified: datetime.datetime
    date_added: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )

    # Relationships
    related_projects: List[RelatedProject] = pydantic.Field(default_factory=list)

    # Access and usage
    access_notes: Optional[str] = None
    tags: List[str] = pydantic.Field(default_factory=list)


class ProjectMetadata(pydantic.BaseModel):
    """Metadata for a project entry."""

    # Basic information
    name: str
    slug: str = pydantic.Field(description="URL-friendly identifier")
    path: str = pydantic.Field(description="Filesystem path to the project")
    description: str
    objectives: str

    # Status and timeline
    status: ProjectStatus
    date_started: datetime.date
    date_completed: Optional[datetime.date] = None
    date_added: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )

    # Personnel
    principal_investigator: str
    collaborators: List[Collaborator] = pydantic.Field(default_factory=list)

    # Data and code
    datasets: List[RelatedDataset] = pydantic.Field(default_factory=list)
    scripts: List[Script] = pydantic.Field(default_factory=list)

    # Results
    results_path: Optional[str] = None
    results_description: Optional[str] = None

    # Publications
    publications: List[Publication] = pydantic.Field(default_factory=list)

    # Metadata
    tags: List[str] = pydantic.Field(default_factory=list)


class IndexEntry(pydantic.BaseModel):
    """An entry in an index page."""

    name: str
    link: str
    description: Optional[str] = None
    category: Optional[str] = None


class IndexCategory(pydantic.BaseModel):
    """A category of entries in an index."""

    category: str
    entries: List[IndexEntry]


class IndexMetadata(pydantic.BaseModel):
    """Metadata for an index page."""

    title: str
    description: str
    entries: List[IndexCategory] = pydantic.Field(default_factory=list)
    last_updated: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )


class KnowledgebaseConfig(pydantic.BaseModel):
    """Configuration for a specific knowledgebase instance."""

    name: str
    description: str
    created: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    git_repo_path: str

    # Template customizations
    custom_templates: bool = False

    # Generation settings
    auto_update_indices: bool = True
    generate_cross_references: bool = True
