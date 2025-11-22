"""Service layer exceptions."""

from src.exceptions.base import TodoError


class ValidationError(TodoError, ValueError):
    """Raised for general data format or content validation failures."""

    pass
