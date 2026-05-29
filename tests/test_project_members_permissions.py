"""
tests/test_project_members_permissions.py

Integration tests for project member authorization.
"""
from tests.conftest import auth_header


def test_list_members_requires_auth(client):
    test_client, seeded = client
    response = test_client.get(
        "/api/project_members",
        params={"project_id": seeded["project"].id},
    )
    assert response.status_code == 401


def test_outsider_cannot_list_private_project_members(client):
    test_client, seeded = client
    response = test_client.get(
        "/api/project_members",
        params={"project_id": seeded["project"].id},
        headers=auth_header(seeded["outsider"]),
    )
    assert response.status_code == 403


def test_viewer_can_list_members(client):
    test_client, seeded = client
    response = test_client.get(
        "/api/project_members",
        params={"project_id": seeded["project"].id},
        headers=auth_header(seeded["viewer"]),
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 1


def test_list_members_requires_project_id(client):
    test_client, seeded = client
    response = test_client.get(
        "/api/project_members",
        headers=auth_header(seeded["editor"]),
    )
    assert response.status_code == 400


def test_outsider_cannot_get_task(client):
    test_client, seeded = client
    response = test_client.get(
        f"/api/tasks/{seeded['task'].id}",
        headers=auth_header(seeded["outsider"]),
    )
    assert response.status_code == 403
