from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import (
    create_project,
    get_project,
    get_projects,
    update_project,
    delete_project
)


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
def create(data: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, data)


@router.get("/{project_id}")
def read(project_id: int, db: Session = Depends(get_db)):
    return get_project(db, project_id)


@router.get("/")
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_projects(db, skip, limit)


@router.put("/{project_id}")
def update(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    return update_project(db, project_id, data)


@router.delete("/{project_id}")
def delete(project_id: int, db: Session = Depends(get_db)):
    return delete_project(db, project_id)