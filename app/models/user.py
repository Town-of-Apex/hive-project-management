"""
app/models/user.py

SQLAlchemy ORM model for the users table.
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import UserRole


class User(Base):
    """
    Standard User model.
    Automatically maps to 'users' table.
    Inherits 'id', 'created_at', and 'updated_at' audit fields from Base.
    """
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), nullable=True)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False, default=UserRole.user.value)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="members", foreign_keys=[team_id])
    department = relationship("Department", foreign_keys=[department_id])
