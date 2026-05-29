/**
 * types/task.ts
 */

export type TaskStatus = "todo" | "in_progress" | "done" | (string & {})
export type TaskPriority = "low" | "medium" | "high"

export interface Task {
  id: number
  project_id: number
  parent_task_id: number | null
  assignee_user_id: number | null
  created_by_user_id: number
  title: string
  description: string | null
  status: string
  priority: string
  start_date: string | null
  due_date: string | null
  completed_at: string | null
  source_type: string | null
  source_external_id: string | null
  created_at: string
  updated_at: string
}

export interface TaskListParams {
  project_id?: number
  status?: string
  assignee_user_id?: number
  search?: string
}

export interface TaskCreateData {
  project_id: number
  title: string
  status?: string
  priority?: string
  parent_task_id?: number | null
  assignee_user_id?: number | null
  created_by_user_id?: number
  description?: string | null
  due_date?: string | null
}

export interface TaskUpdateData {
  title?: string
  description?: string | null
  status?: string
  priority?: string
  parent_task_id?: number | null
  assignee_user_id?: number | null
  due_date?: string | null
}

export interface TaskFormValues {
  title: string
  description: string
  status: string
  priority: string
  assignee_user_id: number | null
  due_date: string
}

export interface NewTaskOptions {
  parentTaskId?: number | null
  defaultStatus?: string
}
