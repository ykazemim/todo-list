"""API v1 router aggregator."""

from fastapi import APIRouter

from src.api.v1.projects import router as projects_router
from src.api.v1.tasks import router as tasks_router

router = APIRouter(prefix="/api/v1")
router.include_router(projects_router)
router.include_router(tasks_router)
