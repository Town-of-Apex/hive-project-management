"""
app/services/goal_service.py

Business logic layer for goals.
"""
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate
from .base_service import BaseService


class GoalService(BaseService[Goal, GoalCreate, GoalUpdate]):
    """
    Goal service.
    Inherits generic CRUD capabilities from BaseService.
    """
    pass


goal_service = GoalService(Goal)