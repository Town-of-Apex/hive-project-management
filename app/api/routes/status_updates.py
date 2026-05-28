"""
app/api/routes/status_updates.py

FastAPI router for the /api/status_updates resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.status_update import StatusUpdateCreate, StatusUpdateUpdate, StatusUpdateRead
from app.services.status_update_service import status_update_service

router = APIRouter(prefix="/api/status_updates", tags=["status_updates"])


@router.post("", status_code=201)
def create_status_update(payload: StatusUpdateCreate, db: Session = Depends(get_db)):
    """Create a new status update for a project."""
    update = status_update_service.create(db, obj_in=payload)
    return ok(StatusUpdateRead.model_validate(update).model_dump())


@router.get("")
def list_status_updates(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return a paginated list of status updates, optionally filtered by project."""
    filters = {}
    if project_id is not None:
        filters["project_id"] = project_id
        
    updates = status_update_service.list(db, skip=skip, limit=limit, filters=filters)
    return ok([StatusUpdateRead.model_validate(u).model_dump() for u in updates])


@router.get("/{update_id}")
def get_status_update(update_id: int, db: Session = Depends(get_db)):
    """Fetch a single status update by ID."""
    update = status_update_service.get(db, update_id)
    if not update:
        raise AppException(f"Status update {update_id} not found.", status_code=404)
    return ok(StatusUpdateRead.model_validate(update).model_dump())


@router.put("/{update_id}")
def update_status_update(update_id: int, payload: StatusUpdateUpdate, db: Session = Depends(get_db)):
    """Update an existing status update record."""
    update = status_update_service.get(db, update_id)
    if not update:
        raise AppException(f"Status update {update_id} not found.", status_code=404)
    updated = status_update_service.update(db, db_obj=update, obj_in=payload)
    return ok(StatusUpdateRead.model_validate(updated).model_dump())


@router.delete("/{update_id}")
def delete_status_update(update_id: int, db: Session = Depends(get_db)):
    """Delete a status update record."""
    deleted = status_update_service.delete(db, id=update_id)
    if not deleted:
        raise AppException(f"Status update {update_id} not found.", status_code=404)
    return ok({"deleted": True, "id": update_id})
