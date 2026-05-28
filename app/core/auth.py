"""
app/core/auth.py

JWT authentication helpers for the dev auth stub.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import AppException
from app.models.enums import UserRole
from app.models.user import User

security_scheme = HTTPBearer(auto_error=False)

ALGORITHM = "HS256"


def create_access_token(*, user_id: int, username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise AppException("Invalid or expired token.", status_code=401) from exc


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or not credentials.credentials:
        raise AppException("Authentication required.", status_code=401)

    payload = decode_token(credentials.credentials)
    user_id = int(payload.get("sub", 0))
    user = (
        db.query(User)
        .options(joinedload(User.department))
        .filter(User.id == user_id)
        .first()
    )
    if not user or not user.is_active:
        raise AppException("User not found or inactive.", status_code=401)
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.admin.value:
        raise AppException("Administrator access required.", status_code=403)
    return user
