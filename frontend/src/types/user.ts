/**
 * types/user.ts
 */

export interface User {
  id: number
  username: string
  full_name: string
  email: string | null
  role: string
  department: string | null
  is_active: boolean
  team_id: number | null
  created_at: string
  updated_at: string
}
