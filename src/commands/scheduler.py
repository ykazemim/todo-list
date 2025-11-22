"""Scheduler for periodic tasks using the Schedule library."""

import time
import sys
import signal
import logging
from pathlib import Path
from schedule import Scheduler
from src.commands.autoclose_overdue import autoclose_overdue_tasks

# Configure logging
log_dir = Path.home() / ".todo-list"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "scheduler.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


class DaemonScheduler:
    """Daemon scheduler that runs in the background."""

    def __init__(self) -> None:
        """Initialize the scheduler."""
        self.scheduler = Scheduler()
        self.running = True
        self._setup_signal_handlers()

    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""

        def signal_handler(signum: int, frame: object) -> None:
            """Handle shutdown signals."""
            logger.info("Received shutdown signal, stopping scheduler...")
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _run_autoclose(self) -> None:
        """Run autoclose and handle errors."""
        try:
            count = autoclose_overdue_tasks()
            if count > 0:
                logger.info(f"Successfully closed {count} overdue task(s).")
            else:
                logger.debug("No overdue tasks found.")
        except Exception as e:
            logger.error(f"Error running autoclose: {str(e)}", exc_info=True)

    def start(self) -> None:
        """Start the scheduler daemon."""
        # Schedule autoclose-overdue to run daily at midnight
        self.scheduler.every().day.at("00:00").do(self._run_autoclose)

        logger.info("Scheduler daemon started.")
        logger.info("Autoclose-overdue will run daily at 00:00")
        logger.info(f"Logs are written to: {log_file}")

        try:
            while self.running:
                self.scheduler.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler interrupted by user.")
        finally:
            logger.info("Scheduler daemon stopped.")


def run_scheduler() -> None:
    """Run the scheduler as a daemon."""
    daemon = DaemonScheduler()
    daemon.start()


if __name__ == "__main__":
    run_scheduler()
