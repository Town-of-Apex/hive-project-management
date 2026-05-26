"""
app/models/status_update.py

SQLAlchemy ORM model for the status_updates table.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class StatusUpdate(Base):
    """
    StatusUpdate model.
    Tracks status updates for a project (on track, off track, etc.).
    Inherits id, created_at, and updated_at from Base.
    """
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    author_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    status = Column(String(50), nullable=False)  # e.g., "on_track", "at_risk", "off_track"
    summary = Column(Text, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="status_updates")
    author = relationship("User")