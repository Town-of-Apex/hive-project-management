/**
 * services/projectService.ts
 */

import { get, post, put } from "@/services/api"
import type { Project, ProjectDetail, ProjectFormData, ProjectListParams } from "@/types/project"

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

export async function getById(id: number): Promise<ProjectDetail> {
  return get<ProjectDetail>(`/api/projects/${id}`)
}

export async function update(id: number, data: Partial<ProjectFormData>): Promise<ProjectDetail> {
  return put<ProjectDetail>(`/api/projects/${id}`, data)
}

export async function create(data: ProjectFormData): Promise<Project> {
  return post<Project>("/api/projects", data)
}
