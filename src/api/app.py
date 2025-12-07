"""FastAPI application entry point."""

from fastapi import FastAPI

from src.api.v1.router import router as v1_router

app = FastAPI(
    title="ToDo List API",
    description="A RESTful API for managing projects and tasks",
    version="1.0.0",
)

app.include_router(v1_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
