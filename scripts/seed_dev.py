"""
scripts/seed_dev.py

Idempotent development seed data for Hive PM.
Run: python scripts/seed_dev.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.database import SessionLocal, _import_all_models
from app.core.security import hash_password
from app.models.department import Department
from app.models.enums import ProjectMemberRole, UserRole
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task
from app.models.team import Team
from app.models.user import User

SEED_MARKER_USERNAME = "devadmin"
DEV_PASSWORD = "devadmin123"


def seed() -> None:
    _import_all_models()
    db = SessionLocal()
    try:
        if db.query(User).filter(User.username == SEED_MARKER_USERNAME).first():
            print("Seed data already present (devadmin exists). Skipping.")
            return

        dept = Department(
            name="Information Technology",
            description="Town IT department",
        )
        db.add(dept)
        db.flush()

        admin = User(
            username="devadmin",
            email="devadmin@apexnc.org",
            full_name="Dev Administrator",
            hashed_password=hash_password(DEV_PASSWORD),
            role=UserRole.admin.value,
            department_id=dept.id,
            is_active=True,
        )
        jsmith = User(
            username="jsmith",
            email="jsmith@apexnc.org",
            full_name="Jane Smith",
            hashed_password=hash_password("employee123"),
            role=UserRole.user.value,
            department_id=dept.id,
            is_active=True,
        )
        db.add_all([admin, jsmith])
        db.flush()

        dept.owner_user_id = admin.id

        team = Team(
            department_id=dept.id,
            owner_user_id=admin.id,
            name="Application Development",
            description="Internal application development team",
        )
        db.add(team)
        db.flush()

        admin.team_id = team.id
        jsmith.team_id = team.id

        projects_data = [
            {
                "name": "Hive Platform Migration",
                "description": "Migrate legacy HIVE tooling to the Apex template stack.",
                "status": "active",
                "priority": "high",
            },
            {
                "name": "Citizen Portal Refresh",
                "description": "UX improvements and accessibility updates for the public portal.",
                "status": "active",
                "priority": "medium",
            },
            {
                "name": "GIS Data Cleanup",
                "description": "Normalize parcel layers and retire obsolete map services.",
                "status": "on_hold",
                "priority": "low",
                "visibility": "department",
            },
        ]

        projects: list[Project] = []
        for pdata in projects_data:
            visibility = pdata.pop("visibility", "organization")
            project = Project(
                department_id=dept.id,
                owner_user_id=admin.id,
                visibility=visibility,
                **pdata,
            )
            db.add(project)
            projects.append(project)
        db.flush()

        for project in projects:
            db.add(
                ProjectMember(
                    project_id=project.id,
                    user_id=admin.id,
                    role=ProjectMemberRole.manager.value,
                )
            )

        tasks_data = [
            (projects[0].id, "Set up PostgreSQL and Alembic", "todo", "high"),
            (projects[0].id, "Implement auth stub", "in_progress", "high"),
            (projects[0].id, "Build projects UI", "in_progress", "medium"),
            (projects[1].id, "Audit color contrast", "todo", "medium"),
            (projects[1].id, "Prototype new home page", "done", "low"),
            (projects[2].id, "Inventory legacy map layers", "todo", "medium"),
        ]
        for project_id, title, status, priority in tasks_data:
            db.add(
                Task(
                    project_id=project_id,
                    title=title,
                    status=status,
                    priority=priority,
                    created_by_user_id=admin.id,
                    assignee_user_id=admin.id,
                )
            )

        db.commit()
        print("Seed data created successfully.")
        print(f"  Login: {SEED_MARKER_USERNAME} / {DEV_PASSWORD}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
