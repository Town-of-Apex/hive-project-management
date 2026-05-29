"""
tests/conftest.py

Pytest fixtures for API integration tests using the configured PostgreSQL database.
Each test runs inside a transaction that rolls back after completion.
"""
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.auth import create_access_token
from app.core.config import settings
from app.core.database import get_db
from app.core.security import hash_password
from app.main import app
from app.models.department import Department
from app.models.enums import ProjectMemberRole, ProjectVisibility, UserRole
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task
from app.models.user import User

engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):  # noqa: ARG001
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def seeded(db_session):
    suffix = uuid.uuid4().hex[:8]
    dept = Department(name=f"IT Test {suffix}", description="Information Technology")
    db_session.add(dept)
    db_session.flush()

    owner = User(
        username=f"owner_{suffix}",
        email=f"owner_{suffix}@example.com",
        full_name="Project Owner",
        hashed_password=hash_password("password"),
        role=UserRole.user.value,
        department_id=dept.id,
        is_active=True,
    )
    editor = User(
        username=f"editor_{suffix}",
        email=f"editor_{suffix}@example.com",
        full_name="Project Editor",
        hashed_password=hash_password("password"),
        role=UserRole.user.value,
        department_id=dept.id,
        is_active=True,
    )
    viewer = User(
        username=f"viewer_{suffix}",
        email=f"viewer_{suffix}@example.com",
        full_name="Project Viewer",
        hashed_password=hash_password("password"),
        role=UserRole.user.value,
        department_id=dept.id,
        is_active=True,
    )
    outsider = User(
        username=f"outsider_{suffix}",
        email=f"outsider_{suffix}@example.com",
        full_name="Outside User",
        hashed_password=hash_password("password"),
        role=UserRole.user.value,
        department_id=dept.id,
        is_active=True,
    )
    db_session.add_all([owner, editor, viewer, outsider])
    db_session.flush()

    project = Project(
        department_id=dept.id,
        owner_user_id=owner.id,
        name=f"Test Project {suffix}",
        description="Private project for task permission tests",
        status="active",
        priority="medium",
        visibility=ProjectVisibility.private.value,
    )
    db_session.add(project)
    db_session.flush()

    db_session.add_all(
        [
            ProjectMember(
                project_id=project.id,
                user_id=editor.id,
                role=ProjectMemberRole.member.value,
            ),
            ProjectMember(
                project_id=project.id,
                user_id=viewer.id,
                role=ProjectMemberRole.viewer.value,
            ),
        ]
    )

    task = Task(
        project_id=project.id,
        created_by_user_id=owner.id,
        title="Visible task",
        status="todo",
        priority="medium",
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    return {
        "owner": owner,
        "editor": editor,
        "viewer": viewer,
        "outsider": outsider,
        "project": project,
        "task": task,
    }


def auth_header(user: User) -> dict[str, str]:
    token = create_access_token(user_id=user.id, username=user.username, role=user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def client(db_session, seeded, monkeypatch):
    monkeypatch.setattr("app.main.init_db", lambda: None)

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client, seeded
    app.dependency_overrides.clear()
