from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base

"""
parent_goal_id (int)
department_id (int)
owner_user_id (int)
name (str)
description (str)
goal_type (str)
status (str)
start_date (datetime)
due_date (datetime)
source_type (str)
source_external_id (str)
"""

class Goal(Base):
    __tablename__ = "goals"
    # Hierarchy (self-referencing tree)
    parent_goal_id = Column(
        Integer,
        ForeignKey("goals.id"),
        nullable=True
    )
    # Ownership / grouping
    department_id = Column(Integer, ForeignKey("departments.id"))
    owner_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    # Core content
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    goal_type = Column(String, default="strategic")  # strategic, operational, etc.
    status = Column(String, default="active")        # active, paused, completed

    # Planning
    start_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)

    # Source tracking (optional integration future-proofing)
    source_type = Column(String, nullable=True)
    source_external_id = Column(String, nullable=True)

    # Relationships
    parent_goal = relationship("Goal", remote_side=[id], backref="child_goals")
    department = relationship("Department", back_populates="goals")