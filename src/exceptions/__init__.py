"""Exception classes for the application."""

from src.exceptions.base import TodoError
from src.exceptions.repository_exceptions import (
    ProjectNotFoundError,
    TaskNotFoundError,
    LimitExceededError,
)
from src.exceptions.service_exceptions import ValidationError

__all__ = [
    "TodoError",
    "ValidationError",
    "ProjectNotFoundError",
    "TaskNotFoundError",
    "LimitExceededError",
]
