"""
app/services/task_service.py

Business logic layer for tasks.
"""
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.project_visibility import (
    can_view_project,
    require_project_edit,
    require_project_view,
    visible_projects_query,
)
from .base_service import BaseService

_VALID_PRIORITIES = {"low", "medium", "high"}


class TaskService(BaseService[Task, TaskCreate, TaskUpdate]):
    """Task service with project-scoped authorization and validation."""

    def validate_priority(self, priority: Optional[str]) -> None:
        if priority is not None and priority not in _VALID_PRIORITIES:
            raise AppException(
                f"Invalid priority '{priority}'. Allowed: {', '.join(sorted(_VALID_PRIORITIES))}.",
                status_code=400,
            )

    def get_project(self, db: Session, project_id: int) -> Project:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise AppException(f"Project {project_id} not found.", status_code=404)
        return project

    def get_task_for_user(
        self,
        db: Session,
        *,
        task_id: int,
        user: User,
        require_edit: bool = False,
    ) -> Task:
        task = self.get(db, task_id)
        if not task:
            raise AppException(f"Task {task_id} not found.", status_code=404)

        project = self.get_project(db, task.project_id)
        if require_edit:
            require_project_edit(db, user, project)
        else:
            require_project_view(db, user, project)
        return task

    def _is_project_assignee(self, db: Session, project: Project, user_id: int) -> bool:
        if project.owner_user_id == user_id:
            return True
        return (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == user_id,
            )
            .first()
            is not None
        )

    def validate_assignee(
        self,
        db: Session,
        project: Project,
        assignee_user_id: Optional[int],
    ) -> None:
        if assignee_user_id is None:
            return
        assignee = db.query(User).filter(User.id == assignee_user_id).first()
        if not assignee:
            raise AppException(f"User {assignee_user_id} not found.", status_code=404)
        if not self._is_project_assignee(db, project, assignee_user_id):
            raise AppException(
                "Assignee must be the project owner or a project member.",
                status_code=400,
            )

    def validate_parent_task(
        self,
        db: Session,
        *,
        project_id: int,
        parent_task_id: Optional[int],
        task_id: Optional[int] = None,
    ) -> None:
        if parent_task_id is None:
            return
        if task_id is not None and parent_task_id == task_id:
            raise AppException("A task cannot be its own parent.", status_code=400)

        parent = self.get(db, parent_task_id)
        if not parent:
            raise AppException(f"Parent task {parent_task_id} not found.", status_code=404)
        if parent.project_id != project_id:
            raise AppException(
                "Parent task must belong to the same project.",
                status_code=400,
            )

    def apply_completed_at(self, *, status: str, completed_at: Optional[datetime]) -> Optional[datetime]:
        if status == "done":
            return completed_at or datetime.now(timezone.utc)
        return None

    def list_for_user(
        self,
        db: Session,
        user: User,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None,
        search_query: Optional[str] = None,
        search_fields: Optional[list] = None,
    ) -> List[Task]:
        filters = dict(filters or {})
        project_id = filters.pop("project_id", None)

        if project_id is not None:
            project = self.get_project(db, project_id)
            require_project_view(db, user, project)
            filters["project_id"] = project_id
            return self.list(
                db,
                skip=skip,
                limit=limit,
                filters=filters,
                search_query=search_query,
                search_fields=search_fields,
            )

        visible_project_ids = [
            project.id for project in visible_projects_query(db, user).all()
        ]
        if not visible_project_ids:
            return []

        query = db.query(Task).filter(Task.project_id.in_(visible_project_ids))
        for field, value in filters.items():
            if hasattr(Task, field):
                query = query.filter(getattr(Task, field) == value)

        if search_query and search_fields:
            from sqlalchemy import or_

            search_filters = []
            term = f"%{search_query}%"
            for field in search_fields:
                if hasattr(Task, field):
                    search_filters.append(getattr(Task, field).ilike(term))
            if search_filters:
                query = query.filter(or_(*search_filters))

        return query.offset(skip).limit(limit).all()

    def create_for_user(
        self,
        db: Session,
        *,
        user: User,
        obj_in: TaskCreate,
    ) -> Task:
        project = self.get_project(db, obj_in.project_id)
        require_project_edit(db, user, project)

        create_data = obj_in.model_dump(mode="json")
        if create_data.get("created_by_user_id") is None:
            create_data["created_by_user_id"] = user.id

        self.validate_parent_task(
            db,
            project_id=obj_in.project_id,
            parent_task_id=create_data.get("parent_task_id"),
        )
        self.validate_assignee(db, project, create_data.get("assignee_user_id"))
        self.validate_priority(create_data.get("priority") or "medium")

        status = create_data.get("status") or "todo"
        create_data["completed_at"] = self.apply_completed_at(
            status=status,
            completed_at=create_data.get("completed_at"),
        )

        return self.create(db, obj_in=TaskCreate(**create_data))

    def update_for_user(
        self,
        db: Session,
        *,
        user: User,
        db_obj: Task,
        obj_in: TaskUpdate,
    ) -> Task:
        project = self.get_project(db, db_obj.project_id)
        require_project_edit(db, user, project)

        update_data = obj_in.model_dump(exclude_unset=True, mode="json")
        target_project_id = update_data.get("project_id", db_obj.project_id)
        if target_project_id != db_obj.project_id:
            target_project = self.get_project(db, target_project_id)
            require_project_edit(db, user, target_project)

        parent_task_id = update_data.get("parent_task_id", db_obj.parent_task_id)
        if "parent_task_id" in update_data or "project_id" in update_data:
            self.validate_parent_task(
                db,
                project_id=target_project_id,
                parent_task_id=parent_task_id,
                task_id=db_obj.id,
            )

        if "assignee_user_id" in update_data:
            target_project = self.get_project(db, target_project_id)
            self.validate_assignee(db, target_project, update_data.get("assignee_user_id"))

        if "priority" in update_data:
            self.validate_priority(update_data.get("priority"))

        if "status" in update_data:
            if update_data["status"] == "done":
                update_data["completed_at"] = self.apply_completed_at(
                    status=update_data["status"],
                    completed_at=update_data.get("completed_at", db_obj.completed_at),
                )
            else:
                update_data["completed_at"] = None

        return self.update(db, db_obj=db_obj, obj_in=update_data)

    def delete_for_user(self, db: Session, *, user: User, task_id: int) -> bool:
        task = self.get_task_for_user(db, task_id=task_id, user=user, require_edit=True)
        return self.delete(db, id=task.id)


task_service = TaskService(Task)
