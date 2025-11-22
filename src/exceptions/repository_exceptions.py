"""Repository layer exceptions."""

from src.exceptions.base import TodoError


class ProjectNotFoundError(TodoError, LookupError):
    """Raised when a specified project ID does not exist."""

    pass


class TaskNotFoundError(TodoError, LookupError):
    """Raised when a specified task ID does not exist within a project."""

    pass


class LimitExceededError(TodoError, RuntimeError):
    """Raised when a maximum system limit (e.g., max projects/tasks) is reached."""

    pass
