"""Add new entries to the knowledgebase."""

import datetime
import re
from pathlib import Path
from typing import Optional

from kbmd.models import DatasetMetadata, ProjectMetadata, ProjectStatus


def add_entry(path: str, entry_type: str) -> None:
    """Add a new dataset or project entry to the knowledgebase."""
    target_path = Path(path).resolve()

    # Check if we're in a knowledgebase
    kbmd_dir = _find_kbmd_directory()
    if not kbmd_dir:
        raise RuntimeError("No .kbmd directory found. Run 'kbmd init' first.")

    if entry_type == "dataset":
        _add_dataset(target_path, kbmd_dir)
    elif entry_type == "project":
        _add_project(target_path, kbmd_dir)
    else:
        raise ValueError(f"Unknown entry type: {entry_type}")


def _find_kbmd_directory() -> Optional[Path]:
    """Find the .kbmd directory by walking up the directory tree."""
    current = Path.cwd()

    while current != current.parent:
        kbmd_dir = current / ".kbmd"
        if kbmd_dir.exists() and kbmd_dir.is_dir():
            return kbmd_dir
        current = current.parent

    return None


def _add_dataset(path: Path, kbmd_dir: Path) -> None:
    """Add a new dataset entry."""
    print(f"Adding dataset: {path}")
    print()

    # Get basic information
    name = input(f"Dataset name [{path.name}]: ").strip() or path.name
    description = input("Description: ").strip()

    if not description:
        raise ValueError("Description is required for datasets")

    # Generate slug
    slug = _generate_slug(name)

    # Get file information
    print()
    size = input("Dataset size (e.g., '2.5 GB', '150 MB'): ").strip()
    if not size:
        raise ValueError("Dataset size is required")

    file_type = input("Primary file type (e.g., 'CSV', 'HDF5', 'TIFF'): ").strip()
    if not file_type:
        raise ValueError("File type is required")

    file_count_input = input("Number of files (optional): ").strip()
    file_count = int(file_count_input) if file_count_input else None

    compression = input("Compression format (optional): ").strip() or None

    # Get data source
    data_source = input("Data source (where did this data come from?): ").strip()
    if not data_source:
        raise ValueError("Data source is required")

    # Get access notes
    access_notes = input("Access notes (optional): ").strip() or None

    # Get tags
    tags_input = input("Tags (comma-separated, optional): ").strip()
    tags = (
        [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        if tags_input
        else []
    )

    # Get last modified time
    if path.exists():
        last_modified = datetime.datetime.fromtimestamp(path.stat().st_mtime)
    else:
        print(f"Warning: Path {path} does not exist")
        last_modified = datetime.datetime.now()

    # Create metadata object
    dataset = DatasetMetadata(
        name=name,
        slug=slug,
        path=str(path),
        description=description,
        size=size,
        file_type=file_type,
        file_count=file_count,
        compression=compression,
        data_source=data_source,
        last_modified=last_modified,
        access_notes=access_notes,
        tags=tags,
    )

    # Save to JSON file
    data_file = kbmd_dir / "data" / "datasets" / f"{slug}.json"
    data_file.write_text(dataset.model_dump_json(indent=2))

    print(f"Dataset '{name}' added successfully!")
    print(f"Data saved to: {data_file}")


def _add_project(path: Path, kbmd_dir: Path) -> None:
    """Add a new project entry."""
    print(f"Adding project: {path}")
    print()

    # Get basic information
    name = input(f"Project name [{path.name}]: ").strip() or path.name
    description = input("Project description: ").strip()

    if not description:
        raise ValueError("Description is required for projects")

    objectives = input("Project objectives: ").strip()
    if not objectives:
        raise ValueError("Objectives are required for projects")

    # Generate slug
    slug = _generate_slug(name)

    # Get status
    print()
    print("Available statuses: active, completed, on_hold, archived")
    status_input = input("Project status [active]: ").strip().lower() or "active"

    try:
        status = ProjectStatus(status_input)
    except ValueError:
        raise ValueError(f"Invalid status: {status_input}")

    # Get dates
    date_started_input = input("Start date (YYYY-MM-DD): ").strip()
    try:
        date_started = datetime.datetime.strptime(date_started_input, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    date_completed_input = input("Completion date (YYYY-MM-DD, optional): ").strip()
    date_completed = None
    if date_completed_input:
        try:
            date_completed = datetime.datetime.strptime(
                date_completed_input, "%Y-%m-%d"
            ).date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

    # Get personnel
    print()
    principal_investigator = input("Principal Investigator: ").strip()
    if not principal_investigator:
        raise ValueError("Principal Investigator is required")

    # Get results information
    print()
    results_path = input("Results location (optional): ").strip() or None
    results_description = input("Results description (optional): ").strip() or None

    # Get tags
    tags_input = input("Tags (comma-separated, optional): ").strip()
    tags = (
        [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        if tags_input
        else []
    )

    # Create metadata object
    project = ProjectMetadata(
        name=name,
        slug=slug,
        path=str(path),
        description=description,
        objectives=objectives,
        status=status,
        date_started=date_started,
        date_completed=date_completed,
        principal_investigator=principal_investigator,
        results_path=results_path,
        results_description=results_description,
        tags=tags,
    )

    # Save to JSON file
    data_file = kbmd_dir / "data" / "projects" / f"{slug}.json"
    data_file.write_text(project.model_dump_json(indent=2))

    print(f"Project '{name}' added successfully!")
    print(f"Data saved to: {data_file}")


def _generate_slug(name: str) -> str:
    """Generate a URL-friendly slug from a name."""
    # Convert to lowercase and replace spaces with hyphens
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s-]+", "-", slug)
    slug = slug.strip("-")

    return slug
