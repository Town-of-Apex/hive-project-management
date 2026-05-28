from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"


    department_id = Column(Integer, ForeignKey("departments.id"))

    owner_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # relationships
    department = relationship("Department", back_populates="teams")

    owner = relationship(
        "User",
        foreign_keys=[owner_user_id]
    )

    members = relationship(
        "User",
        back_populates="team",
        foreign_keys="User.team_id",
    )