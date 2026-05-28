"""
app/services/project_visibility_grant_service.py
"""
from app.models.project_visibility_grant import ProjectVisibilityGrant
from app.schemas.project_visibility_grant import ProjectVisibilityGrantCreate
from .base_service import BaseService


class ProjectVisibilityGrantService(
    BaseService[ProjectVisibilityGrant, ProjectVisibilityGrantCreate, dict]
):
    pass


project_visibility_grant_service = ProjectVisibilityGrantService(ProjectVisibilityGrant)
