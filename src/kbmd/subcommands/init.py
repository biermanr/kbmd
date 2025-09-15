"""Initialize a knowledgebase in the current git-managed folder."""

from pathlib import Path
from git import Repo, InvalidGitRepositoryError

from kbmd.jinja_templates import get_available_templates
from kbmd.models import KnowledgebaseConfig, IndexMetadata


def init_kb() -> None:
    """Initialize a knowledgebase in the current git-managed folder."""
    try:
        repo = Repo(Path.cwd())
    except InvalidGitRepositoryError:
        raise RuntimeError("Current directory is not a git repository.")

    kbmd_dir = Path.cwd() / ".kbmd"

    try:
        kbmd_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise RuntimeError(".kbmd directory already exists in the current directory.")

    # Create directory structure
    _create_directory_structure(kbmd_dir)

    # Copy all templates from package resources
    _copy_templates(kbmd_dir)

    # Create initial configuration
    _create_initial_config(kbmd_dir, repo)

    # Create initial data files
    _create_initial_data_files(kbmd_dir)

    print(f"Initialized kbmd knowledgebase in {kbmd_dir}")


def _create_directory_structure(kbmd_dir: Path) -> None:
    """Create the complete .kbmd directory structure."""
    directories = [
        "templates",
        "data",
        "data/datasets",
        "data/projects",
        "data/indices",
        "generated",
        "generated/datasets",
        "generated/projects",
        "generated/indices",
    ]

    for directory in directories:
        (kbmd_dir / directory).mkdir(parents=True, exist_ok=True)


def _copy_templates(kbmd_dir: Path) -> None:
    """Copy all template files from package resources to .kbmd/templates/."""
    templates_dir = kbmd_dir / "templates"

    all_available_templates = get_available_templates()
    for template_path in all_available_templates:
        target_path = templates_dir / template_path.name
        target_path.write_text(template_path.read_text())


def _create_initial_config(kbmd_dir: Path, repo: Repo) -> None:
    """Create initial project-specific configuration."""
    repo_name = Path.cwd().name

    config = KnowledgebaseConfig(
        name=repo_name,
        description=f"Knowledgebase for {repo_name}",
        git_repo_path=str(Path.cwd().absolute()),
    )

    config_path = kbmd_dir / "config.json"
    config_path.write_text(config.model_dump_json(indent=2))


def _create_initial_data_files(kbmd_dir: Path) -> None:
    """Create initial index data files."""
    # Create filesystem-based index
    filesystem_index = IndexMetadata(
        title="Datasets by Filesystem Location",
        description="Browse datasets organized by their location on different filesystems",
    )

    filesystem_index_path = kbmd_dir / "data" / "indices" / "by-filesystem.json"
    filesystem_index_path.write_text(filesystem_index.model_dump_json(indent=2))

    # Create topic-based index
    topic_index = IndexMetadata(
        title="Projects by Research Topic",
        description="Browse projects organized by research topic and domain",
    )

    topic_index_path = kbmd_dir / "data" / "indices" / "by-topic.json"
    topic_index_path.write_text(topic_index.model_dump_json(indent=2))
