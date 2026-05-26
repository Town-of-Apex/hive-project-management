from sqlalchemy.orm import Session

from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate


# -----------------------------
# CREATE
# -----------------------------

def create_team(db: Session, team_data: TeamCreate):

    team = Team(
        department_id=team_data.department_id,
        owner_user_id=team_data.owner_user_id,

        name=team_data.name,
        description=team_data.description
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return team

# -----------------------------
# UPDATE
# -----------------------------

def update_team(db: Session, team_id: int, team_data: TeamUpdate):

    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        return None

    if team_data.department_id is not None:
        team.department_id = team_data.department_id

    if team_data.owner_user_id is not None:
        team.owner_user_id = team_data.owner_user_id

    if team_data.name is not None:
        team.name = team_data.name.strip()

    if team_data.description is not None:
        team.description = team_data.description

    db.commit()
    db.refresh(team)

    return team

# -----------------------------
# GET SINGLE
# -----------------------------

def get_team(db: Session, team_id: int):

    return db.query(Team).filter(Team.id == team_id).first()

# -----------------------------
# LIST
# -----------------------------

def get_teams(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Team).offset(skip).limit(limit).all()

# -----------------------------
# DELETE
# -----------------------------

def delete_team(db: Session, team_id: int):

    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        return None

    db.delete(team)
    db.commit()

    return team