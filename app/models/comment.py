"""
app/models/comment.py

SQLAlchemy ORM model for the comments table.
"""
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    """
    Comment model.
    Allows users to post comments on tasks or projects.
    Inherits id, created_at, and updated_at from Base.
    """
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    author_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=False)

    # Relationships
    task = relationship("Task", back_populates="comments")
    project = relationship("Project", back_populates="comments")
    author = relationship("User")