"""Build collection of interlinking markdown documents for the knowledgebase."""

import json
import datetime
from pathlib import Path
from typing import Optional, List, Dict

import jinja2

from kbmd.models import (
    DatasetMetadata,
    ProjectMetadata,
    IndexMetadata,
    IndexCategory,
    IndexEntry,
)


def build_kb() -> None:
    """Build the knowledgebase by generating markdown files from templates and data."""
    # Find the .kbmd directory
    kbmd_dir = _find_kbmd_directory()
    if not kbmd_dir:
        raise RuntimeError("No .kbmd directory found. Run 'kbmd init' first.")

    # Set up Jinja2 environment
    template_loader = jinja2.FileSystemLoader(kbmd_dir / "templates")
    jinja_env = jinja2.Environment(loader=template_loader, autoescape=True)

    print("Building knowledgebase...")

    # Build datasets
    datasets_built = _build_datasets(kbmd_dir, jinja_env)
    print(f"Generated {datasets_built} dataset pages")

    # Build projects
    projects_built = _build_projects(kbmd_dir, jinja_env)
    print(f"Generated {projects_built} project pages")

    # Update and build indices
    _update_indices(kbmd_dir)
    indices_built = _build_indices(kbmd_dir, jinja_env)
    print(f"Generated {indices_built} index pages")

    # Build main README
    _build_main_readme(kbmd_dir, jinja_env)
    print("Generated main README.md")

    print("✓ Build completed successfully!")


def _find_kbmd_directory() -> Optional[Path]:
    """Find the .kbmd directory by walking up the directory tree."""
    current = Path.cwd()

    while current != current.parent:
        kbmd_dir = current / ".kbmd"
        if kbmd_dir.exists() and kbmd_dir.is_dir():
            return kbmd_dir
        current = current.parent

    return None


