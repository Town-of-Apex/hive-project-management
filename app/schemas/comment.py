"""
app/schemas/comment.py

Pydantic schemas for the Comment resource.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class CommentCreate(BaseModel):
    task_id: Optional[int] = None
    project_id: Optional[int] = None
    author_user_id: int
    content: str

    @field_validator("content")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class CommentUpdate(BaseModel):
    task_id: Optional[int] = None
    project_id: Optional[int] = None
    content: Optional[str] = None

    @field_validator("content")
    @classmethod
    def not_empty_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be blank")
        return v.strip() if v is not None else None


class CommentRead(BaseModel):
    id: int
    task_id: Optional[int]
    project_id: Optional[int]
    author_user_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
