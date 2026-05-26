"""
app/services/department_service.py

Business logic layer for departments.
"""
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from .base_service import BaseService


class DepartmentService(BaseService[Department, DepartmentCreate, DepartmentUpdate]):
    """
    Department service.
    Inherits generic CRUD capabilities from BaseService.
    """
    pass


department_service = DepartmentService(Department)