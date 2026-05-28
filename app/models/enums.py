"""
app/models/enums.py

Shared string enums for roles and visibility.
Stored as plain strings in the database for simple migrations and API contracts.
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
