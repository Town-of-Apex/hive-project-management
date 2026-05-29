/**
 * services/taskService.ts
 */

import { del, get, post, put } from "@/services/api"
import type { Task, TaskCreateData, TaskListParams, TaskUpdateData } from "@/types/task"

function buildQuery(params: TaskListParams): string {
  const searchParams = new URLSearchParams()
  if (params.project_id != null) {
    searchParams.set("project_id", String(params.project_id))
  }
  if (params.status) searchParams.set("status", params.status)
  if (params.assignee_user_id != null) {
    searchParams.set("assignee_user_id", String(params.assignee_user_id))
  }
  if (params.search) searchParams.set("search", params.search)
  const qs = searchParams.toString()
  return qs ? `?${qs}` : ""
}

export async function getAll(params: TaskListParams = {}): Promise<Task[]> {
  return get<Task[]>(`/api/tasks${buildQuery(params)}`)
}

export async function getById(id: number): Promise<Task> {
  return get<Task>(`/api/tasks/${id}`)
}

export async function create(data: TaskCreateData): Promise<Task> {
  return post<Task>("/api/tasks", data)
}

export async function update(id: number, data: TaskUpdateData): Promise<Task> {
  return put<Task>(`/api/tasks/${id}`, data)
}

export async function remove(id: number): Promise<{ deleted: boolean; id: number }> {
  return del<{ deleted: boolean; id: number }>(`/api/tasks/${id}`)
}
