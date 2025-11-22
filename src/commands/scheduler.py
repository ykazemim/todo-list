"""Scheduler for periodic tasks using the Schedule library."""

import time
import schedule
from src.commands.autoclose_overdue import autoclose_overdue_tasks


def run_scheduler() -> None:
    """Run the scheduler to execute periodic tasks.

    Currently schedules:
    - Autoclose overdue tasks: runs daily at midnight
    """
    # Schedule autoclose-overdue to run daily at midnight
    schedule.every().day.at("00:00").do(autoclose_overdue_tasks)

    print("📅 Scheduler started. Autoclose-overdue will run daily at 00:00")
    print("Press Ctrl+C to stop the scheduler.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n👋 Scheduler stopped.")


if __name__ == "__main__":
    run_scheduler()
