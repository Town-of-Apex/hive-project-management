/**
 * Default task status definitions for table grouping.
 *
 * v1 uses a global ordered set; per-project custom statuses will plug in here later.
 */

export interface TaskStatusDefinition {
  id: string
  label: string
}

/** Default workflow order for grouping (global until per-project statuses exist). */
export const DEFAULT_TASK_STATUSES: TaskStatusDefinition[] = [
  { id: "todo", label: "To do" },
  { id: "in_progress", label: "In progress" },
  { id: "done", label: "Done" },
]

export function labelForTaskStatus(status: string): string {
  const known = DEFAULT_TASK_STATUSES.find((s) => s.id === status)
  if (known) return known.label
  return status.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
}

export function sortIndexForTaskStatus(status: string): number {
  const idx = DEFAULT_TASK_STATUSES.findIndex((s) => s.id === status)
  return idx === -1 ? DEFAULT_TASK_STATUSES.length : idx
}
