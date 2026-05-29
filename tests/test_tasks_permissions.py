"""
tests/test_tasks_permissions.py

Integration tests for task authorization and validation.
"""
from tests.conftest import auth_header


def test_list_tasks_requires_auth(client):
    test_client, seeded = client
    response = test_client.get("/api/tasks", params={"project_id": seeded["project"].id})
    assert response.status_code == 401


def test_outsider_cannot_list_private_project_tasks(client):
    test_client, seeded = client
    response = test_client.get(
        "/api/tasks",
        params={"project_id": seeded["project"].id},
        headers={"Authorization": f"Bearer invalid"},
    )
    assert response.status_code == 401

    response = test_client.get(
        "/api/tasks",
        params={"project_id": seeded["project"].id},
        headers=auth_header(seeded["outsider"]),
    )
    assert response.status_code == 403


def test_viewer_can_list_and_get_task(client):
    test_client, seeded = client

    list_response = test_client.get(
        "/api/tasks",
        params={"project_id": seeded["project"].id},
        headers=auth_header(seeded["viewer"]),
    )
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]) == 1

    get_response = test_client.get(
        f"/api/tasks/{seeded['task'].id}",
        headers=auth_header(seeded["viewer"]),
    )
    assert get_response.status_code == 200
    assert get_response.json()["data"]["title"] == "Visible task"


def test_viewer_cannot_update_or_delete_task(client):
    test_client, seeded = client

    update_response = test_client.put(
        f"/api/tasks/{seeded['task'].id}",
        json={"title": "Changed"},
        headers=auth_header(seeded["viewer"]),
    )
    assert update_response.status_code == 403

    delete_response = test_client.delete(
        f"/api/tasks/{seeded['task'].id}",
        headers=auth_header(seeded["viewer"]),
    )
    assert delete_response.status_code == 403


def test_editor_can_create_update_delete_task(client):
    test_client, seeded = client

    create_response = test_client.post(
        "/api/tasks",
        json={
            "project_id": seeded["project"].id,
            "title": "New task",
            "status": "todo",
        },
        headers=auth_header(seeded["editor"]),
    )
    assert create_response.status_code == 201
    created = create_response.json()["data"]
    assert created["created_by_user_id"] == seeded["editor"].id

    update_response = test_client.put(
        f"/api/tasks/{created['id']}",
        json={"title": "Updated task", "status": "done"},
        headers=auth_header(seeded["editor"]),
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["title"] == "Updated task"
    assert update_response.json()["data"]["completed_at"] is not None

    delete_response = test_client.delete(
        f"/api/tasks/{created['id']}",
        headers=auth_header(seeded["editor"]),
    )
    assert delete_response.status_code == 200


def test_create_subtask_requires_same_project_parent(client):
    test_client, seeded = client

    response = test_client.post(
        "/api/tasks",
        json={
            "project_id": seeded["project"].id,
            "parent_task_id": seeded["task"].id,
            "title": "Subtask",
        },
        headers=auth_header(seeded["editor"]),
    )
    assert response.status_code == 201
    assert response.json()["data"]["parent_task_id"] == seeded["task"].id


def test_assignee_must_be_project_member(client):
    test_client, seeded = client

    response = test_client.post(
        "/api/tasks",
        json={
            "project_id": seeded["project"].id,
            "title": "Bad assignee",
            "assignee_user_id": seeded["outsider"].id,
        },
        headers=auth_header(seeded["editor"]),
    )
    assert response.status_code == 400
