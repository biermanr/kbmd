"""CLI for kbmd: Knowledgebase markdown CLI tool."""

import argparse
from kbmd import config
from kbmd.subcommands.init import init_kb
from kbmd.subcommands.add import add_entry
from kbmd.subcommands.build import build_kb


def main() -> None:
    """Entry point for the kbmd CLI."""
    parser = argparse.ArgumentParser(
        description="kbmd: Manage knowledgebase markdown files via CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "status",
        help="Display information about available knowledgebases and which knowledgebase is currently active",
    )

    subparsers.add_parser(
        "init",
        help="Initialize the current git-managed folder to include a knowledgebase",
    )

    # Add command
    add_parser = subparsers.add_parser(
        "add", help="Add a new dataset or project to the knowledgebase"
    )
    add_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the dataset or project (default: current directory)",
    )
    add_parser.add_argument(
        "--type",
        choices=["dataset", "project"],
        required=True,
        help="Type of entry to create",
    )

    subparsers.add_parser("build", help="Build or compile the knowledgebase content")

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
    elif args.command == "init":
        init_kb()
    elif args.command == "add":
        add_entry(args.path, args.type)
    elif args.command == "build":
        build_kb()


if __name__ == "__main__":
    main()
