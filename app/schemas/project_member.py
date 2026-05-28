"""
app/schemas/project_member.py

Pydantic schemas for the ProjectMember resource.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class ProjectMemberCreate(BaseModel):
    project_id: int
    user_id: int
    role: Optional[str] = "member"

    @field_validator("role")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class ProjectMemberUpdate(BaseModel):
    role: Optional[str] = None

    @field_validator("role")
    @classmethod
    def not_empty_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be blank")
        return v.strip() if v is not None else None


class ProjectMemberRead(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
