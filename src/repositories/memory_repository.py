from typing import Dict, List, Optional
from src.models.project import Project
from src.models.task import Task
from src.exceptions.todo_exceptions import ValidationError
import os

MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 20))

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
