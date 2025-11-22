"""Command to automatically close overdue tasks."""

from src.db.session import get_session
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


def autoclose_overdue_tasks() -> int:
    """Automatically close overdue tasks.

    Finds all tasks where deadline < today and status != done,
    marks them as done and sets closed_at timestamp.

    :return: Number of tasks closed
    """
    session_gen = get_session()
    session = next(session_gen)

    try:
        task_repo = TaskRepository(session)
        task_service = TaskService(task_repo)
        count = task_service.autoclose_overdue_tasks()
        return count
    finally:
        session.close()


if __name__ == "__main__":
    count = autoclose_overdue_tasks()
    print(f"Closed {count} overdue task(s).")
