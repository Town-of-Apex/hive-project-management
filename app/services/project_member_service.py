"""
app/services/project_member_service.py

Business logic layer for project members.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberUpdate
from app.services.project_visibility import require_project_edit, require_project_view
from .base_service import BaseService


class ProjectMemberService(BaseService[ProjectMember, ProjectMemberCreate, ProjectMemberUpdate]):
    """Project member service with project-scoped authorization."""

    def get_project(self, db: Session, project_id: int) -> Project:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise AppException(f"Project {project_id} not found.", status_code=404)
        return project

    def get_member_for_user(
        self,
        db: Session,
        *,
        member_id: int,
        user: User,
        require_edit: bool = False,
    ) -> ProjectMember:
        member = self.get(db, member_id)
        if not member:
            raise AppException(f"Project member record {member_id} not found.", status_code=404)

        project = self.get_project(db, member.project_id)
        if require_edit:
            require_project_edit(db, user, project)
        else:
            require_project_view(db, user, project)
        return member

    def list_for_user(
        self,
        db: Session,
        user: User,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None,
    ) -> List[ProjectMember]:
        filters = dict(filters or {})
        project_id = filters.get("project_id")

        if project_id is not None:
            project = self.get_project(db, project_id)
            require_project_view(db, user, project)
            return self.list(db, skip=skip, limit=limit, filters=filters)

        raise AppException(
            "project_id is required to list project members.",
            status_code=400,
        )

    def create_for_user(
        self,
        db: Session,
        *,
        user: User,
        obj_in: ProjectMemberCreate,
    ) -> ProjectMember:
        project = self.get_project(db, obj_in.project_id)
        require_project_edit(db, user, project)
        return self.create(db, obj_in=obj_in)

    def update_for_user(
        self,
        db: Session,
        *,
        user: User,
        db_obj: ProjectMember,
        obj_in: ProjectMemberUpdate,
    ) -> ProjectMember:
        project = self.get_project(db, db_obj.project_id)
        require_project_edit(db, user, project)
        return self.update(db, db_obj=db_obj, obj_in=obj_in)

    def delete_for_user(self, db: Session, *, user: User, member_id: int) -> bool:
        member = self.get_member_for_user(db, member_id=member_id, user=user, require_edit=True)
        return self.delete(db, id=member.id)


project_member_service = ProjectMemberService(ProjectMember)
