# Project detail page — requirements and roadmap

This document describes the **project workspace** (detail page): what exists today, what we plan to build, open questions, and architectural decisions. It is the canonical reference for expanding `/projects/:projectId` beyond the initial table-view skeleton.

---

## 1. Product vision

The project detail page is the **central hub** for a single project—similar in spirit to an Asana project. Users land here after choosing a project from the list. The page stays **inside the application shell** (global header, footer, auth); only the main content area changes.

Long term, this page supports:

- Multiple **views** of the same task dataset (table, board/kanban, calendar, timeline/gantt, and user-defined views).
- **Project metadata** at the top (name, description, status, priority, visibility, members, settings).
- **Tasks** as the primary working surface, with filtering, sorting, grouping, and inline editing where permitted.
- **Collaboration** (members, invites, comments, status updates).
- **Configuration** (project settings, custom fields, integrations).

**v1 scope (implemented skeleton):**

| Area | v1 behavior |
|------|-------------|
| URL | `/projects/:projectId` (view switcher on same URL later) |
| Layout | `PageContainer` width; roomy vertical spacing |
| Project meta | Read + **Edit / Save / Cancel** when `can_edit` |
| Members | Read-only list (owner + `project_members`) |
| Views | Table only; toolbar shows disabled placeholders for Board, Calendar, Timeline |
| Tasks | Grouped-by-status table, indented subtasks, **New task** dialog when `can_edit` |
| Task detail | Side panel synced to `?task=<id>`; full edit for editors, read-only for viewers |
| Permissions | `can_edit` from `GET /api/projects/:id` |

---

## 2. Information architecture

### 2.1 Page regions (top → bottom)

```
┌─────────────────────────────────────────────────────────────┐
│ Breadcrumb: Projects › {Project name}                        │
├──────────────────────────────┬──────────────────────────────┤
│ Project header               │ Members (sidebar card)        │
│ • Title, description         │ • Owner                       │
│ • Status, priority, meta     │ • Members + roles             │
│ • Edit / Save / Cancel       │                               │
├──────────────────────────────┴──────────────────────────────┤
│ View toolbar: [Table] [Board*] [Calendar*] [Timeline*]     │
├─────────────────────────────────────────────────────────────┤
│ Active view content (tasks table in v1)                      │
└─────────────────────────────────────────────────────────────┘
* disabled until built
```

### 2.2 Future regions (not in v1)

- **Project settings** drawer or sub-route (`/projects/:id/settings`).
- **Activity / comments** strip or side panel.
- **Goals / milestones** linked to project.
- **Files / attachments** (if product needs them).
- **Custom fields** block in header or table columns.

### 2.3 Task detail UX (open)

| Option | Pros | Cons |
|--------|------|------|
| **Modal** | Stays in project context; fast open/close | Limited space; deep links harder |
| **Side panel** | Asana-like; room for fields + activity | Narrow on mobile |
| **Dedicated route** `/projects/:id/tasks/:taskId` | Shareable URLs; full page | Leaves “workspace” feel |

**Decision (Phase B):** **Side panel** (`TaskDetailPanel`) synced to URL query `?task=<id>`. New-task creation uses a view-agnostic **Dialog** (`TaskFormDialog`). Table rows are clickable.

---

## 3. Views

### 3.1 View model (target)

- A project has one or more **views**, each with:
  - `id`, `name`, `type` (`table` | `board` | `calendar` | `timeline` | `custom`)
  - **Layout config** (group by, sort, visible columns, filters)
  - Optional **personal vs project-default** scope (pin / save for me vs everyone)

**v1:** Single implicit “Table” view; `ProjectViewToolbar` + `ProjectViewId` type reserved for expansion.

**URL strategy (decided for v1):** `/projects/:projectId` only. Optional later: query `?view=board` or path segment `/projects/:id/board`—see §8.

### 3.2 Table view (v1 + planned)

**v1:**

