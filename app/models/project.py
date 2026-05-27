from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    department_id = Column(Integer, ForeignKey("departments.id"))
    owner_user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String, nullable=False)
    description = Column(Text)

    status = Column(String, default="active")
    priority = Column(String, default="medium")
    visibility = Column(String, default="organization", nullable=False)

    department = relationship("Department", back_populates="projects")
    owner = relationship("User")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="project", cascade="all, delete-orphan")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    status_updates = relationship("StatusUpdate", back_populates="project", cascade="all, delete-orphan")