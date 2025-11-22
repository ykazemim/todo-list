from typing import Dict, List, Optional, Literal
from datetime import datetime, date
from src.models.project import Project
from src.models.task import Task, StatusType
from src.exceptions.todo_exceptions import (
    ValidationError,
    ProjectNotFoundError,
    TaskNotFoundError,
    LimitExceededError,
)
from src.config.settings import (
    MAX_NUMBER_OF_PROJECTS,
    MAX_NUMBER_OF_TASKS_PER_PROJECT,
    MAX_PROJECT_NAME_WORDS,
    MAX_PROJECT_DESCRIPTION_WORDS,
    MAX_TASK_TITLE_WORDS,
    MAX_TASK_DESCRIPTION_WORDS,
)

VALID_STATUSES: list[StatusType] = ["todo", "doing", "done"]


class InMemoryRepository:
    """Stores Projects and Tasks in memory with basic validation."""

    def __init__(self) -> None:
        self.projects: Dict[int, Project] = {}
        self.next_project_id: int = 1
        self.next_task_id: int = 1

    # ---------- Project CRUD ----------
    def add_project(self, name: str, description: str) -> Project:
        """Create and store a new project with validation.
        Raises:
            ValidationError: If validation fails.
            LimitExceededError: If maximum number of projects is reached.
        """
        if len(name) <= 0:
            raise ValidationError("Project name cannot be empty.")
        if len(self.projects) >= MAX_NUMBER_OF_PROJECTS:
            raise LimitExceededError("Maximum number of projects reached.")
        if any(p.name == name for p in self.projects.values()):
            raise ValidationError(f"Project name '{name}' already exists.")
        if len(name) > MAX_PROJECT_NAME_WORDS:
            raise ValidationError(f"Project name must be ≤ {MAX_PROJECT_NAME_WORDS} characters.")
        if len(description) > MAX_PROJECT_DESCRIPTION_WORDS:
            raise ValidationError(f"Project description must be ≤ {MAX_PROJECT_DESCRIPTION_WORDS} characters.")

        project = Project(id=self.next_project_id, name=name, description=description)
        self.projects[self.next_project_id] = project
        self.next_project_id += 1
        return project

    def list_projects(self) -> List[Project]:
        """Return all projects sorted by creation time (ID)."""
        return sorted(self.projects.values(), key=lambda p: p.id)

    # ---------- Task CRUD ----------
    def add_task(
            self,
            project_id: int,
            title: str,
            description: str,
            status: StatusType = "todo",
            deadline: Optional[str] = None,
    ) -> Task:
        """Add a task to a project.
        Raises:
            ProjectNotFoundError: If project doesn't exist.
            LimitExceededError: If maximum number of tasks is reached.
            ValidationError: If validation fails.
        """
        project = self.projects.get(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

        if len(project.tasks) >= MAX_NUMBER_OF_TASKS_PER_PROJECT:
            raise LimitExceededError("Maximum number of tasks reached for this project.")
        if title is None or title.strip() == "":
            raise ValidationError("Task title cannot be empty.")
        if len(title) > MAX_TASK_TITLE_WORDS:
            raise ValidationError(f"Task title must be ≤ {MAX_TASK_TITLE_WORDS} characters.")
        if description and len(description) > MAX_TASK_DESCRIPTION_WORDS:
            raise ValidationError(f"Task description must be ≤ {MAX_TASK_DESCRIPTION_WORDS} characters.")
        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task_deadline: Optional[date] = None
        if deadline:
            try:
                task_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Deadline must be in YYYY-MM-DD format.")

        task = Task(
            id=self.next_task_id,
            title=title,
            description=description,
            status=status,
            deadline=task_deadline,
        )
        self.next_task_id += 1
        project.tasks.append(task)
        return task

    def change_task_status(self, project_id: int, task_id: int, status: StatusType) -> Task:
        """Change only the status of a task.
        Raises:
            ProjectNotFoundError: If project doesn't exist.
            TaskNotFoundError: If task doesn't exist.
            ValidationError: If status is invalid.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")
        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task.status = status
        return task

    def list_all_projects(self) -> List[Project]:
        """Return all projects sorted by creation time.
        If no projects exist, returns an empty list.
        """
        return sorted(self.projects.values(), key=lambda p: p.id)

    def list_tasks(self, project_id: int) -> List[Task]:
        """Return all tasks for a project.
        Raises:
            ProjectNotFoundError: If project doesn't exist.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        return project.tasks

    def edit_task(
            self,
            project_id: int,
            task_id: int,
            title: str | None = None,
            description: str | None = None,
            status: str | None = None,
            deadline: str | None = None,
    ) -> Task:
        """Edit a task's attributes.
        Raises:
            ProjectNotFoundError: If project doesn't exist.
            TaskNotFoundError: If task doesn't exist.
            ValidationError: If validation fails.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")

        if title is not None:
            if not (1 <= len(title) <= MAX_TASK_TITLE_WORDS):
                raise ValidationError(f"Title must be 1–{MAX_TASK_TITLE_WORDS} characters.")
            task.title = title

        if description is not None:
            if not (1 <= len(description) <= MAX_TASK_DESCRIPTION_WORDS):
                raise ValidationError(f"Description must be 1–{MAX_TASK_DESCRIPTION_WORDS} characters.")
            task.description = description

        if status is not None:
            if status not in ("todo", "doing", "done"):
                raise ValidationError("Invalid status.")
            task.status = status

        task_deadline: Optional[date] = None
        if deadline:
            try:
                task_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Deadline must be in YYYY-MM-DD format.")
        task.deadline = task_deadline

        return task

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task by ID within a project.
        Raises:
            ProjectNotFoundError: If project doesn't exist.
            TaskNotFoundError: If task doesn't exist.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

        for i, t in enumerate(project.tasks):
            if t.id == task_id:
                project.tasks.pop(i)
                return
        raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")

    def edit_project(self, project_id: int, new_name: str, new_description: str) -> Project:
        """Edit a project's name and description.
        Raises:
            ProjectNotFoundError: If project doesn't exist.
            ValidationError: If validation fails.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

        if not (1 <= len(new_name) <= MAX_PROJECT_NAME_WORDS):
            raise ValidationError(f"Project name must be 1–{MAX_PROJECT_NAME_WORDS} characters.")
        if not (1 <= len(new_description) <= MAX_PROJECT_DESCRIPTION_WORDS):
            raise ValidationError(f"Project description must be 1–{MAX_PROJECT_DESCRIPTION_WORDS} characters.")

        # Ensure uniqueness of the new name
        if any(p.name == new_name and p.id != project_id for p in self.projects.values()):
            raise ValidationError("Project name must be unique.")

        project.name = new_name
        project.description = new_description
        return project

    def delete_project(self, project_id: int) -> None:
        """Delete a project and all its tasks.
        Raises:
            ProjectNotFoundError: If project doesn't exist.
        """
        if project_id not in self.projects:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        del self.projects[project_id]
