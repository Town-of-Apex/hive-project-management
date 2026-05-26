"""
app/schemas/project.py

Pydantic schemas for the Project resource.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class ProjectCreate(BaseModel):
    department_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    status: str = "active"
    priority: str = "medium"

    @field_validator("name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class ProjectUpdate(BaseModel):
    department_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

    @field_validator("name")
    @classmethod
    def not_empty_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be blank")
        return v.strip() if v is not None else None


class ProjectRead(BaseModel):
    id: int
    department_id: Optional[int]
    owner_user_id: Optional[int]
    name: str
    description: Optional[str]
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}