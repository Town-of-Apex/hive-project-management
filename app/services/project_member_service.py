"""
app/services/project_member_service.py

Business logic layer for project members.
"""
from app.models.project_member import ProjectMember
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberUpdate
from .base_service import BaseService


class ProjectMemberService(BaseService[ProjectMember, ProjectMemberCreate, ProjectMemberUpdate]):
    """
    ProjectMember service.
    Inherits generic CRUD capabilities from BaseService.
    """
    pass


project_member_service = ProjectMemberService(ProjectMember)
