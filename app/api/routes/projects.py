"""
app/api/routes/projects.py

FastAPI router for the /api/projects resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.services.project_service import project_service

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project."""
    project = project_service.create(db, obj_in=payload)
    return ok(ProjectRead.model_validate(project).model_dump())


@router.get("")
def list_projects(
    search: Optional[str] = Query(None, description="Free-text search across name and description"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return a filtered, paginated list of projects."""
    filters = {}
    if status is not None:
        filters["status"] = status
        
    projects = project_service.list(
        db, 
        skip=skip, 
        limit=limit, 
        filters=filters,
        search_query=search, 
        search_fields=["name", "description"]
    )
    return ok([ProjectRead.model_validate(p).model_dump() for p in projects])


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Fetch a single project by ID."""
    project = project_service.get(db, project_id)
    if not project:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    return ok(ProjectRead.model_validate(project).model_dump())


@router.put("/{project_id}")
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    """Update one or more fields on an existing project."""
    project = project_service.get(db, project_id)
    if not project:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    updated = project_service.update(db, db_obj=project, obj_in=payload)
    return ok(ProjectRead.model_validate(updated).model_dump())


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Permanently delete a project."""
    deleted = project_service.delete(db, id=project_id)
    if not deleted:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    return ok({"deleted": True, "id": project_id})