"""
SmartTrack — Unit Tests
Run with: python -m pytest tests/ -v
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, init_db

DB_PATH = "test_smarttrack.db"


@pytest.fixture
def client(tmp_path):
    """Create a test client with an isolated temp database."""
    app.config["TESTING"] = True
    os.environ["DB_PATH"] = str(tmp_path / "test.db")
    with app.app_context():
        init_db()
    with app.test_client() as client:
        yield client


# ── HEALTH CHECK ──────────────────────────────────────────────────────────────

def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"


# ── PROJECT TESTS ─────────────────────────────────────────────────────────────

def test_create_project(client):
    resp = client.post("/api/projects", json={"name": "Test Project", "description": "A test"})
    assert resp.status_code == 201
    assert "id" in resp.get_json()


def test_get_projects(client):
    client.post("/api/projects", json={"name": "Project Alpha"})
    resp = client.get("/api/projects")
    assert resp.status_code == 200
    projects = resp.get_json()
    assert isinstance(projects, list)
    assert len(projects) >= 1


def test_create_project_missing_name(client):
    resp = client.post("/api/projects", json={"description": "No name"})
    assert resp.status_code == 400


def test_delete_project(client):
    create_resp = client.post("/api/projects", json={"name": "Delete Me"})
    project_id = create_resp.get_json()["id"]
    del_resp = client.delete(f"/api/projects/{project_id}")
    assert del_resp.status_code == 200


# ── TASK TESTS ────────────────────────────────────────────────────────────────

def test_create_task(client):
    proj_resp = client.post("/api/projects", json={"name": "Task Project"})
    project_id = proj_resp.get_json()["id"]
    resp = client.post("/api/tasks", json={
        "project_id": project_id,
        "title": "Fix the bug",
        "priority": "High",
        "assignee": "Rajkumar"
    })
    assert resp.status_code == 201


def test_update_task_status(client):
    proj_resp = client.post("/api/projects", json={"name": "Status Project"})
    project_id = proj_resp.get_json()["id"]
    task_resp = client.post("/api/tasks", json={
        "project_id": project_id,
        "title": "A task"
    })
    task_id = task_resp.get_json()["id"]
    update_resp = client.put(f"/api/tasks/{task_id}", json={"status": "In Progress"})
    assert update_resp.status_code == 200


def test_get_tasks_for_project(client):
    proj_resp = client.post("/api/projects", json={"name": "Tasks Project"})
    project_id = proj_resp.get_json()["id"]
    client.post("/api/tasks", json={"project_id": project_id, "title": "Task 1"})
    client.post("/api/tasks", json={"project_id": project_id, "title": "Task 2"})
    resp = client.get(f"/api/projects/{project_id}/tasks")
    assert resp.status_code == 200
    tasks = resp.get_json()
    assert len(tasks) == 2


def test_user_stories_endpoint(client):
    resp = client.get("/api/stories")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "stories" in data
