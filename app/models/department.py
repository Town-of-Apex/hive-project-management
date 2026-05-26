from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Department(Base):
    __tablename__ = "departments"

    owner_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # relationships
    owner = relationship(
        "User",
        foreign_keys=[owner_user_id]
    )

    teams = relationship(
        "Team",
        back_populates="department"
    )

    goals = relationship(
        "Goal",
        back_populates="department"
    )