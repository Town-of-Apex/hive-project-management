"""
app/services/project_service.py

Business logic layer for projects, including visibility-aware listing.
"""
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.project_visibility import visible_projects_query
from .base_service import BaseService


class ProjectService(BaseService[Project, ProjectCreate, ProjectUpdate]):
    def list_visible(
        self,
        db: Session,
        user: User,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None,
        search_query: Optional[str] = None,
        search_fields: Optional[List[str]] = None,
    ) -> List[Project]:
        query = visible_projects_query(db, user)

        if filters:
            for field, value in filters.items():
                if hasattr(Project, field):
                    query = query.filter(getattr(Project, field) == value)

        if search_query and search_fields:
            search_filters = []
            term = f"%{search_query}%"
            for field in search_fields:
                if hasattr(Project, field):
                    search_filters.append(getattr(Project, field).ilike(term))
            if search_filters:
                query = query.filter(or_(*search_filters))

        return query.offset(skip).limit(limit).all()


project_service = ProjectService(Project)
