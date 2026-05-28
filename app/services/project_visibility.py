"""
app/services/project_visibility.py

Access rules for projects: visibility modes, membership, whitelist grants, and admin override.
"""
from sqlalchemy import or_, and_, exists
from sqlalchemy.orm import Session, Query

from app.models.enums import ProjectMemberRole, ProjectVisibility, UserRole
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.project_visibility_grant import ProjectVisibilityGrant
from app.models.user import User

_EDIT_ROLES = {ProjectMemberRole.manager.value, ProjectMemberRole.member.value}


def is_admin(user: User) -> bool:
    return user.role == UserRole.admin.value


def can_view_project(db: Session, user: User, project: Project) -> bool:
    if is_admin(user):
        return True
    if _has_explicit_access(db, user, project):
        return True

    visibility = project.visibility or ProjectVisibility.organization.value
    if visibility == ProjectVisibility.organization.value:
        return True
    if visibility == ProjectVisibility.department.value:
        return (
            user.department_id is not None
            and project.department_id is not None
            and user.department_id == project.department_id
        )
    return False


def can_edit_project(db: Session, user: User, project: Project) -> bool:
    if is_admin(user):
        return True
    if project.owner_user_id == user.id:
        return True
    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == user.id,
        )
        .first()
    )
    return member is not None and member.role in _EDIT_ROLES


def visible_projects_query(db: Session, user: User) -> Query:
    if is_admin(user):
        return db.query(Project)

    member_exists = exists().where(
        and_(
            ProjectMember.project_id == Project.id,
            ProjectMember.user_id == user.id,
        )
    )
    grant_exists = exists().where(
        and_(
            ProjectVisibilityGrant.project_id == Project.id,
            ProjectVisibilityGrant.user_id == user.id,
        )
    )
    same_department = and_(
        Project.visibility == ProjectVisibility.department.value,
        Project.department_id.isnot(None),
        Project.department_id == user.department_id,
        user.department_id.isnot(None),
    )

    return db.query(Project).filter(
        or_(
            Project.owner_user_id == user.id,
            member_exists,
            grant_exists,
            Project.visibility == ProjectVisibility.organization.value,
            same_department,
        )
    )


def require_project_view(db: Session, user: User, project: Project) -> None:
    from app.core.exceptions import AppException

    if not can_view_project(db, user, project):
        raise AppException("You do not have access to this project.", status_code=403)


def require_project_edit(db: Session, user: User, project: Project) -> None:
    from app.core.exceptions import AppException

    if not can_edit_project(db, user, project):
        raise AppException("You do not have permission to modify this project.", status_code=403)


def _has_explicit_access(db: Session, user: User, project: Project) -> bool:
    if project.owner_user_id == user.id:
        return True
    if (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == user.id,
        )
        .first()
    ):
        return True
    if (
        db.query(ProjectVisibilityGrant)
        .filter(
            ProjectVisibilityGrant.project_id == project.id,
            ProjectVisibilityGrant.user_id == user.id,
        )
        .first()
    ):
        return True
    return False
