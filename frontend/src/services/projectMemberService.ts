/**
 * services/projectMemberService.ts
 */

import { get } from "@/services/api"
import type { ProjectMember, ProjectMemberListParams } from "@/types/projectMember"

function buildQuery(params: ProjectMemberListParams): string {
  const searchParams = new URLSearchParams()
  if (params.project_id != null) {
    searchParams.set("project_id", String(params.project_id))
  }
  if (params.user_id != null) {
    searchParams.set("user_id", String(params.user_id))
  }
  const qs = searchParams.toString()
  return qs ? `?${qs}` : ""
}

export async function getAll(params: ProjectMemberListParams = {}): Promise<ProjectMember[]> {
  return get<ProjectMember[]>(`/api/project_members${buildQuery(params)}`)
}
