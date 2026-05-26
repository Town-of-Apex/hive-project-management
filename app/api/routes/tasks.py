from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import (
    create_task,
    get_task,
    get_tasks,
    update_task,
    delete_task
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create(data: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, data)


@router.get("/{task_id}")
def read(task_id: int, db: Session = Depends(get_db)):
    return get_task(db, task_id)


@router.get("/")
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tasks(db, skip, limit)


@router.put("/{task_id}")
def update(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    return update_task(db, task_id, data)


@router.delete("/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db)):
    return delete_task(db, task_id)