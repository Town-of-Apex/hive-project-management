# Hive Project Management Platform

Version 0.5.0 — internal project management for the Town of Apex.

## Local development (recommended)

### Prerequisites

- Docker Desktop
- Python 3.13+
- Node.js 20+

### One-time setup

```powershell
docker network create apex-internal
```

Copy environment template and adjust if needed:

```powershell
copy .env.example .env
```

### Start dev stack

From the repository root:

```powershell
.\run_dev.ps1
```

This script:

1. Creates/uses `.venv` and installs Python dependencies
2. Starts the `apex-db` PostgreSQL container (`localhost:5432`)
3. Runs `alembic upgrade head`
4. Seeds dev data (`devadmin` / `devadmin123`) unless you pass `-SkipSeed`
5. Launches the FastAPI backend on port **8080** (new window)
6. Launches the Vite frontend on port **5173** (current window)

Open [http://localhost:5173](http://localhost:5173), sign in, and go to **Projects**.

### Database

| Context | `DATABASE_URL` |
|---------|----------------|
| Host (`run_dev.ps1`) | `postgresql+psycopg://postgres:postgres@localhost:5432/apex_db` |
| Docker backend | `postgresql+psycopg://postgres:postgres@apex-db:5432/apex_db` |

Schema changes are managed with **Alembic** (not `create_all` on startup).

```powershell
.\.venv\Scripts\python -m alembic upgrade head
.\.venv\Scripts\python scripts/seed_dev.py
```

### Auth stub

Development uses username/password login with JWT. Seeded admin:

- **Username:** `devadmin`
- **Password:** `devadmin123`

Production Microsoft Entra ID integration is planned for a later phase.

## Full Docker stack

```powershell
docker network create apex-internal
docker compose up --build
```

See [TEMPLATE_README.md](TEMPLATE_README.md) for architecture details inherited from the Apex application template.

---

## Roadmap and next steps

Use this section as the working backlog when picking up development. Follow the [App-Architecture](.agents/skills/App-Architecture/SKILL.md) skill for structure (routes → services → models/schemas; frontend pages → services → types).

### Completed (Phase 0 — foundation)

- [x] Removed permit template code (backend + frontend)
- [x] PostgreSQL via `apex-db` container; Alembic migrations (`001_initial_hive_schema`)
- [x] Project model hardening (`project_members` table, unique constraint, `visibility` column, department ↔ project links)
- [x] Dev seed data (`scripts/seed_dev.py`) — `devadmin` / `devadmin123`, sample projects and tasks
- [x] JWT auth stub (`/api/auth/login`, `/api/auth/me`); projects/tasks require login
- [x] Basic Projects UI (list, search, status filter, create project, task counts)
- [x] `run_dev.ps1` orchestration (DB, migrate, seed, backend window, frontend)
- [x] `User.department_id` FK (replaces free-text `department` string; migration `002`)
- [x] Comment XOR rule: exactly one of `task_id` or `project_id` (DB check + Pydantic/service validation)
- [x] `department_id` filter on `GET /api/projects`
- [x] App roles (`users.role`: `admin`, `user`) and project member roles (`manager`, `member`, `viewer`)
- [x] Project visibility enforcement (`private` / `department` / `organization`) + whitelist grants API
- [x] `UserProfilePage` wired to `/api/auth/me` (real user + department name)

### Immediate polish (do soon)

- [ ] Smoke-test full `.\run_dev.ps1` flow after migration `002` (existing DBs: run `alembic upgrade head`)
- [ ] Settings page: wire user admin to auth token (admin-only `/api/users` already protected)

### Phase 1 — Authentication (production path)

**Goal:** No anonymous API access in deployed environments; staff sign in with Town identity.

| Task | Notes |
|------|--------|
| Microsoft Entra ID (OIDC) | Per template direction; JIT user provisioning from AD claims |
| Remove or gate dev password login | Disable stub login in production via env flag |
| Require `JWT_SECRET` at startup | Fail fast if unset in non-dev environments |
| Session / token refresh | Optional refresh token or shorter-lived access tokens |
| Frontend login UX | “Sign in with Microsoft” + handle redirect/callback |

**Definition of done:** Deployed app uses Entra; dev can still use local stub when `DEV_AUTH_STUB=true`.

### Phase 2 — Roles and project visibility

**Goal:** Authorization in **services**, not only in the UI.

| Layer | Where | Examples |
|-------|--------|----------|
| App role | `users.role` | `admin`, `user` |
| Project role | `project_members.role` | `manager`, `member`, `viewer` |

| Task | Notes |
|------|--------|
| [x] `app/services/project_visibility.py` | `can_view_project`, `can_edit_project`, list filtering |
| [x] Enforce on project routes | Visibility-aware list/get/update/delete |
| [x] `projects.visibility` + whitelist grants | `GET/POST/DELETE /api/projects/{id}/visibility-grants` |
| [ ] Enforce visibility on task/member routes | Extend checks to nested resources |
| [ ] Admin UI for app roles | Assign roles; add/remove project members |

**Definition of done:** User A cannot read or mutate User B’s private project via API.

### Phase 3 — Configurable values (no code deploy for statuses)

**Goal:** Admins change statuses and priorities without shipping new code.

| Task | Notes |
|------|--------|
| `lookup_categories` + `lookup_values` tables | e.g. `task_status`, `project_status`, `task_priority` |
| Seed default values on migration | `todo`, `in_progress`, `done`, etc. |
| Validate status/priority on create/update | Services reject unknown keys |
| Admin UI for lookups | Settings or dedicated admin page |
| Optional per-project overrides | Defer if global lookups are enough for v1 |

**Defer:** Arbitrary custom fields (JSON) until lookups prove insufficient.

### Phase 4 — Core PM UI (vertical slices)

Build one feature end-to-end at a time (types → service → page). Copy the **projects** slice as the pattern.

| Sprint | Frontend | Backend |
|--------|----------|---------|
| 4a | Project detail page | Single project + related data endpoint or parallel fetches |
| 4b | Tasks tab (list, create, assignee) | Task CRUD already exists; wire UI |
| 4c | Members tab | Project member CRUD + role checks |
| 4d | Comments + status updates | Thread or flat comments; latest status on project header |
| 4e | Departments / teams browser | List depts, teams, link users |
| 4f | Goals UI | Hierarchy list; link to departments |

**UX:** Collapsible sidebar when nav grows (template todo); keep using `components/ui` primitives.

### Phase 5 — Near-production hardening

| Area | Tasks |
|------|--------|
| Security | [Security-Review](.agents/skills/Security-Review/SKILL.md): CORS, HTTPS, secrets, rate limits |
| Migrations | Alembic in CI; documented rollback; no manual prod SQL |
| Tests | pytest: login, 401/403, lookup validation, project list filters |
| Observability | Structured logging, health endpoint |
| Deploy | Full Docker stack on Linux VM; PG backups; [Pre-Deploy-Check](.agents/skills/Pre-Deploy-Check/SKILL.md) |
| Docs | AD setup guide, roles matrix, “add a new entity” checklist |

### Suggested priority order

1. Phase 0 polish (profile, settings auth, model cleanup)
2. Phase 2 permissions (before building lots of UI that assumes open access)
3. Phase 3 lookup tables (before task board depends on fixed status strings)
4. Phase 4 project detail + tasks UI
5. Phase 1 Entra ID (when ready for Town SSO)
6. Phase 5 hardening before internal rollout

### Explicitly out of scope (for now)

- External integrations (Asana, GLPI, email) — `source_type` / `source_external_id` on tasks/goals are placeholders
- Full custom fields engine
- Public / citizen-facing access
- Reintroducing permit or other template demo domains

### Team workflow reminders

- One entity per PR when possible: model + schema + service + route + `frontend/src/types` + `frontend/src/services` + page slice
- Business rules only in `app/services/`; keep route handlers thin
- Every model change gets an Alembic revision
- No raw `fetch` in pages — use `frontend/src/services/*`
- Do not duplicate Peak-Pincer patterns (monolith routes, IP auth bypass, runtime string migrations) — see `og_codebase_review.md` as anti-patterns
