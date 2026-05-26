"""
app/api/routes/comments.py

FastAPI router for the /api/comments resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.comment import CommentCreate, CommentUpdate, CommentRead
from app.services.comment_service import comment_service

router = APIRouter(prefix="/api/comments", tags=["comments"])


@router.post("", status_code=201)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    """Create a new comment."""
    comment = comment_service.create(db, obj_in=payload)
    return ok(CommentRead.model_validate(comment).model_dump())


@router.get("")
def list_comments(
    task_id: Optional[int] = Query(None, description="Filter by task ID"),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return a paginated list of comments, optionally filtered."""
    filters = {}
    if task_id is not None:
        filters["task_id"] = task_id
    if project_id is not None:
        filters["project_id"] = project_id
        
    comments = comment_service.list(db, skip=skip, limit=limit, filters=filters)
    return ok([CommentRead.model_validate(c).model_dump() for c in comments])


@router.get("/{comment_id}")
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Fetch a single comment by ID."""
    comment = comment_service.get(db, comment_id)
    if not comment:
        raise AppException(f"Comment {comment_id} not found.", status_code=404)
    return ok(CommentRead.model_validate(comment).model_dump())


@router.put("/{comment_id}")
def update_comment(comment_id: int, payload: CommentUpdate, db: Session = Depends(get_db)):
    """Update an existing comment."""
    comment = comment_service.get(db, comment_id)
    if not comment:
        raise AppException(f"Comment {comment_id} not found.", status_code=404)
    updated = comment_service.update(db, db_obj=comment, obj_in=payload)
    return ok(CommentRead.model_validate(updated).model_dump())


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Delete a comment by ID."""
    deleted = comment_service.delete(db, id=comment_id)
    if not deleted:
        raise AppException(f"Comment {comment_id} not found.", status_code=404)
    return ok({"deleted": True, "id": comment_id})
