"""
app/services/team_service.py

Business logic layer for teams.
"""
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate
from .base_service import BaseService


class TeamService(BaseService[Team, TeamCreate, TeamUpdate]):
    """
    Team service.
    Inherits generic CRUD capabilities from BaseService.
    """
    pass


team_service = TeamService(Team)