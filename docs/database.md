# Database

Hive uses **PostgreSQL** (`apex-db` container) with **Alembic** for schema migrations.

## Local development

```powershell
docker network create apex-internal   # once
docker compose up -d apex-db
.\.venv\Scripts\python -m alembic upgrade head
.\.venv\Scripts\python scripts/seed_dev.py
```

Or use `.\run_dev.ps1`, which runs migrations and seed automatically.

## Connection URLs

| Environment | URL |
|-------------|-----|
| Host (`run_dev.ps1`) | `postgresql+psycopg://postgres:postgres@localhost:5432/apex_db` |
| Docker backend | `postgresql+psycopg://postgres:postgres@apex-db:5432/apex_db` |

## New migrations

```powershell
.\.venv\Scripts\python -m alembic revision -m "describe_change" --autogenerate
.\.venv\Scripts\python -m alembic upgrade head
```

## Port conflicts

If `docker compose up -d apex-db` fails with port 5432 already allocated, stop the other service or change the host port in `docker-compose.yml` and set `DATABASE_URL` accordingly in `run_dev.ps1`.
