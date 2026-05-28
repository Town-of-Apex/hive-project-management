"""
app/models/project_visibility_grant.py

Whitelist entries granting a user view access to a project regardless of visibility mode.
"""
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProjectVisibilityGrant(Base):
    __tablename__ = "project_visibility_grants"
    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="uq_project_visibility_grants_project_user"),
    )

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    project = relationship("Project", back_populates="visibility_grants")
    user = relationship("User")
