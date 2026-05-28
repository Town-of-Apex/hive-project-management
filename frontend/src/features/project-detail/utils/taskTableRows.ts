/**
 * utils/taskTableRows.ts
 *
 * Builds ordered table rows: status groups → parent tasks → indented subtasks.
 */

import type { Task } from "@/types/task"
import {
  DEFAULT_TASK_STATUSES,
  labelForTaskStatus,
  sortIndexForTaskStatus,
} from "@/features/project-detail/constants/taskStatuses"

export interface TaskTableRow {
  task: Task
  depth: number
}

export interface TaskStatusGroup {
  status: string
  label: string
  rows: TaskTableRow[]
}

function buildChildrenMap(tasks: Task[]): Map<number, Task[]> {
  const byParent = new Map<number, Task[]>()
  for (const task of tasks) {
    if (task.parent_task_id == null) continue
    const siblings = byParent.get(task.parent_task_id) ?? []
    siblings.push(task)
    byParent.set(task.parent_task_id, siblings)
  }
  for (const siblings of byParent.values()) {
    siblings.sort((a, b) => a.title.localeCompare(b.title))
  }
  return byParent
}

function appendWithChildren(
  task: Task,
  childrenByParent: Map<number, Task[]>,
  rows: TaskTableRow[],
  depth: number
): void {
  rows.push({ task, depth })
  const children = childrenByParent.get(task.id) ?? []
  for (const child of children) {
    appendWithChildren(child, childrenByParent, rows, depth + 1)
  }
}

function rowsForStatus(tasks: Task[], status: string): TaskTableRow[] {
  const inStatus = tasks.filter((t) => t.status === status)
  const childrenByParent = buildChildrenMap(inStatus)
  const topLevel = inStatus
    .filter((t) => t.parent_task_id == null || !inStatus.some((p) => p.id === t.parent_task_id))
    .sort((a, b) => a.title.localeCompare(b.title))

  const rows: TaskTableRow[] = []
  for (const task of topLevel) {
    appendWithChildren(task, childrenByParent, rows, 0)
  }
  return rows
}

/** Group tasks by status with hierarchical ordering within each group. */
export function buildTaskStatusGroups(tasks: Task[]): TaskStatusGroup[] {
  const statusIds = new Set(tasks.map((t) => t.status))
  const orderedStatuses: string[] = []

  for (const def of DEFAULT_TASK_STATUSES) {
    if (statusIds.has(def.id)) orderedStatuses.push(def.id)
  }

  const unknown = [...statusIds]
    .filter((s) => !DEFAULT_TASK_STATUSES.some((d) => d.id === s))
    .sort((a, b) => sortIndexForTaskStatus(a) - sortIndexForTaskStatus(b) || a.localeCompare(b))

  for (const s of unknown) {
    if (!orderedStatuses.includes(s)) orderedStatuses.push(s)
  }

  return orderedStatuses
    .map((status) => ({
      status,
      label: labelForTaskStatus(status),
      rows: rowsForStatus(tasks, status),
    }))
    .filter((g) => g.rows.length > 0)
}
