"""
app/services/project_service.py

Business logic layer for projects.
"""
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from .base_service import BaseService


class ProjectService(BaseService[Project, ProjectCreate, ProjectUpdate]):
    """
    Project service.
    Inherits generic CRUD capabilities from BaseService.
    """
    pass


project_service = ProjectService(Project)