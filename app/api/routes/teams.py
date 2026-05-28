"""
app/api/routes/teams.py

FastAPI router for the /api/teams resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok
from app.core.exceptions import AppException
from app.schemas.team import TeamCreate, TeamUpdate, TeamRead
from app.services.team_service import team_service

router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.post("", status_code=201)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    """Create a new team."""
    team = team_service.create(db, obj_in=payload)
    return ok(TeamRead.model_validate(team).model_dump())


@router.get("")
def list_teams(
    search: Optional[str] = Query(None, description="Free-text search across name and description"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return a filtered, paginated list of teams."""
    filters = {}
    if department_id is not None:
        filters["department_id"] = department_id
        
    teams = team_service.list(
        db, 
        skip=skip, 
        limit=limit, 
        filters=filters,
        search_query=search, 
        search_fields=["name", "description"]
    )
    return ok([TeamRead.model_validate(t).model_dump() for t in teams])


@router.get("/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Fetch a single team by ID."""
    team = team_service.get(db, team_id)
    if not team:
        raise AppException(f"Team {team_id} not found.", status_code=404)
    return ok(TeamRead.model_validate(team).model_dump())


@router.put("/{team_id}")
def update_team(team_id: int, payload: TeamUpdate, db: Session = Depends(get_db)):
    """Update one or more fields on an existing team."""
    team = team_service.get(db, team_id)
    if not team:
        raise AppException(f"Team {team_id} not found.", status_code=404)
    updated = team_service.update(db, db_obj=team, obj_in=payload)
    return ok(TeamRead.model_validate(updated).model_dump())


@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """Permanently delete a team."""
    deleted = team_service.delete(db, id=team_id)
    if not deleted:
        raise AppException(f"Team {team_id} not found.", status_code=404)
    return ok({"deleted": True, "id": team_id})