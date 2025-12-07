"""Pydantic schemas for API request/response validation."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict

from src.config.settings import (
    MAX_PROJECT_NAME_CHARS,
    MAX_PROJECT_DESCRIPTION_CHARS,
    MAX_TASK_TITLE_CHARS,
    MAX_TASK_DESCRIPTION_CHARS,
)


StatusType = Literal["todo", "doing", "done"]


class ProjectCreate(BaseModel):
    """Schema for creating a project."""

    name: str = Field(..., min_length=1, max_length=MAX_PROJECT_NAME_CHARS)
    description: str = Field(..., min_length=1, max_length=MAX_PROJECT_DESCRIPTION_CHARS)


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: str = Field(..., min_length=1, max_length=MAX_PROJECT_NAME_CHARS)
    description: str = Field(..., min_length=1, max_length=MAX_PROJECT_DESCRIPTION_CHARS)


class ProjectResponse(BaseModel):
    """Schema for project response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    created_at: datetime
    task_count: int = 0


class TaskCreate(BaseModel):
    """Schema for creating a task."""

    title: str = Field(..., min_length=1, max_length=MAX_TASK_TITLE_CHARS)
    description: str = Field(..., min_length=1, max_length=MAX_TASK_DESCRIPTION_CHARS)
    status: StatusType = "todo"
    deadline: date | None = None


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: str | None = Field(None, min_length=1, max_length=MAX_TASK_TITLE_CHARS)
    description: str | None = Field(None, min_length=1, max_length=MAX_TASK_DESCRIPTION_CHARS)
    status: StatusType | None = None
    deadline: date | None = None


class TaskStatusUpdate(BaseModel):
    """Schema for updating task status only."""

    status: StatusType


class TaskResponse(BaseModel):
    """Schema for task response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: StatusType
    deadline: date | None
    project_id: int
    created_at: datetime
    closed_at: datetime | None
