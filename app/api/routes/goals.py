"""
app/api/routes/goals.py

FastAPI router for the /api/goals resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.goal import GoalCreate, GoalUpdate, GoalRead
from app.services.goal_service import goal_service

router = APIRouter(prefix="/api/goals", tags=["goals"])


@router.post("", status_code=201)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db)):
    """Create a new goal."""
    goal = goal_service.create(db, obj_in=payload)
    return ok(GoalRead.model_validate(goal).model_dump())


@router.get("")
def list_goals(
    search: Optional[str] = Query(None, description="Free-text search across name and description"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return a filtered, paginated list of goals."""
    filters = {}
    if status is not None:
        filters["status"] = status
        
    goals = goal_service.list(
        db, 
        skip=skip, 
        limit=limit, 
        filters=filters,
        search_query=search, 
        search_fields=["name", "description"]
    )
    return ok([GoalRead.model_validate(g).model_dump() for g in goals])


@router.get("/{goal_id}")
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    """Fetch a single goal by ID."""
    goal = goal_service.get(db, goal_id)
    if not goal:
        raise AppException(f"Goal {goal_id} not found.", status_code=404)
    return ok(GoalRead.model_validate(goal).model_dump())


@router.put("/{goal_id}")
def update_goal(goal_id: int, payload: GoalUpdate, db: Session = Depends(get_db)):
    """Update an existing goal."""
    goal = goal_service.get(db, goal_id)
    if not goal:
        raise AppException(f"Goal {goal_id} not found.", status_code=404)
    updated = goal_service.update(db, db_obj=goal, obj_in=payload)
    return ok(GoalRead.model_validate(updated).model_dump())


@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    """Delete a goal by ID."""
    deleted = goal_service.delete(db, id=goal_id)
    if not deleted:
        raise AppException(f"Goal {goal_id} not found.", status_code=404)
    return ok({"deleted": True, "id": goal_id})