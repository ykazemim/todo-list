"""Service layer for Task business logic."""

from typing import List, Optional
from datetime import datetime
from src.models.task import Task, StatusType
from src.repositories.task_repository import TaskRepository


class TaskService:
    """Service for Task operations."""

    def __init__(self, task_repository: TaskRepository) -> None:
        """Initialize service with task repository.

        :param task_repository: Task repository instance
        """
        self.task_repository = task_repository

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str,
        status: StatusType = "todo",
        deadline: Optional[str] = None,
    ) -> Task:
        """Create a new task.

        :param project_id: Parent project ID
        :param title: Task title
        :param description: Task description
        :param status: Task status (default: todo)
        :param deadline: Optional deadline string (YYYY-MM-DD)
        :return: Created task
        """
        return self.task_repository.add(
            project_id, title, description, status, deadline
        )

    def list_tasks(self, project_id: int) -> List[Task]:
        """List all tasks for a project.

        :param project_id: Parent project ID
        :return: List of tasks
        """
        return self.task_repository.list_by_project(project_id)

    def get_task(self, project_id: int, task_id: int) -> Task:
        """Get a task by ID.

        :param project_id: Parent project ID
        :param task_id: Task ID
        :return: Task if found
        """
        return self.task_repository.get_by_id(project_id, task_id)

    def update_task(
        self,
        project_id: int,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> Task:
        """Update a task.

        :param project_id: Parent project ID
        :param task_id: Task ID
        :param title: New task title (optional)
        :param description: New task description (optional)
        :param status: New task status (optional)
        :param deadline: New deadline string YYYY-MM-DD (optional)
        :return: Updated task
        """
        return self.task_repository.update(
            project_id, task_id, title, description, status, deadline
        )

    def change_task_status(
        self, project_id: int, task_id: int, status: StatusType
    ) -> Task:
        """Change task status.

        :param project_id: Parent project ID
        :param task_id: Task ID
        :param status: New status
        :return: Updated task
        """
        return self.task_repository.change_status(project_id, task_id, status)

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task.

        :param project_id: Parent project ID
        :param task_id: Task ID
        """
        self.task_repository.delete(project_id, task_id)

    def autoclose_overdue_tasks(self) -> int:
        """Automatically close overdue tasks.

        Marks overdue tasks (deadline < today and status != done) as done
        and sets closed_at timestamp.

        :return: Number of tasks closed
        """
        overdue_tasks = self.task_repository.find_overdue_tasks()
        count = 0

        for task in overdue_tasks:
            self.task_repository.change_status(
                task.project_id, task.id, "done"
            )
            count += 1

        return count