- Group tasks by **status** (global default order: todo → in_progress → done; unknown statuses in extra groups).
- Within group: parent tasks then **indented subtasks** (one level of hierarchy displayed; deeper trees still render recursively).
- Columns: Task, Assignee, Priority, Due, Actions (when `can_edit`).
- Create task: **New task** button + footer action → `TaskFormDialog` (title, description, status, priority, assignee, due).
- Row click → `TaskDetailPanel`; URL updates to `?task=<id>`.

**Planned:**

| Feature | Description |
|---------|-------------|
| Column picker | Show/hide columns (description, created, subtask count, custom fields) |
| Sort | Per-column sort; multi-sort later |
| Filter | Status, assignee, priority, due range, search |
| Group by | Status (v1), then assignee, priority, section/custom field |
| Inline edit | Title, status, assignee, dates in row |
| Row actions | Open detail, duplicate, delete, add subtask |
| Bulk select | Multi-edit, bulk status change |
| Empty states | Per-group and whole-project |
| Density toggle | Compact / comfortable / spacious |

### 3.3 Board (kanban) view

- Columns = status (or custom field).
- Drag-and-drop status change.
- WIP limits (optional, advanced).
- Card fields: title, assignee, due, priority.

### 3.4 Calendar view

- Tasks with `due_date` (and optionally `start_date`) on month/week/day grids.
- Drag to reschedule.
- Unscheduled bucket.

### 3.5 Timeline / Gantt view

- Requires `start_date` + `due_date` (or inferred duration).
- Dependencies between tasks (not in schema yet).
- Zoom: week / month / quarter.

---

## 4. Actions catalog

Actions are grouped by actor permission (`can_edit` / role / admin). Implement gradually; ✅ = v1 or partial.

### 4.1 Project-level

| Action | v1 | Notes |
|--------|-----|------|
| View project | ✅ | 403 if not visible |
| Edit name, description, status, priority | ✅ | Edit mode toggle |
| Edit visibility | — | Field exists on model; UI later |
| Edit department / owner | — | Admin or policy TBD |
| Delete project | — | Confirm dialog; redirect to list |
| Duplicate project | — | |
| Archive / restore | — | May map to `status=archived` |
| Open project settings | — | |
| Star / favorite project | — | User preference table TBD |

### 4.2 Members and access

| Action | v1 | Notes |
|--------|-----|------|
| List members | ✅ | Read-only |
| Invite / add member | — | `POST /api/project_members` |
| Change member role | — | `PUT .../members/:id` |
| Remove member | — | |
| List visibility grants | — | Private projects |
| Grant / revoke whitelist access | — | Existing API on project |
| Transfer ownership | — | Policy + audit |

### 4.3 Tasks (in workspace)

| Action | v1 | Notes |
|--------|-----|------|
| List tasks for project | ✅ | |
| Create task | ✅ | `TaskFormDialog`; defaults status `todo` |
| View task detail | ✅ | Side panel + `?task=` URL |
| Edit task fields inline | — | Edit in side panel (table inline deferred) |
| Delete task | ✅ | Confirm dialog; row menu + panel |
| Create subtask | ✅ | Dialog with `parent_task_id`; row menu + panel |
| Reorder tasks | — | Needs `sort_order` or rank column |
| Assign / reassign | ✅ | Create dialog + detail panel |
| Set dates | ✅ | Due date in create dialog + detail panel |
| Comment on task | — | `comments` API exists |
| Attach files | — | Not in schema |

### 4.4 Views and display

| Action | v1 | Notes |
|--------|-----|------|
| Switch view | Partial | Toolbar UI only |
| Save view configuration | — | |
| Pin personal view | — | |
| Export (CSV) | — | |

### 4.5 Collaboration

| Action | v1 | Notes |
|--------|-----|------|
| Post project status update | — | `status_updates` API |
| List status updates | — | |
| Project-level comments | — | `comments?project_id=` |

---

## 5. Permissions and security

### 5.1 Current backend rules

- **View project:** visibility mode + membership + grants + admin.
- **Edit project:** admin, owner, or member with role `manager` | `member` (`viewer` cannot edit).
- **`can_edit` on `GET/PUT /api/projects/:id`:** returned to drive UI (v1).

