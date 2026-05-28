"""
app/schemas/project_member.py

Pydantic schemas for the ProjectMember resource.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import ProjectMemberRole


class ProjectMemberCreate(BaseModel):
    project_id: int
    user_id: int
    role: ProjectMemberRole = ProjectMemberRole.member


class ProjectMemberUpdate(BaseModel):
    role: Optional[ProjectMemberRole] = None


class ProjectMemberRead(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
