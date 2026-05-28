"""
app/services/task_service.py

Business logic layer for tasks.
"""
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from .base_service import BaseService


class TaskService(BaseService[Task, TaskCreate, TaskUpdate]):
    """
    Task service.
    Inherits generic CRUD capabilities from BaseService.
    """
    pass


task_service = TaskService(Task)