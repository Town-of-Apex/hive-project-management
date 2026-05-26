"""
app/api/routes/departments.py

FastAPI router for the /api/departments resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentRead
from app.services.department_service import department_service

router = APIRouter(prefix="/api/departments", tags=["departments"])


@router.post("", status_code=201)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new department."""
    department = department_service.create(db, obj_in=payload)
    return ok(DepartmentRead.model_validate(department).model_dump())


@router.get("")
def list_departments(
    search: Optional[str] = Query(None, description="Free-text search across name and description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return a filtered, paginated list of departments."""
    departments = department_service.list(
        db, 
        skip=skip, 
        limit=limit, 
        search_query=search, 
        search_fields=["name", "description"]
    )
    return ok([DepartmentRead.model_validate(d).model_dump() for d in departments])


@router.get("/{department_id}")
def get_department(department_id: int, db: Session = Depends(get_db)):
    """Fetch a single department by ID."""
    department = department_service.get(db, department_id)
    if not department:
        raise AppException(f"Department {department_id} not found.", status_code=404)
    return ok(DepartmentRead.model_validate(department).model_dump())


@router.put("/{department_id}")
def update_department(department_id: int, payload: DepartmentUpdate, db: Session = Depends(get_db)):
    """Update an existing department."""
    department = department_service.get(db, department_id)
    if not department:
        raise AppException(f"Department {department_id} not found.", status_code=404)
    updated = department_service.update(db, db_obj=department, obj_in=payload)
    return ok(DepartmentRead.model_validate(updated).model_dump())


@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    """Delete a department by ID."""
    deleted = department_service.delete(db, id=department_id)
    if not deleted:
        raise AppException(f"Department {department_id} not found.", status_code=404)
    return ok({"deleted": True, "id": department_id})
