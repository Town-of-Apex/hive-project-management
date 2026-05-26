from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Thing(Base):
    __tablename__ = "things"

    department_id = Column(Integer, ForeignKey("departments.id"))
    owner_user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String, nullable=False)
    description = Column(Text)

    status = Column(String, default="active")
    priority = Column(String, default="medium")

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    owner = relationship("User")
    tasks = relationship("Task", back_populates="project")