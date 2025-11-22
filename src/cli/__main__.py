"""CLI entry point for commands."""

import sys


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: todolist <command>")
        print("Commands:")
        print("  tasks:autoclose-overdue  - Automatically close overdue tasks")
        sys.exit(1)

    # Join all args to handle commands like "tasks:autoclose-overdue"
    command = " ".join(sys.argv[1:])

    if command == "tasks:autoclose-overdue":
        from src.cli.commands import handle_autoclose_overdue

        handle_autoclose_overdue()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: tasks:autoclose-overdue")
        sys.exit(1)


if __name__ == "__main__":
    main()
