"""
app/schemas/status_update.py

Pydantic schemas for the StatusUpdate resource.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class StatusUpdateCreate(BaseModel):
    project_id: int
    author_user_id: int
    status: str
    summary: str

    @field_validator("status", "summary")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class StatusUpdateUpdate(BaseModel):
    status: Optional[str] = None
    summary: Optional[str] = None

    @field_validator("status", "summary")
    @classmethod
    def not_empty_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be blank")
        return v.strip() if v is not None else None


class StatusUpdateRead(BaseModel):
    id: int
    project_id: int
    author_user_id: int
    status: str
    summary: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
