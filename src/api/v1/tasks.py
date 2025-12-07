"""Task API endpoints."""

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_db, get_task_service
from src.api.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
)
from src.exceptions import (
    ProjectNotFoundError,
    TaskNotFoundError,
    ValidationError,
    LimitExceededError,
)

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Create a new task in a project."""
    service = get_task_service(db)
    try:
        deadline_str = data.deadline.isoformat() if data.deadline else None
        task = service.create_task(
            project_id,
            data.title,
            data.description,
            data.status,
            deadline_str,
        )
        return TaskResponse.model_validate(task)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except LimitExceededError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
) -> Sequence[TaskResponse]:
    """List all tasks for a project."""
    service = get_task_service(db)
    try:
        tasks = service.list_tasks(project_id)
        return [TaskResponse.model_validate(t) for t in tasks]
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Get a task by ID."""
    service = get_task_service(db)
    try:
        task = service.get_task(project_id, task_id)
        return TaskResponse.model_validate(task)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: int,
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Update a task."""
    service = get_task_service(db)
    try:
        deadline_str = data.deadline.isoformat() if data.deadline else None
        task = service.update_task(
            project_id,
            task_id,
            data.title,
            data.description,
            data.status,
            deadline_str,
        )
        return TaskResponse.model_validate(task)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{task_id}/status", response_model=TaskResponse)
def change_task_status(
    project_id: int,
    task_id: int,
    data: TaskStatusUpdate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Change the status of a task."""
    service = get_task_service(db)
    try:
        task = service.change_task_status(project_id, task_id, data.status)
        return TaskResponse.model_validate(task)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a task."""
    service = get_task_service(db)
    try:
        service.delete_task(project_id, task_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
