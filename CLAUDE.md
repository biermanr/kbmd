# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`kbmd` is a CLI tool for managing knowledgebases as markdown files in git repositories. The tool helps researchers track datasets and projects across shared HPC clusters by creating structured markdown files with standardized metadata schemas.

## Architecture

This is a Python CLI application built with:
- **CLI Framework**: argparse with subcommands (`status`, `init`, `build`, `push`, `fresh`)
- **Configuration**: Pydantic models for config validation in `config.py`
- **Templates**: Jinja2 templates for generating markdown files
- **Project Structure**:
  - `src/kbmd/cli.py` - Main CLI entry point
  - `src/kbmd/config.py` - Configuration management
  - `src/kbmd/subcommands/` - Individual command implementations
  - `src/kbmd/templates/` - Jinja2 templates for markdown generation
  - `src/kbmd/jinja_templates.py` - Template loading utilities

## Development Commands

### Dependencies and Environment
```bash
# Install dependencies (uses uv package manager)
uv sync

# Install with dev dependencies
uv sync --dev
```

### Code Quality
```bash
# Format code
ruff format

# Lint and fix issues
ruff check --fix

# Type checking
mypy src/kbmd

# Run pre-commit hooks
pre-commit run --all-files
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=kbmd

# Run specific test file
pytest tests/config_test.py
```

### Building and Installation
```bash
# Build package
uv build

# Install locally for development
uv pip install -e .

# Run CLI directly
kbmd --help
```

## Code Standards

- Python 3.10+ required
- Uses `ruff` for linting and formatting with docstring requirements (D rules enabled)
- Type checking with `mypy` in strict mode
- Double quotes for strings (configured in ruff)
- Pre-commit hooks enforce code quality

## Key Dependencies

- `gitpython` - Git repository operations
- `jinja2` - Template rendering for markdown files
- `pydantic` - Configuration validation and data models

## Implementation Status

Currently implementing basic CLI structure. The `init` and `build` subcommands have stub implementations in `src/kbmd/subcommands/`. The main workflow involves creating `.kbmd/` directories in git repositories to store knowledgebase configuration and generated markdown files.
