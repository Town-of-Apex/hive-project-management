# Template app recommended additions

This document tracks UI primitives, patterns, and backend conventions introduced in product apps that should be considered for inclusion in the Apex template starter. Add entries here when shipping reusable building blocks so the template team can promote them upstream.

---

## UI components (`frontend/src/components/ui`)

### Sheet (`Sheet.tsx`)

**Why:** Side panels for in-context detail views (task drill-in, record preview, activity feeds) without leaving the workspace route.

**Includes:** `Sheet`, `SheetContent`, `SheetHeader`, `SheetTitle`, `SheetBody`, `SheetFooter`, `SheetTrigger`, `SheetClose`

**Built on:** `@radix-ui/react-dialog` (same dependency as `Dialog.tsx`)

**When to use:** Detail views that need more space than a center modal but should keep the parent page visible. Pair with URL query params (e.g. `?task=123`) for shareable deep links.

---

## Feature patterns

### URL-synced workspace overlays (`useProjectWorkspace`)

**Why:** View-agnostic orchestration for overlays (detail panel + create dialog) that future views (board, calendar) can reuse without duplicating state.

**Location:** `frontend/src/features/project-detail/hooks/useProjectWorkspace.ts`

**Exports:** `openTask(id)`, `closeTask()`, `openNewTask({ parentTaskId?, defaultStatus? })`, URL sync via `?task=`

### View-agnostic task create dialog (`TaskFormDialog`)

**Why:** Single create/subtask entry point callable from table footer, header button, row menu, detail panel, or future kanban cards.

**Fields:** title, description, status, priority, assignee (project members only), due date, optional `parent_task_id`

### Task detail side panel (`TaskDetailPanel`)

**Why:** Full edit surface with subtask list, parent breadcrumb, save/delete, and read-only mode for viewers.

### Assignee picker scoped to project (`TaskAssigneeSelect`)

**Why:** Restricts assignment to project owner + members, matching backend validation.

### Confirm delete dialog (`TaskDeleteConfirmDialog`)

**Why:** Standardized destructive confirmation for tasks (reuses Dialog primitive pattern from `ComponentsPage`).

---

## Backend conventions

### Task service authorization (`app/services/task_service.py`)

**Why:** Task CRUD must enforce project visibility and edit rights; generic `BaseService` alone is insufficient.

**Includes:**

- `require_project_view` / `require_project_edit` on all task operations
- `list_for_user` scoped to visible projects when no `project_id` filter
- Parent task same-project validation
- Assignee must be owner or project member
- `created_by_user_id` defaulted from JWT when omitted
- `completed_at` set/cleared when status moves to/from `done`

### Integration tests against PostgreSQL (`tests/conftest.py`)

**Why:** Match production database behavior; use transaction rollback per test rather than SQLite.

**Requires:** PostgreSQL available (e.g. `docker compose up apex-db -d`) and migrations applied (`uv run alembic upgrade head`).

### Project member authorization (`app/services/project_member_service.py`)

**Why:** Member routes previously had no auth; list/create/update/delete now require project view or edit.

---

## Types and services

### Extended task client (`taskService.ts`)

Add to template: `getById`, `update`, `remove`, plus `TaskUpdateData` and `TaskFormValues` in `types/task.ts`.

---

*Add new sections as reusable patterns ship in product apps.*
