/**
 * types/user.ts
 */

export type UserRole = "admin" | "user"

export interface User {
  id: number
  username: string
  full_name: string
  email: string | null
  role: UserRole | string
  department_id: number | null
  department_name?: string | null
  is_active: boolean
  team_id: number | null
  created_at: string
  updated_at: string
}
