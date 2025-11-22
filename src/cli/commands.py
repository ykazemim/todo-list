"""CLI command handlers."""

import sys
from src.commands.autoclose_overdue import autoclose_overdue_tasks


def handle_autoclose_overdue() -> None:
    """Handle the autoclose-overdue command."""
    try:
        count = autoclose_overdue_tasks()
        if count > 0:
            print(f"✅ Successfully closed {count} overdue task(s).")
        else:
            print("ℹ️  No overdue tasks found.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
