"""
app/schemas/task.py

Pydantic schemas for the Task resource.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class TaskCreate(BaseModel):
    project_id: int
    parent_task_id: Optional[int] = None
    assignee_user_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    source_type: Optional[str] = None
    source_external_id: Optional[str] = None

    @field_validator("title")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class TaskUpdate(BaseModel):
    project_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    assignee_user_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def not_empty_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be blank")
        return v.strip() if v is not None else None


class TaskRead(BaseModel):
    id: int
    project_id: int
    parent_task_id: Optional[int]
    assignee_user_id: Optional[int]
    created_by_user_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    start_date: Optional[datetime]
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    source_type: Optional[str]
    source_external_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}