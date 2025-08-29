"""Tests for kbmd.config module."""

import os

import pytest
import pathlib

import kbmd.config


def test_missing_schema_version():
    """Test that loading a config with an unsupported schema version raises ValueError."""
    os.environ["KBMD_SCHEMA_VERSION"] = "unsupported_version"
    with pytest.raises(ValueError):
        kbmd.config.load_config()
    del os.environ["KBMD_SCHEMA_VERSION"]


def test_kbmd_config_path_env_var(tmp_path):
    """Test that the KBMD_CONFIG_PATH environment variable overrides the default config path."""
    # Set environment variable to a custom config path
    env_path = tmp_path / "env_config.json"
    os.environ["KBMD_CONFIG_PATH"] = str(env_path)

    # Load config without specifying config_path should use env var path
    with pytest.warns(UserWarning):
        cfg = kbmd.config.load_config()

    assert cfg.config_path == env_path
    assert cfg.kbs == {}

    # The config file should now exist at the env path
    assert env_path.exists()

    # Cleanup environment variable
    del os.environ["KBMD_CONFIG_PATH"]


def test_load_missing_config_schema_001(tmp_path):
    """Test loading a missing config file for schema version 001 creates and writes a default config."""
    os.environ["KBMD_CONFIG_PATH"] = str(tmp_path / "nonexistent_config.json")
    os.environ["KBMD_SCHEMA_VERSION"] = "001"
    config_path = pathlib.Path(os.environ["KBMD_CONFIG_PATH"])

    # Load config should create a default config and write it out
    with pytest.warns(UserWarning):
        cfg = kbmd.config.load_config()

    assert cfg.config_path == config_path
    assert cfg.kbs == {}

    # The config file should now exist
    assert config_path.exists()

    # Reloading should yield an equivalent config instance
    reloaded_cfg = kbmd.config.load_config()
    assert reloaded_cfg == cfg

    del os.environ["KBMD_CONFIG_PATH"]
    del os.environ["KBMD_SCHEMA_VERSION"]


def test_write_config_schema_001(tmp_path):
    """Test writing and then reading a config for schema version 001."""
    config_path = tmp_path / "config.json"
    os.environ["KBMD_CONFIG_PATH"] = str(config_path)
    os.environ["KBMD_SCHEMA_VERSION"] = "001"

    cfg = kbmd.config.Config001(config_path=config_path)

    assert not config_path.exists()
    kbmd.config.write_config(cfg)
    assert config_path.exists()

    cfg = kbmd.config.load_config()
    assert cfg.config_path == config_path
    assert cfg.kbs == {}

    del os.environ["KBMD_CONFIG_PATH"]
    del os.environ["KBMD_SCHEMA_VERSION"]
