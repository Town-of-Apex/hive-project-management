"""
app/schemas/goal.py

Pydantic schemas for the Goal resource.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class GoalCreate(BaseModel):
    parent_goal_id: Optional[int] = None
    department_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    goal_type: str = "strategic"
    status: str = "active"
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    source_type: Optional[str] = None
    source_external_id: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()


class GoalUpdate(BaseModel):
    parent_goal_id: Optional[int] = None
    department_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    goal_type: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None

    @field_validator("name")
    @classmethod
    def validate_name_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Name cannot be blank")
        return v.strip() if v is not None else None


class GoalRead(BaseModel):
    id: int
    parent_goal_id: Optional[int]
    department_id: Optional[int]
    owner_user_id: Optional[int]
    name: str
    description: Optional[str]
    goal_type: str
    status: str
    start_date: Optional[datetime]
    due_date: Optional[datetime]
    source_type: Optional[str]
    source_external_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}