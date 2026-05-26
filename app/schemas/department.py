from pydantic import BaseModel, field_validator
from typing import Optional



class DepartmentCreate(BaseModel):
    owner_user_id: Optional[int] = None

    name: str
    description: Optional[str] = None
    
    
class DepartmentUpdate(BaseModel):
    owner_user_id: Optional[int] = None

    name: Optional[str] = None
    description: Optional[str] = None
    
from datetime import datetime


class DepartmentResponse(BaseModel):
    id: int

    owner_user_id: Optional[int]

    name: str
    description: Optional[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True