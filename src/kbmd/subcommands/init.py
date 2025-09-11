"""Initialize a knowledgebase in the current git-managed folder."""

from pathlib import Path
from git import Repo, InvalidGitRepositoryError

from kbmd.jinja_templates import get_available_templates


def init_kb() -> None:
    """Initialize a knowledgebase in the current git-managed folder."""
    try:
        _ = Repo(Path.cwd())
    except InvalidGitRepositoryError:
        raise RuntimeError("Current directory is not a git repository.")

    kbmd_dir = Path.cwd() / ".kbmd"

    try:
        kbmd_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise RuntimeError(".kbmd directory already exists in the current directory.")

    # Create a root.jinja template
    all_available_templates = get_available_templates()
    root_template = next(
        (t for t in all_available_templates if t.name == "root.jinja"), None
    )
    if root_template is None:
        raise RuntimeError("root.jinja template not found in available templates.")
    target_path = kbmd_dir / "root.jinja"
    if target_path.exists():
        raise RuntimeError("root.jinja already exists in the .kbmd directory.")

    target_path.write_text(root_template.read_text())
