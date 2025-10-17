from typing import Dict, List, Optional, Literal
from datetime import datetime, date
from src.models.project import Project
from src.models.task import Task
from src.exceptions.todo_exceptions import ValidationError
import os

MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 20))

StatusType = Literal["todo", "doing", "done"]
MAX_TASK_TITLE = 30
MAX_TASK_DESC = 150
VALID_STATUSES: list[StatusType] = ["todo", "doing", "done"]


class InMemoryRepository:
    """
    Stores Projects and Tasks in memory with basic validation.
    """

    def __init__(self) -> None:
        self.projects: Dict[int, Project] = {}
        self.next_project_id: int = 1
        self.next_task_id: int = 1

    # ---------- Project CRUD ----------

    def add_project(self, name: str, description: str) -> Project:
        """
        Create and store a new project with validation.

        Raises:
            ValidationError: If limits are exceeded or name is duplicate.
        """
        if len(self.projects) >= MAX_NUMBER_OF_PROJECT:
            raise ValidationError("Maximum number of projects reached.")

        if any(p.name == name for p in self.projects.values()):
            raise ValidationError(f"Project name '{name}' already exists.")

        if len(name) > 30:
            raise ValidationError("Project name must be ≤ 30 characters.")

        if len(description) > 150:
            raise ValidationError("Project description must be ≤ 150 characters.")

        project = Project(id=self.next_project_id, name=name, description=description)
        self.projects[self.next_project_id] = project
        self.next_project_id += 1
        return project

    def edit_project(self, project_id: int, name: str, description: str) -> Project:
        """
        Update a project's name and description.
        """
        project = self.projects.get(project_id)
        if project is None:
            raise ValidationError("Project not found.")

        if len(name) > 30:
            raise ValidationError("Project name must be ≤ 30 characters.")

        if len(description) > 150:
            raise ValidationError("Project description must be ≤ 150 characters.")

        if any(p.name == name and p.id != project_id for p in self.projects.values()):
            raise ValidationError(f"Project name '{name}' already exists.")

        project.name = name
        project.description = description
        return project

    def delete_project(self, project_id: int) -> None:
        """
        Delete a project and cascade delete its tasks.
        """
        if project_id not in self.projects:
            raise ValidationError("Project not found.")
        del self.projects[project_id]

    def list_projects(self) -> List[Project]:
        """
        Return all projects sorted by creation time (ID).
        """
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
        """
        Add a task to a project.
        """
        project = self.projects.get(project_id)
        if project is None:
            raise ValidationError("Project not found.")

        if len(project.tasks) >= int(os.getenv("MAX_NUMBER_OF_TASK", 200)):
            raise ValidationError("Maximum number of tasks reached for this project.")

        if len(title) > MAX_TASK_TITLE:
            raise ValidationError(f"Task title must be ≤ {MAX_TASK_TITLE} characters.")

        if len(description) > MAX_TASK_DESC:
            raise ValidationError(f"Task description must be ≤ {MAX_TASK_DESC} characters.")

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

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        title: str,
        description: str,
        status: StatusType,
        deadline: Optional[str] = None,
    ) -> Task:
        """
        Edit a task's details.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValidationError("Task not found.")

        if len(title) > MAX_TASK_TITLE:
            raise ValidationError(f"Task title must be ≤ {MAX_TASK_TITLE} characters.")
        if len(description) > MAX_TASK_DESC:
            raise ValidationError(f"Task description must be ≤ {MAX_TASK_DESC} characters.")
        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task_deadline: Optional[date] = None
        if deadline:
            try:
                task_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Deadline must be in YYYY-MM-DD format.")

        task.title = title
        task.description = description
        task.status = status
        task.deadline = task_deadline
        return task

    def delete_task(self, project_id: int, task_id: int) -> None:
        """
        Delete a task by ID within a project.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValidationError("Task not found.")

        project.tasks.remove(task)

    def change_task_status(self, project_id: int, task_id: int, status: StatusType) -> Task:
        """
        Change only the status of a task.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValidationError("Task not found.")

        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task.status = status
        return task

    def list_all_projects(self) -> List[Project]:
        """
        Return all projects sorted by creation time.
        If no projects exist, returns an empty list.
        """
        return sorted(self.projects.values(), key=lambda p: p.id)

    def list_tasks(self, project_id: int) -> List[Task]:
        """
        Return all tasks for a project.
        If the project doesn't exist or has no tasks, returns an empty list.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValidationError("Project not found.")
        return project.tasks
