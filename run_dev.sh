#!/usr/bin/env bash
# Hive Project Management — Dev Mode (macOS / Linux)
# Parity with run_dev.ps1

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

SKIP_SEED=false
for arg in "$@"; do
  case "$arg" in
    --skip-seed) SKIP_SEED=true ;;
  esac
done

echo ""
echo "Hive Project Management — Dev Mode"
echo ""

# Virtual environment
if [[ ! -x ".venv/bin/python" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

PYTHON=".venv/bin/python"
PIP=".venv/bin/pip"

echo "Installing Python dependencies..."
"$PIP" install -q -r requirements.txt

# PostgreSQL container
echo "Starting PostgreSQL (apex-db)..."
if ! docker network inspect apex-internal >/dev/null 2>&1; then
  echo "Creating docker network apex-internal..."
  docker network create apex-internal
fi
docker compose up -d apex-db >/dev/null

echo "Waiting for PostgreSQL on localhost:5432..."
ready=false
for _ in $(seq 1 30); do
  if (echo >/dev/tcp/localhost/5432) >/dev/null 2>&1; then
    ready=true
    break
  fi
  sleep 1
done
if [[ "$ready" != true ]]; then
  echo "PostgreSQL did not become ready on port 5432. Is apex-db running?" >&2
  exit 1
fi

# Host dev always targets local apex-db
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/apex_db"
export ALLOW_SQLITE_FALLBACK="false"

# Load optional .env (except DATABASE_URL overrides)
if [[ -f ".env" ]]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ "$line" =~ ^[[:space:]]*$ ]] && continue
    if [[ "$line" =~ ^[[:space:]]*([^=]+)=(.*)$ ]]; then
      key="${BASH_REMATCH[1]// /}"
      val="${BASH_REMATCH[2]}"
      if [[ "$key" != "DATABASE_URL" && "$key" != "ALLOW_SQLITE_FALLBACK" ]]; then
        export "$key=$val"
      fi
    fi
  done < ".env"
fi

echo "Running database migrations..."
"$PYTHON" -m alembic upgrade head

if [[ "$SKIP_SEED" == false ]]; then
  echo "Seeding development data..."
  "$PYTHON" scripts/seed_dev.py
else
  echo "Skipping seed (--skip-seed)."
fi

cleanup() {
  echo ""
  echo "Stopping backend..."
  [[ -n "${BACKEND_PID:-}" ]] && kill "$BACKEND_PID" 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM

echo ""
echo "Starting backend (uvicorn :8080)..."
"$PYTHON" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080 &
BACKEND_PID=$!

if [[ ! -d "frontend/node_modules" ]]; then
  echo "Installing frontend dependencies..."
  (cd frontend && npm install)
fi

echo ""
echo "Starting frontend (Vite :5173)..."
echo "Open http://localhost:5173 and sign in with devadmin / devadmin123"
echo ""

cd frontend
npm run dev
