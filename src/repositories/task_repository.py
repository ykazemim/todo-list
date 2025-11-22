"""SQLAlchemy repository for Task operations."""

from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.models.task import Task, StatusType
from src.models.project import Project
from src.exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    LimitExceededError,
    ValidationError,
)
from src.config.settings import (
    MAX_NUMBER_OF_TASKS_PER_PROJECT,
    MAX_TASK_TITLE_WORDS,
    MAX_TASK_DESCRIPTION_WORDS,
)

VALID_STATUSES: list[StatusType] = ["todo", "doing", "done"]


class TaskRepository:
    """Repository for Task database operations."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        :param session: SQLAlchemy database session
        """
        self.session = session

    def add(
        self,
        project_id: int,
        title: str,
        description: str,
        status: StatusType = "todo",
        deadline: Optional[str] = None,
    ) -> Task:
        """Add a task to a project.

        :param project_id: Parent project ID
        :param title: Task title
        :param description: Task description
        :param status: Task status (default: todo)
        :param deadline: Optional deadline string (YYYY-MM-DD)
        :return: Created task
        :raises ProjectNotFoundError: If project doesn't exist
        :raises LimitExceededError: If maximum number of tasks is reached
        :raises ValidationError: If validation fails
        """
        # Verify project exists
        project = self.session.get(Project, project_id)
        if not project:
            raise ProjectNotFoundError(
                f"Project with ID {project_id} not found."
            )

        # Check task count for project
        count = self.session.scalar(
            select(func.count(Task.id)).where(Task.project_id == project_id)
        )
        if count and count >= MAX_NUMBER_OF_TASKS_PER_PROJECT:
            raise LimitExceededError(
                "Maximum number of tasks reached for this project."
            )

        if not title or title.strip() == "":
            raise ValidationError("Task title cannot be empty.")
        if len(title) > MAX_TASK_TITLE_WORDS:
            raise ValidationError(
                f"Task title must be ≤ {MAX_TASK_TITLE_WORDS} characters."
            )
        if description and len(description) > MAX_TASK_DESCRIPTION_WORDS:
            raise ValidationError(
                f"Task description must be ≤ {MAX_TASK_DESCRIPTION_WORDS} characters."
            )
        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task_deadline: Optional[date] = None
        if deadline:
            try:
                task_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Deadline must be in YYYY-MM-DD format.")

        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            deadline=task_deadline,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_by_id(self, project_id: int, task_id: int) -> Task:
        """Get a task by ID within a project.

        :param project_id: Parent project ID
        :param task_id: Task ID
        :return: Task if found
        :raises ProjectNotFoundError: If project doesn't exist
        :raises TaskNotFoundError: If task doesn't exist
        """
        project = self.session.get(Project, project_id)
        if not project:
            raise ProjectNotFoundError(
                f"Project with ID {project_id} not found."
            )

        task = self.session.get(Task, task_id)
        if not task or task.project_id != project_id:
            raise TaskNotFoundError(
                f"Task with ID {task_id} not found in project {project_id}."
            )
        return task

    def list_by_project(self, project_id: int) -> List[Task]:
        """List all tasks for a project.

        :param project_id: Parent project ID
        :return: List of tasks
        :raises ProjectNotFoundError: If project doesn't exist
        """
        project = self.session.get(Project, project_id)
        if not project:
            raise ProjectNotFoundError(
                f"Project with ID {project_id} not found."
            )

        stmt = select(Task).where(Task.project_id == project_id).order_by(Task.id)
        return list(self.session.scalars(stmt).all())

    def update(
        self,
        project_id: int,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> Task:
        """Update a task's attributes.

        :param project_id: Parent project ID
        :param task_id: Task ID
        :param title: New task title (optional)
        :param description: New task description (optional)
        :param status: New task status (optional)
        :param deadline: New deadline string YYYY-MM-DD (optional)
        :return: Updated task
        :raises ProjectNotFoundError: If project doesn't exist
        :raises TaskNotFoundError: If task doesn't exist
        :raises ValidationError: If validation fails
        """
        task = self.get_by_id(project_id, task_id)

        if title is not None:
            if not (1 <= len(title) <= MAX_TASK_TITLE_WORDS):
                raise ValidationError(
                    f"Title must be 1–{MAX_TASK_TITLE_WORDS} characters."
                )
            task.title = title

        if description is not None:
            if not (1 <= len(description) <= MAX_TASK_DESCRIPTION_WORDS):
                raise ValidationError(
                    f"Description must be 1–{MAX_TASK_DESCRIPTION_WORDS} characters."
                )
            task.description = description

        if status is not None:
            if status not in VALID_STATUSES:
                raise ValidationError("Invalid status.")
            task.status = status

        if deadline is not None:
            task_deadline: Optional[date] = None
            if deadline:
                try:
                    task_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
                except ValueError:
                    raise ValidationError("Deadline must be in YYYY-MM-DD format.")
            task.deadline = task_deadline

        self.session.commit()
        self.session.refresh(task)
        return task

    def change_status(
        self, project_id: int, task_id: int, status: StatusType
    ) -> Task:
        """Change only the status of a task.

        :param project_id: Parent project ID
        :param task_id: Task ID
        :param status: New status
        :return: Updated task
        :raises ProjectNotFoundError: If project doesn't exist
        :raises TaskNotFoundError: If task doesn't exist
        :raises ValidationError: If status is invalid
        """
        task = self.get_by_id(project_id, task_id)

        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task.status = status
        if status == "done" and not task.closed_at:
            task.closed_at = datetime.utcnow()
        elif status != "done":
            task.closed_at = None

        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, project_id: int, task_id: int) -> None:
        """Delete a task by ID within a project.

        :param project_id: Parent project ID
        :param task_id: Task ID
        :raises ProjectNotFoundError: If project doesn't exist
        :raises TaskNotFoundError: If task doesn't exist
        """
        task = self.get_by_id(project_id, task_id)
        self.session.delete(task)
        self.session.commit()

    def find_overdue_tasks(self) -> List[Task]:
        """Find all overdue tasks that are not done.

        :return: List of overdue tasks
        """
        today = date.today()
        stmt = (
            select(Task)
            .where(Task.deadline < today)
            .where(Task.status != "done")
        )
        return list(self.session.scalars(stmt).all())
