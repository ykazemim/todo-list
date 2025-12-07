"""Task model definition."""

from __future__ import annotations
from datetime import date, datetime, timezone
from typing import Literal, Optional
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base

StatusType = Literal["todo", "doing", "done"]


class Task(Base):
    """ORM model representing a Task inside a Project.

    :param id: Unique identifier for the task
    :param title: Task title
    :param description: Task description
    :param status: Task status (todo, doing, done)
    :param deadline: Optional deadline date
    :param project_id: Foreign key to the parent project
    :param created_at: Timestamp when task was created
    :param closed_at: Timestamp when task was closed (if done)
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[StatusType] = mapped_column(
        String(10),
        nullable=False,
        default="todo",
        server_default="todo",
    )
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default="CURRENT_TIMESTAMP",
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    __table_args__ = (
        CheckConstraint(
            "status IN ('todo', 'doing', 'done')",
            name="check_task_status",
        ),
    )

    def __repr__(self) -> str:
        """Return string representation of the task."""
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
