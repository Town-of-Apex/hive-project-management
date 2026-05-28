"""
app/api/routes/auth.py

Authentication stub routes (login / current user).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, get_current_user
from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.responses import ok
from app.core.security import verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, MeResponse, TokenResponse
from app.schemas.user import UserRead
from app.services.user_service import user_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = user_service.get_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise AppException("Invalid username or password.", status_code=401)
    if not user.is_active:
        raise AppException("Account is inactive.", status_code=401)

    token = create_access_token(user_id=user.id, username=user.username, role=user.role)
    return ok(TokenResponse(access_token=token).model_dump())


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return ok(MeResponse(user=UserRead.model_validate(current_user)).model_dump())
