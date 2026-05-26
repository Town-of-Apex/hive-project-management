"""
app/api/routes/tasks.py

FastAPI router for the /api/tasks resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services.task_service import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    task = task_service.create(db, obj_in=payload)
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
):
    """Return a filtered, paginated list of tasks."""
    filters = {}
    if project_id is not None:
        filters["project_id"] = project_id
    if assignee_user_id is not None:
        filters["assignee_user_id"] = assignee_user_id
    if status is not None:
        filters["status"] = status
        
    tasks = task_service.list(
        db, 
        skip=skip, 
        limit=limit, 
        filters=filters,
        search_query=search,
        search_fields=["title", "description"]
    )
    return ok([TaskRead.model_validate(t).model_dump() for t in tasks])


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Fetch a single task by ID."""
    task = task_service.get(db, task_id)
    if not task:
        raise AppException(f"Task {task_id} not found.", status_code=404)
    return ok(TaskRead.model_validate(task).model_dump())


@router.put("/{task_id}")
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    """Update one or more fields on an existing task."""
    task = task_service.get(db, task_id)
    if not task:
        raise AppException(f"Task {task_id} not found.", status_code=404)
    updated = task_service.update(db, db_obj=task, obj_in=payload)
    return ok(TaskRead.model_validate(updated).model_dump())


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Permanently delete a task."""
    deleted = task_service.delete(db, id=task_id)
    if not deleted:
        raise AppException(f"Task {task_id} not found.", status_code=404)
    return ok({"deleted": True, "id": task_id})