### 5.2 Gaps (must address before production)

| Gap | Risk | Recommendation |
|-----|------|----------------|
| Task routes lack project visibility checks | ~~IDOR~~ | ✅ Addressed in Phase B (`task_service` + route auth) |
| `project_members` routes lack auth | ~~Anyone can add/remove members~~ | ✅ Addressed in Phase B (`project_member_service`) |
| Task edit permission vs project edit | Viewers might edit tasks if task API stays open | Define `can_edit_tasks` (may differ from project metadata) |
| No `can_edit` on list endpoint | List page cannot dim actions per row | Optional `can_edit` on `ProjectRead` for list |

### 5.3 Frontend permission patterns (target)

- Use `project.can_edit` for project metadata and add-task (v1).
- Introduce `useProjectCapabilities(projectId)` hook when API exposes richer flags.
- Disable controls vs hide vs optimistic UI—prefer **disabled + tooltip** for discoverability.

---

## 6. Data and API

### 6.1 v1 API usage

| Data | Endpoint |
|------|----------|
| Project + `can_edit` | `GET /api/projects/:id` |
| Update project | `PUT /api/projects/:id` |
| Tasks | `GET /api/tasks?project_id=` |
| Create task | `POST /api/tasks` (`created_by_user_id` optional; defaults from JWT) |
| Update / delete task | `PUT/DELETE /api/tasks/:id` |
| Members | `GET /api/project_members?project_id=` |
| User names | `GET /api/users` |

### 6.2 Recommended aggregate endpoints (future)

Reduce round-trips and N+1 name resolution:

```
GET /api/projects/:id/workspace
  → project, can_edit, members (+ user summaries), task summary counts, default view config

GET /api/projects/:id/tasks?include=assignee,creator,subtask_count
```

### 6.3 Task status model

**v1:** Global statuses in `frontend/src/features/project-detail/constants/taskStatuses.ts`.

**Target:** Per-project status workflow (columns for board, group order for table).

| Decision | Options |
|----------|---------|
| Storage | JSON on project vs `project_status` table |
| System defaults | Seed todo / in_progress / done for new projects |
| Migration | Map existing free-form strings |

### 6.4 Custom fields

Not in schema. Typical approach:

- `custom_field_definitions` (project or workspace scope)
- `custom_field_values` (entity_type=task, entity_id)
- Table/board views read definitions to build columns

---

## 7. Frontend architecture

### 7.1 v1 module layout

```
frontend/src/
  pages/ProjectDetailPage.tsx          # Route entry; composes feature
  features/project-detail/
    constants/taskStatuses.ts          # Global statuses (swap for per-project later)
    hooks/useProjectDetail.ts          # Data loading + task mutations
    hooks/useProjectWorkspace.ts       # URL-synced panel + new-task dialog
    utils/taskTableRows.ts             # Grouping / tree ordering
    components/
      ProjectDetailBreadcrumb.tsx
      ProjectDetailHeader.tsx
      ProjectMembersPanel.tsx
      ProjectViewToolbar.tsx           # View switcher (extensible)
      ProjectTaskTableView.tsx
      TaskDetailPanel.tsx              # Side panel (?task=)
      TaskFormDialog.tsx               # View-agnostic create/subtask
      TaskAssigneeSelect.tsx
      TaskDeleteConfirmDialog.tsx
```

### 7.2 Extension guidelines

1. **New views:** Add `components/views/BoardView.tsx`, register in a `PROJECT_VIEWS` map keyed by `ProjectViewId`, render from `ProjectDetailPage` by active view state.
2. **View state:** Prefer URL search params (`?view=table`) or React context `ProjectWorkspaceProvider` when many siblings need tasks + filters.
3. **Filters/sorts:** Store in context or URL; pass derived `tasks` into view components—do not fetch per view.
4. **Keep pages thin:** `ProjectDetailPage` orchestrates; business logic in hooks/utils.
5. **Services:** One service module per API resource; extend `taskService` / `projectMemberService` as features land.

