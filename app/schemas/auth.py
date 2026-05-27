"""
app/schemas/auth.py

Pydantic schemas for authentication endpoints.
"""
from pydantic import BaseModel, field_validator

from app.schemas.user import UserRead


class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Username is required")
        return v.strip()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    user: UserRead
