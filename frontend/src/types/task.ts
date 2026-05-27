/**
 * types/task.ts
 */

export interface Task {
  id: number
  project_id: number
  title: string
  status: string
  priority: string
  created_at: string
  updated_at: string
}

export interface TaskListParams {
  project_id?: number
}
