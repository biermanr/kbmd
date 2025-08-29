"""CLI for kbmd: Knowledgebase markdown CLI tool."""

import argparse
from kbmd import config


def main() -> None:
    """Entry point for the kbmd CLI."""
    parser = argparse.ArgumentParser(
        description="kbmd: Manage knowledgebase markdown files via CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Stub for "status" command
    subparsers.add_parser(
        "status",
        help="Display information about available knowledgebases and which knowledgebase is currently active",
    )

    # Stub for "add" command
    subparsers.add_parser(
        "add", help="Add a new project or dataset to the knowledgebase"
    )
    # TODO: add arguments for "add"

    # Stub for "push" command
    subparsers.add_parser("push", help="Push local changes to remote repository")
    # TODO: add arguments for "push"

    # Stub for "fresh" command
    subparsers.add_parser("fresh", help="Refresh metadata for all tracked files")
    # TODO: add arguments for "fresh"

    args = parser.parse_args()

    if args.command == "status":
        cfg = config.load_config()
        print(f"Configuration schema version: {cfg.schema_version}")
        print(f"Configuration path: {cfg.config_path}")
        if cfg.kbs:
            print("Knowledgebases:")
            for kb_name, kb_info in cfg.kbs.items():
                print(f"  - {kb_name}: {kb_info}")
        else:
            print("No knowledgebases configured.")


if __name__ == "__main__":
    main()
