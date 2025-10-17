# src/exceptions/todo_exceptions.py
class TodoError(Exception):
    """Base exception for all ToDo application domain errors."""
    pass

class ValidationError(TodoError, ValueError):
    """Raised for general data format or content validation failures."""
    pass

class ProjectNotFoundError(TodoError, LookupError):
    """Raised when a specified project ID does not exist."""
    pass

class TaskNotFoundError(TodoError, LookupError):
    """Raised when a specified task ID does not exist within a project."""
    pass

class LimitExceededError(TodoError, RuntimeError):
    """Raised when a maximum system limit (e.g., max projects/tasks) is reached."""
    pass