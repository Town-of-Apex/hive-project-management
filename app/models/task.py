from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    parent_task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=True
    )

    assignee_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    status = Column(String, default="todo")
    priority = Column(String, default="medium")

    start_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    source_type = Column(String, nullable=True)
    source_external_id = Column(String, nullable=True)

    # Relationships

    project = relationship(
        "Project",
        back_populates="tasks"
    )

    assignee = relationship(
        "User",
        foreign_keys=[assignee_user_id]
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by_user_id]
    )

    child_tasks = relationship(
        "Task",
        back_populates="parent_task",
        cascade="all, delete-orphan"
    )

    parent_task = relationship(
        "Task",
        back_populates="child_tasks",
        remote_side="Task.id"
    )

    comments = relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan"
    )