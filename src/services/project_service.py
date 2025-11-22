"""Service layer for Project business logic."""

from typing import List
from src.models.project import Project
from src.repositories.project_repository import ProjectRepository


class ProjectService:
    """Service for Project operations."""

    def __init__(self, project_repository: ProjectRepository) -> None:
        """Initialize service with project repository.

        :param project_repository: Project repository instance
        """
        self.project_repository = project_repository

    def create_project(self, name: str, description: str) -> Project:
        """Create a new project.

        :param name: Project name
        :param description: Project description
        :return: Created project
        """
        return self.project_repository.add(name, description)

    def list_projects(self) -> List[Project]:
        """List all projects.

        :return: List of all projects
        """
        return self.project_repository.list_all()

    def get_project(self, project_id: int) -> Project:
        """Get a project by ID.

        :param project_id: Project ID
        :return: Project if found
        """
        return self.project_repository.get_by_id(project_id)

    def update_project(
        self, project_id: int, name: str, description: str
    ) -> Project:
        """Update a project.

        :param project_id: Project ID
        :param name: New project name
        :param description: New project description
        :return: Updated project
        """
        return self.project_repository.update(project_id, name, description)

    def delete_project(self, project_id: int) -> None:
        """Delete a project and all its tasks.

        :param project_id: Project ID
        """
        self.project_repository.delete(project_id)
