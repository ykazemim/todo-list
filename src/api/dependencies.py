"""FastAPI dependency injection."""

from typing import Generator

from sqlalchemy.orm import Session

from src.db.session import SessionLocal
from src.repositories.project_repository import ProjectRepository
from src.repositories.task_repository import TaskRepository
from src.services.project_service import ProjectService
from src.services.task_service import TaskService


def get_db() -> Generator[Session, None, None]:
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session) -> ProjectService:
    """Create and return a ProjectService instance."""
    repository = ProjectRepository(db)
    return ProjectService(repository)


def get_task_service(db: Session) -> TaskService:
    """Create and return a TaskService instance."""
    repository = TaskRepository(db)
    return TaskService(repository)
