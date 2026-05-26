"""
app/services/comment_service.py

Business logic layer for comments.
"""
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from .base_service import BaseService


class CommentService(BaseService[Comment, CommentCreate, CommentUpdate]):
    """
    Comment service.
    Inherits generic CRUD capabilities from BaseService.
    """
    pass


comment_service = CommentService(Comment)
