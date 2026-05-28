"""
app/services/comment_service.py

Business logic layer for comments.
"""
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.comment_validation import validate_comment_parents
from .base_service import BaseService


class CommentService(BaseService[Comment, CommentCreate, CommentUpdate]):
    def create(self, db: Session, *, obj_in: CommentCreate, extra_data=None) -> Comment:
        validate_comment_parents(task_id=obj_in.task_id, project_id=obj_in.project_id)
        return super().create(db, obj_in=obj_in, extra_data=extra_data)

    def update(
        self,
        db: Session,
        *,
        db_obj: Comment,
        obj_in: CommentUpdate,
    ) -> Comment:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "task_id" in update_data or "project_id" in update_data:
            task_id = update_data.get("task_id", db_obj.task_id)
            project_id = update_data.get("project_id", db_obj.project_id)
            validate_comment_parents(task_id=task_id, project_id=project_id)
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


comment_service = CommentService(Comment)
