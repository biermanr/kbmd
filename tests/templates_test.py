"""Test template functionality."""

from kbmd.jinja_templates import get_available_templates


def test_root_template_exists():
    """Test that the root.jinja template is available."""
    templates = get_available_templates()
    template_names = [p.name for p in templates]
    assert "root.jinja" in template_names
