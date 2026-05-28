"""
app/schemas/user.py

Pydantic schemas for the User resource.
"""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, field_validator

from app.schemas.enums import UserRole


class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str
    email: Optional[EmailStr] = None
    role: UserRole = UserRole.user
    department_id: Optional[int] = None
    team_id: Optional[int] = None

    @field_validator("username", "full_name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None
    team_id: Optional[int] = None

    @field_validator("password")
    @classmethod
    def password_length(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    email: Optional[str]
    role: str
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    is_active: bool
    team_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


def user_read_dict(user: Any) -> dict:
    """Serialize a User ORM instance including optional department name."""
    data = UserRead.model_validate(user).model_dump()
    dept = getattr(user, "department", None)
    if dept is not None:
        data["department_name"] = dept.name
    return data
