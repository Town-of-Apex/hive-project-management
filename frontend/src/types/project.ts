/**
 * types/project.ts
 *
 * TypeScript contracts for the Project resource.
 */

export type ProjectStatus = "active" | "on_hold" | "completed" | "archived"
export type ProjectPriority = "low" | "medium" | "high"

export interface Project {
  id: number
  department_id: number | null
  owner_user_id: number | null
  name: string
  description: string | null
  status: string
  priority: string
  visibility: string
  created_at: string
  updated_at: string
}

export interface ProjectFormData {
  name: string
  description: string
  status: ProjectStatus
  priority: ProjectPriority
}

export type ProjectVisibility = "private" | "department" | "organization"
export type ProjectMemberRole = "manager" | "member" | "viewer"

export interface ProjectListParams {
  search?: string
  status?: string
  department_id?: number
}
