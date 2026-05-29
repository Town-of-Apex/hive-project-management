"""
app/api/routes/tasks.py

FastAPI router for the /api/tasks resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.core.responses import ok
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services.task_service import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", status_code=201)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new task."""
    task = task_service.create_for_user(db, user=current_user, obj_in=payload)
    return ok(TaskRead.model_validate(task).model_dump())


@router.get("")
def list_tasks(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    assignee_user_id: Optional[int] = Query(None, description="Filter by assignee user ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Free-text search across title and description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a filtered, paginated list of tasks visible to the current user."""
    filters = {}
    if project_id is not None:
        filters["project_id"] = project_id
    if assignee_user_id is not None:
        filters["assignee_user_id"] = assignee_user_id
    if status is not None:
        filters["status"] = status

    tasks = task_service.list_for_user(
        db,
        current_user,
        skip=skip,
        limit=limit,
        filters=filters,
        search_query=search,
        search_fields=["title", "description"],
    )
    return ok([TaskRead.model_validate(t).model_dump() for t in tasks])


@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch a single task by ID."""
    task = task_service.get_task_for_user(db, task_id=task_id, user=current_user)
    return ok(TaskRead.model_validate(task).model_dump())


@router.put("/{task_id}")
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update one or more fields on an existing task."""
    task = task_service.get_task_for_user(
        db, task_id=task_id, user=current_user, require_edit=True
    )
    updated = task_service.update_for_user(db, user=current_user, db_obj=task, obj_in=payload)
    return ok(TaskRead.model_validate(updated).model_dump())


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Permanently delete a task."""
    deleted = task_service.delete_for_user(db, user=current_user, task_id=task_id)
    if not deleted:
        from app.core.exceptions import AppException

        raise AppException(f"Task {task_id} not found.", status_code=404)
    return ok({"deleted": True, "id": task_id})
