"""
app/schemas/project_visibility_grant.py

Pydantic schemas for project visibility whitelist grants.
"""
from datetime import datetime

from pydantic import BaseModel


class ProjectVisibilityGrantCreate(BaseModel):
    user_id: int


class ProjectVisibilityGrantRead(BaseModel):
    id: int
    project_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
