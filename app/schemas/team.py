from pydantic import BaseModel, field_validator
from typing import Optional


class TeamCreate(BaseModel):
    department_id: int
    owner_user_id: Optional[int] = None

    name: str
    description: Optional[str] = None
    
    @field_validator("name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()
    

class TeamUpdate(BaseModel):
    department_id: Optional[int] = None
    owner_user_id: Optional[int] = None

    name: Optional[str] = None
    description: Optional[str] = None
    
    
from datetime import datetime


class TeamResponse(BaseModel):
    id: int

    department_id: int
    owner_user_id: Optional[int]

    name: str
    description: Optional[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True