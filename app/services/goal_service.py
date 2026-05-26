from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate


# -----------------------------
# CREATE
# -----------------------------
def create_goal(db: Session, goal_data: GoalCreate):

    goal = Goal(
        parent_goal_id=goal_data.parent_goal_id,
        department_id=goal_data.department_id,
        owner_user_id=goal_data.owner_user_id,

        name=goal_data.name,
        description=goal_data.description,

        goal_type=goal_data.goal_type,
        status=goal_data.status,

        start_date=goal_data.start_date,
        due_date=goal_data.due_date,

        source_type=goal_data.source_type,
        source_external_id=goal_data.source_external_id
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal


# -----------------------------
# UPDATE
# -----------------------------

def update_goal(db: Session, goal_id: int, goal_data: GoalUpdate):

    goal = db.query(Goal).filter(Goal.id == goal_id).first()

    if not goal:
        return None

    if goal_data.parent_goal_id is not None:
        goal.parent_goal_id = goal_data.parent_goal_id

    if goal_data.department_id is not None:
        goal.department_id = goal_data.department_id

    if goal_data.owner_user_id is not None:
        goal.owner_user_id = goal_data.owner_user_id

    if goal_data.name is not None:
        goal.name = goal_data.name.strip()

    if goal_data.description is not None:
        goal.description = goal_data.description

    if goal_data.goal_type is not None:
        goal.goal_type = goal_data.goal_type

    if goal_data.status is not None:
        goal.status = goal_data.status

    if goal_data.start_date is not None:
        goal.start_date = goal_data.start_date

    if goal_data.due_date is not None:
        goal.due_date = goal_data.due_date

    db.commit()
    db.refresh(goal)

    return goal

# -----------------------------
# GET
# -----------------------------

def get_goal(db: Session, goal_id: int):

    return db.query(Goal).filter(Goal.id == goal_id).first()


# -----------------------------
# LIST
# -----------------------------

def get_goals(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Goal).offset(skip).limit(limit).all()

# -----------------------------
# DELETE
# -----------------------------

def delete_goal(db: Session, goal_id: int):

    goal = db.query(Goal).filter(Goal.id == goal_id).first()

    if not goal:
        return None

    db.delete(goal)
    db.commit()

    return goal