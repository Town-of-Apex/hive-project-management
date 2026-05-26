from sqlalchemy.orm import Session
from datetime import datetime

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate




# -----------------------------
# CREATE
# -----------------------------
def create_project(db: Session, project_data: ProjectCreate):

    project = Project(
        name=project_data.name,
        description=project_data.description,
        department_id=project_data.department_id,
        status=project_data.status,
        priority=project_data.priority,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


# -----------------------------
# UPDATE
# -----------------------------

def update_project(db: Session, project_id: int, project_data: ProjectUpdate):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return None

    if project_data.parent_goal_id is not None:
        project.parent_goal_id = project_data.parent_goal_id

    if project_data.department_id is not None:
        project.department_id = project_data.department_id

    if project_data.owner_user_id is not None:
        project.owner_user_id = project_data.owner_user_id

    if project_data.name is not None:
        project.name = project_data.name.strip()

    if project_data.description is not None:
        project.description = project_data.description

    if project_data.status is not None:
        project.status = project_data.status
        
    if project.priority is not None:
        project.priority = project_data.priority

    db.commit()
    db.refresh(project)

    return project

# -----------------------------
# GET
# -----------------------------

def get_project(db: Session, project_id: int):

    return db.query(Project).filter(Project.id == project_id).first()


# -----------------------------
# LIST
# -----------------------------

def get_projects(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Project).offset(skip).limit(limit).all()

# -----------------------------
# DELETE
# -----------------------------

def delete_project(db: Session, project_id: int):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return None

    db.delete(project)
    db.commit()

    return project