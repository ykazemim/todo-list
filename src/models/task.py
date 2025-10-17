from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Literal, Optional

StatusType = Literal["todo", "doing", "done"]

@dataclass
class Task:
    """
    Represents a Task inside a Project.
    """
    id: int
    title: str
    description: str
    status: StatusType = "todo"
    deadline: Optional[date] = None
