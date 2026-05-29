"""
app/api/routes/project_members.py

FastAPI router for the /api/project_members resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberUpdate, ProjectMemberRead
from app.services.project_member_service import project_member_service

router = APIRouter(prefix="/api/project_members", tags=["project_members"])


@router.post("", status_code=201)
def create_project_member(
    payload: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a member to a project."""
    member = project_member_service.create_for_user(db, user=current_user, obj_in=payload)
    return ok(ProjectMemberRead.model_validate(member).model_dump())


@router.get("")
def list_project_members(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a list of project members for a visible project."""
    filters = {}
    if project_id is not None:
        filters["project_id"] = project_id
    if user_id is not None:
        filters["user_id"] = user_id

    members = project_member_service.list_for_user(
        db,
        current_user,
        skip=skip,
        limit=limit,
        filters=filters,
    )
    return ok([ProjectMemberRead.model_validate(m).model_dump() for m in members])


@router.get("/{member_id}")
def get_project_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch a single project member by ID."""
    member = project_member_service.get_member_for_user(db, member_id=member_id, user=current_user)
    return ok(ProjectMemberRead.model_validate(member).model_dump())


@router.put("/{member_id}")
def update_project_member(
    member_id: int,
    payload: ProjectMemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a project member's role."""
    member = project_member_service.get_member_for_user(
        db, member_id=member_id, user=current_user, require_edit=True
    )
    updated = project_member_service.update_for_user(
        db, user=current_user, db_obj=member, obj_in=payload
    )
    return ok(ProjectMemberRead.model_validate(updated).model_dump())


@router.delete("/{member_id}")
def delete_project_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a member from a project."""
    deleted = project_member_service.delete_for_user(db, user=current_user, member_id=member_id)
    if not deleted:
        raise AppException(f"Project member record {member_id} not found.", status_code=404)
    return ok({"deleted": True, "id": member_id})
