"""Domain models for the application."""

from src.models.project import Project
from src.models.task import Task, StatusType

__all__ = ["Project", "Task", "StatusType"]
