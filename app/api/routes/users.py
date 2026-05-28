"""
app/api/routes/users.py

FastAPI router for user CRUD operations.
Routes are thin wrapper over user_service.py.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, require_admin
from app.core.database import get_db
from app.models.user import User
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.user import UserCreate, UserUpdate, user_directory_dict, user_read_dict
from app.services.user_service import user_service

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/directory")
def list_users_directory(
    skip: int = Query(0, ge=0),
    limit: int = Query(500, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """List active users for display (names on projects/tasks). Non-admin accessible."""
    users = user_service.list_directory(db, skip=skip, limit=limit)
    return ok([user_directory_dict(u) for u in users])


@router.post("", status_code=201)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Create a new user."""
    try:
        user = user_service.create_user(db, payload)
        return ok(user_read_dict(user))
    except ValueError as e:
        raise AppException(str(e), status_code=400)


@router.get("")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """List all registered users."""
    users = user_service.list_users(db, skip=skip, limit=limit)
    return ok([user_read_dict(u) for u in users])


@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Fetch a single user by ID."""
    user = user_service.get(db, user_id)
    if not user:
        raise AppException(f"User {user_id} not found.", status_code=404)
    return ok(user_read_dict(user))


@router.put("/{user_id}")
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Update an existing user's details."""
    try:
        user = user_service.update_user(db, user_id, payload)
    except ValueError as e:
        raise AppException(str(e), status_code=400)

    if not user:
        raise AppException(f"User {user_id} not found.", status_code=404)
    return ok(user_read_dict(user))


@router.delete("/{user_id}", status_code=200)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Permanently delete a user from the database."""
    deleted = user_service.delete(db, id=user_id)
    if not deleted:
        raise AppException(f"User {user_id} not found.", status_code=404)
    return ok({"deleted": True, "id": user_id})
