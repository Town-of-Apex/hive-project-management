/**
 * types/projectMember.ts
 */

import type { ProjectMemberRole } from "@/types/project"

export interface ProjectMember {
  id: number
  project_id: number
  user_id: number
  role: ProjectMemberRole | string
  created_at: string
  updated_at: string
}

export interface ProjectMemberListParams {
  project_id?: number
  user_id?: number
}
