"""SQLAlchemy repository for Project operations."""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.models.project import Project
from src.exceptions import (
    ProjectNotFoundError,
    LimitExceededError,
    ValidationError,
)
from src.config.settings import (
    MAX_NUMBER_OF_PROJECTS,
    MAX_PROJECT_NAME_CHARS,
    MAX_PROJECT_DESCRIPTION_CHARS,
)


class ProjectRepository:
    """Repository for Project database operations."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        :param session: SQLAlchemy database session
        """
        self.session = session

    def add(self, name: str, description: str) -> Project:
        """Create and store a new project.

        :param name: Project name
        :param description: Project description
        :return: Created project
        :raises ValidationError: If validation fails
        :raises LimitExceededError: If maximum number of projects is reached
        """
        if len(name) <= 0:
            raise ValidationError("Project name cannot be empty.")

        # Check project count
        count = self.session.scalar(select(func.count(Project.id)))
        if count and count >= MAX_NUMBER_OF_PROJECTS:
            raise LimitExceededError("Maximum number of projects reached.")

        # Check for duplicate name
        existing = self.session.scalar(
            select(Project).where(Project.name == name)
        )
        if existing:
            raise ValidationError(f"Project name '{name}' already exists.")

        if len(name) > MAX_PROJECT_NAME_CHARS:
            raise ValidationError(
                f"Project name must be ≤ {MAX_PROJECT_NAME_CHARS} characters."
            )
        if len(description) > MAX_PROJECT_DESCRIPTION_CHARS:
            raise ValidationError(
                f"Project description must be ≤ {MAX_PROJECT_DESCRIPTION_CHARS} characters."
            )

        project = Project(name=name, description=description)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Project:
        """Get a project by ID.

        :param project_id: Project ID
        :return: Project if found
        :raises ProjectNotFoundError: If project doesn't exist
        """
        project = self.session.get(Project, project_id)
        if not project:
            raise ProjectNotFoundError(
                f"Project with ID {project_id} not found."
            )
        return project

    def list_all(self) -> List[Project]:
        """List all projects sorted by ID.

        :return: List of all projects
        """
        stmt = select(Project).order_by(Project.id)
        return list(self.session.scalars(stmt).all())

    def update(self, project_id: int, name: str, description: str) -> Project:
        """Update a project's name and description.

        :param project_id: Project ID
        :param name: New project name
        :param description: New project description
        :return: Updated project
        :raises ProjectNotFoundError: If project doesn't exist
        :raises ValidationError: If validation fails
        """
        project = self.get_by_id(project_id)

        if not (1 <= len(name) <= MAX_PROJECT_NAME_CHARS):
            raise ValidationError(
                f"Project name must be 1–{MAX_PROJECT_NAME_CHARS} characters."
            )
        if not (1 <= len(description) <= MAX_PROJECT_DESCRIPTION_CHARS):
            raise ValidationError(
                f"Project description must be 1–{MAX_PROJECT_DESCRIPTION_CHARS} characters."
            )

        # Check for duplicate name (excluding current project)
        existing = self.session.scalar(
            select(Project).where(
                Project.name == name, Project.id != project_id
            )
        )
        if existing:
            raise ValidationError("Project name must be unique.")

        project.name = name
        project.description = description
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete(self, project_id: int) -> None:
        """Delete a project and all its tasks.

        :param project_id: Project ID
        :raises ProjectNotFoundError: If project doesn't exist
        """
        project = self.get_by_id(project_id)
        self.session.delete(project)
        self.session.commit()
