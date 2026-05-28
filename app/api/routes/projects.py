"""
app/api/routes/projects.py

FastAPI router for the /api/projects resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.responses import ok
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead, ProjectReadWithPermissions
from app.schemas.project_visibility_grant import (
    ProjectVisibilityGrantCreate,
    ProjectVisibilityGrantRead,
)
from app.services.project_service import project_service
from app.services.project_visibility import (
    can_edit_project,
    require_project_edit,
    require_project_view,
)
from app.services.project_visibility_grant_service import project_visibility_grant_service

router = APIRouter(prefix="/api/projects", tags=["projects"])


def _project_with_permissions(db: Session, current_user: User, project) -> dict:
    base = ProjectRead.model_validate(project).model_dump()
    base["can_edit"] = can_edit_project(db, current_user, project)
    return ProjectReadWithPermissions.model_validate(base).model_dump()


@router.post("", status_code=201)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new project."""
    create_data = payload.model_dump(mode="json")
    if create_data.get("owner_user_id") is None:
        create_data["owner_user_id"] = current_user.id
    project = project_service.create(db, obj_in=ProjectCreate(**create_data))
    return ok(ProjectRead.model_validate(project).model_dump())


@router.get("")
def list_projects(
    search: Optional[str] = Query(None, description="Free-text search across name and description"),
    status: Optional[str] = Query(None, description="Filter by status"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a filtered, paginated list of projects visible to the current user."""
    filters = {}
    if status is not None:
        filters["status"] = status
    if department_id is not None:
        filters["department_id"] = department_id

    projects = project_service.list_visible(
        db,
        current_user,
        skip=skip,
        limit=limit,
        filters=filters,
        search_query=search,
        search_fields=["name", "description"],
    )
    return ok([ProjectRead.model_validate(p).model_dump() for p in projects])


@router.get("/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch a single project by ID."""
    project = project_service.get(db, project_id)
    if not project:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    require_project_view(db, current_user, project)
    return ok(_project_with_permissions(db, current_user, project))


@router.put("/{project_id}")
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update one or more fields on an existing project."""
    project = project_service.get(db, project_id)
    if not project:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    require_project_edit(db, current_user, project)
    updated = project_service.update(
        db,
        db_obj=project,
        obj_in=payload.model_dump(exclude_unset=True, mode="json"),
    )
    return ok(_project_with_permissions(db, current_user, updated))


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Permanently delete a project."""
    project = project_service.get(db, project_id)
    if not project:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    require_project_edit(db, current_user, project)
    deleted = project_service.delete(db, id=project_id)
    if not deleted:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    return ok({"deleted": True, "id": project_id})


@router.get("/{project_id}/visibility-grants")
def list_visibility_grants(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List whitelist users granted explicit access to a project."""
    project = project_service.get(db, project_id)
    if not project:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    require_project_view(db, current_user, project)
    grants = project_visibility_grant_service.list(
        db,
        filters={"project_id": project_id},
        limit=500,
    )
    return ok([ProjectVisibilityGrantRead.model_validate(g).model_dump() for g in grants])


@router.post("/{project_id}/visibility-grants", status_code=201)
def add_visibility_grant(
    project_id: int,
    payload: ProjectVisibilityGrantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Grant a user whitelist access to view a private or restricted project."""
    project = project_service.get(db, project_id)
    if not project:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    require_project_edit(db, current_user, project)
    grant = project_visibility_grant_service.create(
        db,
        obj_in=ProjectVisibilityGrantCreate(user_id=payload.user_id),
        extra_data={"project_id": project_id},
    )
    return ok(ProjectVisibilityGrantRead.model_validate(grant).model_dump())


@router.delete("/{project_id}/visibility-grants/{grant_id}")
def remove_visibility_grant(
    project_id: int,
    grant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a whitelist visibility grant."""
    project = project_service.get(db, project_id)
    if not project:
        raise AppException(f"Project {project_id} not found.", status_code=404)
    require_project_edit(db, current_user, project)
    grant = project_visibility_grant_service.get(db, grant_id)
    if not grant or grant.project_id != project_id:
        raise AppException(f"Visibility grant {grant_id} not found.", status_code=404)
    project_visibility_grant_service.delete(db, id=grant_id)
    return ok({"deleted": True, "id": grant_id})
