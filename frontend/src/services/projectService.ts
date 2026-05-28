/**
 * services/projectService.ts
 */

import { get, post } from "@/services/api"
import type { Project, ProjectFormData, ProjectListParams } from "@/types/project"

function buildQuery(params: ProjectListParams): string {
  const searchParams = new URLSearchParams()
  if (params.search) searchParams.set("search", params.search)
  if (params.status) searchParams.set("status", params.status)
  if (params.department_id != null) searchParams.set("department_id", String(params.department_id))
  const qs = searchParams.toString()
  return qs ? `?${qs}` : ""
}

export async function getAll(params: ProjectListParams = {}): Promise<Project[]> {
  return get<Project[]>(`/api/projects${buildQuery(params)}`)
}

export async function getById(id: number): Promise<Project> {
  return get<Project>(`/api/projects/${id}`)
}

export async function create(data: ProjectFormData): Promise<Project> {
  return post<Project>("/api/projects", data)
}