def _build_datasets(kbmd_dir: Path, jinja_env: jinja2.Environment) -> int:
    """Build dataset markdown files from data and templates."""
    template = jinja_env.get_template("dataset.jinja")
    datasets_dir = kbmd_dir / "data" / "datasets"
    output_dir = kbmd_dir / "generated" / "datasets"
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for data_file in datasets_dir.glob("*.json"):
        dataset_data = json.loads(data_file.read_text())
        dataset = DatasetMetadata(**dataset_data)

        # Add generated date for template
        template_vars = dataset.model_dump()
        template_vars["generated_date"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Generate markdown
        markdown_content = template.render(**template_vars)

        # Write to output file
        output_file = output_dir / f"{dataset.slug}.md"
        output_file.write_text(markdown_content)
        count += 1

    return count


def _build_projects(kbmd_dir: Path, jinja_env: jinja2.Environment) -> int:
    """Build project markdown files from data and templates."""
    template = jinja_env.get_template("project.jinja")
    projects_dir = kbmd_dir / "data" / "projects"
    output_dir = kbmd_dir / "generated" / "projects"
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for data_file in projects_dir.glob("*.json"):
        project_data = json.loads(data_file.read_text())
        project = ProjectMetadata(**project_data)

        # Add generated date for template
        template_vars = project.model_dump()
        template_vars["generated_date"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Convert date objects to strings for template
        if "date_started" in template_vars and template_vars["date_started"]:
            template_vars["date_started"] = template_vars["date_started"]
        if "date_completed" in template_vars and template_vars["date_completed"]:
            template_vars["date_completed"] = template_vars["date_completed"]

        # Generate markdown
        markdown_content = template.render(**template_vars)

        # Write to output file
        output_file = output_dir / f"{project.slug}.md"
        output_file.write_text(markdown_content)
        count += 1

    return count


def _update_indices(kbmd_dir: Path) -> None:
    """Update index data files with current datasets and projects."""
    # Update filesystem index
    _update_filesystem_index(kbmd_dir)

    # Update topic index
    _update_topic_index(kbmd_dir)


def _update_filesystem_index(kbmd_dir: Path) -> None:
    """Update the filesystem-based index with current datasets."""
    datasets_dir = kbmd_dir / "data" / "datasets"
    projects_dir = kbmd_dir / "data" / "projects"

    # Group by filesystem path
    filesystem_groups: Dict[str, List[IndexEntry]] = {}

    # Add datasets
    for data_file in datasets_dir.glob("*.json"):
        dataset_data = json.loads(data_file.read_text())
        dataset = DatasetMetadata(**dataset_data)

        # Extract filesystem root (e.g., /scratch, /projects, /cold)
        path_parts = Path(dataset.path).parts
        fs_root = f"/{path_parts[1]}" if len(path_parts) > 1 else "/"

        if fs_root not in filesystem_groups:
            filesystem_groups[fs_root] = []

        filesystem_groups[fs_root].append(
            IndexEntry(
                name=dataset.name,
                link=f"../datasets/{dataset.slug}.md",
                description=dataset.description[:100] + "..."
                if len(dataset.description) > 100
                else dataset.description,
            )
        )

    # Add projects
    for data_file in projects_dir.glob("*.json"):
        project_data = json.loads(data_file.read_text())
        project = ProjectMetadata(**project_data)

        # Extract filesystem root
        path_parts = Path(project.path).parts
        fs_root = f"/{path_parts[1]}" if len(path_parts) > 1 else "/"

        if fs_root not in filesystem_groups:
            filesystem_groups[fs_root] = []

        filesystem_groups[fs_root].append(
            IndexEntry(
                name=project.name,
                link=f"../projects/{project.slug}.md",
                description=project.description[:100] + "..."
                if len(project.description) > 100
                else project.description,
            )
        )

    # Create index metadata
    categories = [
        IndexCategory(category=fs_root, entries=items)
        for fs_root, items in sorted(filesystem_groups.items())
    ]

    index = IndexMetadata(
        title="Browse by Filesystem Location",
        description="Datasets and projects organized by their location on different filesystems",
        entries=categories,
    )

    # Save updated index
    index_file = kbmd_dir / "data" / "indices" / "by-filesystem.json"
    index_file.write_text(index.model_dump_json(indent=2))


def _update_topic_index(kbmd_dir: Path) -> None:
    """Update the topic-based index with current projects."""
    projects_dir = kbmd_dir / "data" / "projects"

    # Group by tags (topics)
    topic_groups: Dict[str, List[IndexEntry]] = {}

    for data_file in projects_dir.glob("*.json"):
        project_data = json.loads(data_file.read_text())
        project = ProjectMetadata(**project_data)

        # Use tags as topics, or "Untagged" if no tags
        topics = project.tags if project.tags else ["Untagged"]

        for topic in topics:
            if topic not in topic_groups:
                topic_groups[topic] = []

            topic_groups[topic].append(
                IndexEntry(
                    name=project.name,
                    link=f"../projects/{project.slug}.md",
                    description=project.description[:100] + "..."
                    if len(project.description) > 100
                    else project.description,
                )
            )

    # Create index metadata
    categories = [
        IndexCategory(category=topic, entries=items)
        for topic, items in sorted(topic_groups.items())
    ]

    index = IndexMetadata(
        title="Browse by Research Topic",
        description="Projects organized by research topic and domain",
        entries=categories,
    )

    # Save updated index
    index_file = kbmd_dir / "data" / "indices" / "by-topic.json"
    index_file.write_text(index.model_dump_json(indent=2))


def _build_indices(kbmd_dir: Path, jinja_env: jinja2.Environment) -> int:
    """Build index markdown files from data and templates."""
    template = jinja_env.get_template("index.jinja")
    indices_dir = kbmd_dir / "data" / "indices"
    output_dir = kbmd_dir / "generated" / "indices"
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for data_file in indices_dir.glob("*.json"):
        index_data = json.loads(data_file.read_text())
        index = IndexMetadata(**index_data)

        # Add generated date for template
        template_vars = index.model_dump()
        template_vars["generated_date"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        template_vars["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d")

        # Generate markdown
        markdown_content = template.render(**template_vars)

        # Write to output file
        output_file = output_dir / f"{data_file.stem}.md"
        output_file.write_text(markdown_content)
        count += 1

    return count


def _build_main_readme(kbmd_dir: Path, jinja_env: jinja2.Environment) -> None:
    """Build the main README.md from the root template."""
    template = jinja_env.get_template("root.jinja")

    # Load configuration for project name
    config_file = kbmd_dir / "config.json"
    config_data = {}
    if config_file.exists():
        config_data = json.loads(config_file.read_text())

    project_name = config_data.get("name", Path.cwd().name)

    # Generate markdown
    markdown_content = template.render(project_name=project_name)

    # Write to generated folder
    output_file = kbmd_dir / "generated" / "README.md"
    output_file.write_text(markdown_content)
