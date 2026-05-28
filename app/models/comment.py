"""
app/models/comment.py

SQLAlchemy ORM model for the comments table.
"""
from sqlalchemy import Column, Integer, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    """
    Comment model.
    Exactly one of task_id or project_id must be set (enforced in DB and service layer).
    """
    __table_args__ = (
        CheckConstraint(
            "(task_id IS NOT NULL AND project_id IS NULL) OR "
            "(task_id IS NULL AND project_id IS NOT NULL)",
            name="ck_comments_task_xor_project",
        ),
    )

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    author_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=False)

    task = relationship("Task", back_populates="comments")
    project = relationship("Project", back_populates="comments")
    author = relationship("User")
