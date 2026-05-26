from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.team import TeamCreate, TeamUpdate
from app.services.team_service import (
    create_team,
    get_team,
    get_teams,
    update_team,
    delete_team
)


router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/")
def create(data: TeamCreate, db: Session = Depends(get_db)):
    return create_team(db, data)


@router.get("/{team_id}")
def read(team_id: int, db: Session = Depends(get_db)):
    return get_team(db, team_id)


@router.get("/")
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_teams(db, skip, limit)


@router.put("/{team_id}")
def update(team_id: int, data: TeamUpdate, db: Session = Depends(get_db)):
    return update_team(db, team_id, data)


@router.delete("/{team_id}")
def delete(team_id: int, db: Session = Depends(get_db)):
    return delete_team(db, team_id)