"""Tests for task endpoints."""

import pytest


@pytest.fixture
def project_id(client):
    """Create a project and return its ID."""
    response = client.post("/api/v1/projects", json={
        "name": "Test Project",
        "description": "For task testing"
    })
    return response.json()["id"]


class TestCreateTask:
    """Tests for POST /api/v1/projects/{id}/tasks."""

    def test_create_task_success(self, client, project_id):
        response = client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Test Task",
            "description": "Task description",
            "status": "todo"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["status"] == "todo"

    def test_create_task_with_deadline(self, client, project_id):
        response = client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Task with deadline",
            "description": "Has deadline",
            "status": "todo",
            "deadline": "2025-12-31"
        })
        assert response.status_code == 201
        assert response.json()["deadline"] == "2025-12-31"

    def test_create_task_project_not_found(self, client):
        response = client.post("/api/v1/projects/9999/tasks", json={
            "title": "Task",
            "description": "Desc",
            "status": "todo"
        })
        assert response.status_code == 404

    def test_create_task_invalid_status(self, client, project_id):
        response = client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Task",
            "description": "Desc",
            "status": "invalid"
        })
        assert response.status_code == 422


class TestListTasks:
    """Tests for GET /api/v1/projects/{id}/tasks."""

    def test_list_tasks_empty(self, client, project_id):
        response = client.get(f"/api/v1/projects/{project_id}/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_with_data(self, client, project_id):
        client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Task 1",
            "description": "Desc 1",
            "status": "todo"
        })
        client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Task 2",
            "description": "Desc 2",
            "status": "doing"
        })
        response = client.get(f"/api/v1/projects/{project_id}/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGetTask:
    """Tests for GET /api/v1/projects/{id}/tasks/{task_id}."""

    def test_get_task_success(self, client, project_id):
        create_resp = client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Test Task",
            "description": "Desc",
            "status": "todo"
        })
        task_id = create_resp.json()["id"]
        response = client.get(f"/api/v1/projects/{project_id}/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"

    def test_get_task_not_found(self, client, project_id):
        response = client.get(f"/api/v1/projects/{project_id}/tasks/9999")
        assert response.status_code == 404


class TestUpdateTask:
    """Tests for PUT /api/v1/projects/{id}/tasks/{task_id}."""

    def test_update_task_success(self, client, project_id):
        create_resp = client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Original",
            "description": "Original desc",
            "status": "todo"
        })
        task_id = create_resp.json()["id"]
        response = client.put(f"/api/v1/projects/{project_id}/tasks/{task_id}", json={
            "title": "Updated",
            "description": "Updated desc"
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"


class TestChangeTaskStatus:
    """Tests for PATCH /api/v1/projects/{id}/tasks/{task_id}/status."""

    def test_change_status_success(self, client, project_id):
        create_resp = client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Task",
            "description": "Desc",
            "status": "todo"
        })
        task_id = create_resp.json()["id"]
        response = client.patch(
            f"/api/v1/projects/{project_id}/tasks/{task_id}/status",
            json={"status": "done"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "done"
        assert response.json()["closed_at"] is not None

    def test_change_status_invalid(self, client, project_id):
        create_resp = client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "Task",
            "description": "Desc",
            "status": "todo"
        })
        task_id = create_resp.json()["id"]
        response = client.patch(
            f"/api/v1/projects/{project_id}/tasks/{task_id}/status",
            json={"status": "invalid"}
        )
        assert response.status_code == 422


class TestDeleteTask:
    """Tests for DELETE /api/v1/projects/{id}/tasks/{task_id}."""

    def test_delete_task_success(self, client, project_id):
        create_resp = client.post(f"/api/v1/projects/{project_id}/tasks", json={
            "title": "ToDelete",
            "description": "Desc",
            "status": "todo"
        })
        task_id = create_resp.json()["id"]
        response = client.delete(f"/api/v1/projects/{project_id}/tasks/{task_id}")
        assert response.status_code == 204

        get_resp = client.get(f"/api/v1/projects/{project_id}/tasks/{task_id}")
        assert get_resp.status_code == 404