### 7.3 Styling

- Continue **CSS variables + inline layout** on page/feature components to match Apex template pages.
- Use **shadcn/ui primitives** for interactive controls.
- Spacing: prefer `var(--space-6)`–`var(--space-8)` between major sections for an open feel.

---

## 8. Open questions and decisions

| # | Topic | Question | Options / notes |
|---|--------|----------|------------------|
| 1 | Task detail UX | Modal, side panel, or route? | **Side panel + `?task=`** (Phase B) |
| 2 | View in URL | Same URL vs `?view=` vs `/projects/:id/:view` | v1: same URL; query param lowest friction for switcher |
| 3 | Task vs project edit rights | Can a `viewer` comment or edit assigned tasks only? | Common pattern: viewer = read-only everything |
| 4 | Add task default status | Always `todo` vs remember last vs per-group add | v1: `todo` |
| 5 | Subtask creation | Inline under parent vs only from task detail | Dialog from row menu + detail panel |
| 6 | Departments | Show department name on project header? | `department_id` on project |
| 7 | Notifications | In-app/email on assign, mention, due? | Out of scope until events exist |
| 8 | Realtime | WebSocket for board moves vs poll | |
| 9 | Personal “My tasks” | Cross-project list vs project-only | |
| 10 | Archived projects | Read-only workspace or hidden tasks? | |
| 11 | Mobile | Collapse members to accordion? Simplified table? | |
| 12 | `created_by_user_id` on task create | Should API default from JWT? | ✅ Backend defaults from JWT when omitted |

---

## 9. Phased roadmap (suggested)

### Phase A — Foundation (current)

- [x] Route, breadcrumb, list navigation
- [x] Project header with edit mode + `can_edit`
- [x] Members read-only
- [x] Table view grouped by status, subtask indent
- [x] Add task
- [x] View toolbar placeholders

### Phase B — Task workflow

- [x] Task row click → detail side panel + `?task=` URL
- [ ] Inline edit title, status, assignee, due (in table rows)
- [x] Create subtask from row menu + detail panel
- [x] Delete task with confirm
- [x] Secure task APIs with project permissions
- [ ] `can_edit_tasks` if different from project edit (uses `can_edit` for now)

### Phase C — Table power features

- [ ] Filter, sort, search
- [ ] Column visibility
- [ ] Bulk actions

### Phase D — Alternate views

- [ ] Board + drag status
- [ ] Calendar
- [ ] Timeline / gantt (needs dependencies schema?)

### Phase E — Collaboration and config

- [ ] Member invite / role management UI
- [ ] Visibility grants UI
- [ ] Status updates feed
- [ ] Project settings + custom fields
- [ ] Saved views / pins

---

## 10. Acceptance criteria (v1 skeleton)

- [ ] From `/projects`, clicking a row opens `/projects/:id` inside app shell.
- [ ] Project name, description, status, priority visible; Edit works when user has edit rights.
- [ ] Members panel shows owner and members with roles.
- [ ] Tasks appear in status groups; subtasks indented under parent.
- [ ] User with `can_edit` can add a task; viewer cannot.
- [ ] Board/Calendar/Timeline tabs visible but disabled with clear “coming soon” behavior.
- [ ] `GET /api/projects/:id` includes `can_edit: boolean`.
- [ ] Invalid or inaccessible project shows error and back navigation.

---

## 11. Related files

| Layer | Path |
|-------|------|
| Page | `frontend/src/pages/ProjectDetailPage.tsx` |
| Feature module | `frontend/src/features/project-detail/` |
| API routes | `app/api/routes/projects.py`, `tasks.py`, `project_members.py` |
| Visibility | `app/services/project_visibility.py` |
| UI | `frontend/src/components/ui/Sheet.tsx` |
| Tests | `tests/test_tasks_permissions.py`, `tests/test_project_members_permissions.py` |
| Template notes | `docs/template_app_recommended_additions.md` |

---

*Last updated: Phase B task workflow (side panel, dialog create, secured APIs) — May 2026.*
