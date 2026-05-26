from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate


# -----------------------------
# CREATE
# -----------------------------

def create_department(db: Session, data: DepartmentCreate):

    department = Department(

        owner_user_id=data.owner_user_id,

        name=data.name,

        description=data.description

    )

    db.add(department)

    db.commit()

    db.refresh(department)

    return department

# -----------------------------
# UPDATE
# -----------------------------

def update_department(db: Session, department_id: int, data: DepartmentUpdate):

    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        return None

    if data.owner_user_id is not None:
        department.owner_user_id = data.owner_user_id

    if data.name is not None:
        department.name = data.name.strip()

    if data.description is not None:
        department.description = data.description

    db.commit()
    db.refresh(department)

    return department
    return team

# -----------------------------
# GET SINGLE
# -----------------------------

def get_department(db: Session, department_id: int):

    return db.query(Department).filter(Department.id == department_id).first()

# -----------------------------
# LIST
# -----------------------------

def get_departments(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Department).offset(skip).limit(limit).all()

# -----------------------------
# DELETE
# -----------------------------

def delete_department(db: Session, department_id: int):

    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        return None

    db.delete(department)
    db.commit()

    return department