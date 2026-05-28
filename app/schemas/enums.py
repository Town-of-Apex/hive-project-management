"""
app/schemas/enums.py

Pydantic-facing enum types shared across schemas.
"""
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class ProjectMemberRole(str, Enum):
    manager = "manager"
    member = "member"
    viewer = "viewer"


class ProjectVisibility(str, Enum):
    private = "private"
    department = "department"
    organization = "organization"
