from sqlalchemy.orm import Session
from datetime import datetime

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate




# -----------------------------
# CREATE
# -----------------------------
def create_task(db: Session, task_data: TaskCreate):

    task = Task(
        project_id=task_data.project_id,
        parent_task_id=task_data.parent_task_id,
        assignee_user_id=task_data.assignee_user_id,
        created_by_user_id=task_data.created_by_user_id,
        
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        start_date=task_data.start_date,
        due_date=task_data.due_date,
        completed_at=task_data.completed_at,
        source_type=task_data.source_type,
        source_external_id=task_data.source_external_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# -----------------------------
# UPDATE
# -----------------------------

def update_task(db: Session, task_id: int, task_data: TaskUpdate):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    if task_data.project_id is not None:
        task.project_id = task_data.project_id

    if task_data.parent_task_id is not None:
        task.parent_task_id = task_data.parent_task_id

    if task_data.assignee_user_id is not None:
        task.assignee_user_id = task_data.assignee_user_id
    
    if task_data.created_by_user_id is not None:
        task.created_by_user_id = task_data.created_by_user_id

    if task_data.title is not None:
        task.title = task_data.title.strip()

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.status is not None:
        task.status = task_data.status

    if task_data.priority is not None:
        task.priority = task_data.priority

    if task_data.start_date is not None:
        task.start_date = task_data.start_date

    if task_data.due_date is not None:
        task.due_date = task_data.due_date

    if task_data.completed_at is not None:
        task.completed_at = task_data.completed_at



    db.commit()
    db.refresh(task)

    return task

# -----------------------------
# GET
# -----------------------------

def get_goal(db: Session, task_id: int):

    return db.query(Task).filter(Task.id == task_id).first()


# -----------------------------
# LIST
# -----------------------------

def get_goals(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Task).offset(skip).limit(limit).all()

# -----------------------------
# DELETE
# -----------------------------

def delete_goal(db: Session, task_id: int):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    db.delete(task)
    db.commit()

    return task