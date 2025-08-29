"""Reading and writing the kbmd configuration file."""

import abc
import os
import pathlib
import warnings
from typing import Type

import pydantic


def get_kbmd_config_path() -> pathlib.Path:
    """Return the path to the kbmd configuration file, considering environment overrides."""
    return pathlib.Path(
        os.environ.get("KBMD_CONFIG_PATH", pathlib.Path.home() / ".kbmd_config.json")
    )


def get_kbmd_schema_version() -> str:
    """Return the kbmd configuration schema version, considering environment overrides."""
    return os.environ.get(
        "KBMD_SCHEMA_VERSION", "001"
    )  # NOTE maybe lift default schema version to __init__.py?


# Abstract base classes for configuration
class AbstractConfig(pydantic.BaseModel, abc.ABC):
    """Base class for kbmd configuration schemas."""

    schema_version: str = pydantic.Field(default_factory=get_kbmd_schema_version)
    config_path: pathlib.Path = pydantic.Field(default_factory=get_kbmd_config_path)
    kbs: dict[str, pathlib.Path] = pydantic.Field(default_factory=dict)


SCHEMA_VERSIONS: dict[str, Type[AbstractConfig]] = {}


def register_config_schema_version(cls: Type[AbstractConfig]) -> Type[AbstractConfig]:
    """Decorator to register a configuration schema version with the SCHEMA_VERSIONS dict."""
    version = cls.model_fields[
        "schema_version"
    ].default  # is this the best way to access the schema version?
    SCHEMA_VERSIONS[version] = cls
    return cls


@register_config_schema_version
class Config001(AbstractConfig):
    """Configuration schema version 001."""

    schema_version: str = "001"


def write_config(config: AbstractConfig) -> None:
    """Write the given configuration instance to its config_path in JSON format."""
    config_path = config.config_path
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w") as f:
        f.write(config.model_dump_json(indent=2))


def load_config() -> AbstractConfig:
    """Load a configuration file.

    Returns:
        An instance of the configuration model corresponding to the schema version.
        If the configuration file does not exist, creates it and returns a default instance.

    Raises:
        ValueError: If the specified schema version is not supported.

    """
    schema_version = get_kbmd_schema_version()
    config_path = get_kbmd_config_path()

    config_cls = SCHEMA_VERSIONS.get(schema_version)
    if config_cls is None:
        raise ValueError(f"Unsupported schema version: {schema_version}")

    if not config_path.exists():
        warnings.warn(
            f"Configuration file not found at {config_path}, continuing with default configuration of schema {schema_version}.",
            UserWarning,
        )
        config = config_cls()
        write_config(config)
    else:
        with config_path.open() as f:
            config = config_cls.model_validate_json(f.read())

    return config
