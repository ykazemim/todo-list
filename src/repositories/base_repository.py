"""Base repository interface using Protocol."""

from typing import Protocol, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")


class BaseRepository(Protocol[T]):
    """Protocol defining the interface for repository implementations.

    This allows for interchangeable repository implementations
    (InMemory, SQLAlchemy, etc.) while maintaining type safety.
    """

    pass
