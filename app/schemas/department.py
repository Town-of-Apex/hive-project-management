"""
app/schemas/department.py

Pydantic schemas for the Department resource.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class DepartmentCreate(BaseModel):
    owner_user_id: Optional[int] = None
    name: str
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class DepartmentUpdate(BaseModel):
    owner_user_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def not_empty_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be blank")
        return v.strip() if v is not None else None


class DepartmentRead(BaseModel):
    id: int
    owner_user_id: Optional[int]
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}