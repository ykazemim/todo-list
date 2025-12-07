"""Project model definition."""

from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base

if TYPE_CHECKING:
    from src.models.task import Task


class Project(Base):
    """ORM model representing a Project containing multiple tasks.

    :param id: Unique identifier for the project
    :param name: Project name (must be unique)
    :param description: Project description
    :param created_at: Timestamp when project was created
    :param tasks: List of tasks belonging to this project
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default="CURRENT_TIMESTAMP",
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    __table_args__ = (UniqueConstraint("name", name="uq_project_name"),)

    def __repr__(self) -> str:
        """Return string representation of the project."""
        return f"<Project(id={self.id}, name='{self.name}')>"
