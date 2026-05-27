/**
 * services/taskService.ts
 */

import { get } from "@/services/api"
import type { Task, TaskListParams } from "@/types/task"

function buildQuery(params: TaskListParams): string {
  const searchParams = new URLSearchParams()
  if (params.project_id != null) {
    searchParams.set("project_id", String(params.project_id))
  }
  const qs = searchParams.toString()
  return qs ? `?${qs}` : ""
}

export async function getAll(params: TaskListParams = {}): Promise<Task[]> {
  return get<Task[]>(`/api/tasks${buildQuery(params)}`)
}
