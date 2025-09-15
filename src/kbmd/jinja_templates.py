"""Template utilities for kbmd package."""

import importlib.resources
from typing import Iterator
from importlib.resources.abc import Traversable


def get_available_templates() -> Iterator[Traversable]:
    """Get an iterator of available jinja template files."""
    templates_dir = importlib.resources.files("kbmd.templates")
    # Filter for .jinja files
    for item in templates_dir.iterdir():
        if item.name.endswith(".jinja"):
            yield item
