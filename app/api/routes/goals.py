from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.goal import GoalCreate, GoalUpdate
from app.services.goal_service import (
    create_goal,
    get_goal,
    get_goals,
    update_goal,
    delete_goal
)

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.post("/")
def create(data: GoalCreate, db: Session = Depends(get_db)):
    return create_goal(db, data)


@router.get("/{goal_id}")
def read(goal_id: int, db: Session = Depends(get_db)):
    return get_goal(db, goal_id)


@router.get("/")
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_goals(db, skip, limit)


@router.put("/{goal_id}")
def update(goal_id: int, data: GoalUpdate, db: Session = Depends(get_db)):
    return update_goal(db, goal_id, data)


@router.delete("/{goal_id}")
def delete(goal_id: int, db: Session = Depends(get_db)):
    return delete_goal(db, goal_id)