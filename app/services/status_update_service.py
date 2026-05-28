"""
app/services/status_update_service.py

Business logic layer for status updates.
"""
from app.models.status_update import StatusUpdate
from app.schemas.status_update import StatusUpdateCreate, StatusUpdateUpdate
from .base_service import BaseService


class StatusUpdateService(BaseService[StatusUpdate, StatusUpdateCreate, StatusUpdateUpdate]):
    """
    StatusUpdate service.
    Inherits generic CRUD capabilities from BaseService.
    """
    pass


status_update_service = StatusUpdateService(StatusUpdate)
