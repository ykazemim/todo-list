from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from src.models.task import Task

@dataclass
class Project:
    """
    Represents a Project containing multiple tasks.
    """
    id: int
    name: str
    description: str
    tasks: List[Task] = field(default_factory=list)
