"""Tests for project endpoints."""

import pytest


class TestCreateProject:
    """Tests for POST /api/v1/projects."""

    def test_create_project_success(self, client):
        response = client.post("/api/v1/projects", json={
            "name": "Test Project",
            "description": "Test description"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Project"
        assert data["description"] == "Test description"
        assert "id" in data

    def test_create_project_empty_name(self, client):
        response = client.post("/api/v1/projects", json={
            "name": "",
            "description": "Test description"
        })
        assert response.status_code == 422

    def test_create_project_name_too_long(self, client):
        response = client.post("/api/v1/projects", json={
            "name": "x" * 100,
            "description": "Test description"
        })
        assert response.status_code == 422

    def test_create_project_duplicate_name(self, client):
        client.post("/api/v1/projects", json={
            "name": "Unique",
            "description": "First"
        })
        response = client.post("/api/v1/projects", json={
            "name": "Unique",
            "description": "Second"
        })
        assert response.status_code == 400


class TestListProjects:
    """Tests for GET /api/v1/projects."""

    def test_list_projects_empty(self, client):
        response = client.get("/api/v1/projects")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_projects_with_data(self, client):
        client.post("/api/v1/projects", json={
            "name": "Project 1",
            "description": "Desc 1"
        })
        client.post("/api/v1/projects", json={
            "name": "Project 2",
            "description": "Desc 2"
        })
        response = client.get("/api/v1/projects")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGetProject:
    """Tests for GET /api/v1/projects/{id}."""

    def test_get_project_success(self, client):
        create_resp = client.post("/api/v1/projects", json={
            "name": "Test",
            "description": "Desc"
        })
        project_id = create_resp.json()["id"]
        response = client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test"

    def test_get_project_not_found(self, client):
        response = client.get("/api/v1/projects/9999")
        assert response.status_code == 404


class TestUpdateProject:
    """Tests for PUT /api/v1/projects/{id}."""

    def test_update_project_success(self, client):
        create_resp = client.post("/api/v1/projects", json={
            "name": "Original",
            "description": "Original desc"
        })
        project_id = create_resp.json()["id"]
        response = client.put(f"/api/v1/projects/{project_id}", json={
            "name": "Updated",
            "description": "Updated desc"
        })
        assert response.status_code == 200
        assert response.json()["name"] == "Updated"

    def test_update_project_not_found(self, client):
        response = client.put("/api/v1/projects/9999", json={
            "name": "Test",
            "description": "Desc"
        })
        assert response.status_code == 404


class TestDeleteProject:
    """Tests for DELETE /api/v1/projects/{id}."""

    def test_delete_project_success(self, client):
        create_resp = client.post("/api/v1/projects", json={
            "name": "ToDelete",
            "description": "Desc"
        })
        project_id = create_resp.json()["id"]
        response = client.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == 204

        get_resp = client.get(f"/api/v1/projects/{project_id}")
        assert get_resp.status_code == 404

    def test_delete_project_not_found(self, client):
        response = client.delete("/api/v1/projects/9999")
        assert response.status_code == 404
