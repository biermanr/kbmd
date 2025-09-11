"""Template utilities for kbmd package."""

import importlib.resources
import pathlib
from typing import Iterator


def get_available_templates() -> Iterator[pathlib.Path]:
    """Get an iterator of available jinja template files."""
    templates_dir = importlib.resources.files("kbmd.templates")
    jinja_templates = templates_dir.glob("*.jinja")
    return jinja_templates
