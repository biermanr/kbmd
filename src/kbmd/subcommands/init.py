"""Initialize a knowledgebase in the current git-managed folder."""

from pathlib import Path
from git import Repo, InvalidGitRepositoryError


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
