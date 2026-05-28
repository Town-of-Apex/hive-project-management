"""
app/models/project_member.py

SQLAlchemy ORM model for the project_members table.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProjectMember(Base):
    """
    ProjectMember model.
    Maps users to projects they are members of, with an assigned role.
    Inherits id, created_at, and updated_at from Base.
    """
    __tablename__ = "project_members"
    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="uq_project_members_project_user"),
    )

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), nullable=False, default="member")  # e.g., "manager", "contributor", "viewer"

    # Relationships
    project = relationship("Project", back_populates="members")
    user = relationship("User")