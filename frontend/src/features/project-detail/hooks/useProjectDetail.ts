/**
 * hooks/useProjectDetail.ts
 *
 * Loads project workspace data for the detail page.
 */

import { useCallback, useEffect, useState } from "react"

import { useAuth } from "@/contexts/AuthContext"
import { ApiRequestError } from "@/types/api"
import * as projectService from "@/services/projectService"
import * as projectMemberService from "@/services/projectMemberService"
import * as taskService from "@/services/taskService"
import { dbService } from "@/services/dbService"
import type { ProjectDetail, ProjectFormData } from "@/types/project"
import type { ProjectMember } from "@/types/projectMember"
import type { Task } from "@/types/task"
import type { User } from "@/types/db"

export interface UseProjectDetailResult {
  project: ProjectDetail | null
  tasks: Task[]
  members: ProjectMember[]
  usersById: Record<number, User>
  loading: boolean
  error: string | null
  errorStatus: number | null
  reload: () => Promise<void>
  updateProject: (data: Partial<ProjectFormData>) => Promise<ProjectDetail>
  addTask: (title: string, status?: string) => Promise<Task>
}

export function useProjectDetail(projectId: number | null): UseProjectDetailResult {
  const { user } = useAuth()
  const [project, setProject] = useState<ProjectDetail | null>(null)
  const [tasks, setTasks] = useState<Task[]>([])
  const [members, setMembers] = useState<ProjectMember[]>([])
  const [usersById, setUsersById] = useState<Record<number, User>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [errorStatus, setErrorStatus] = useState<number | null>(null)

  const reload = useCallback(async () => {
    if (projectId == null || Number.isNaN(projectId)) {
      setError("Invalid project.")
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)
    setErrorStatus(null)
    try {
      const [projectData, taskData, memberData, users] = await Promise.all([
        projectService.getById(projectId),
        taskService.getAll({ project_id: projectId }),
        projectMemberService.getAll({ project_id: projectId }),
        dbService.getUserDirectory(),
      ])
      setProject(projectData)
      setTasks(taskData)
      setMembers(memberData)
      const map: Record<number, User> = {}
      for (const u of users) map[u.id] = u
      setUsersById(map)
    } catch (err) {
      if (err instanceof ApiRequestError) {
        setError(err.message)
        setErrorStatus(err.status)
      } else {
        setError(String(err))
        setErrorStatus(null)
      }
      setProject(null)
      setTasks([])
      setMembers([])
    } finally {
      setLoading(false)
    }
  }, [projectId])

  useEffect(() => {
    void reload()
  }, [reload])

  const updateProject = useCallback(
    async (data: Partial<ProjectFormData>) => {
      if (projectId == null) throw new Error("Invalid project.")
      const updated = await projectService.update(projectId, data)
      setProject(updated)
      return updated
    },
    [projectId]
  )

  const addTask = useCallback(
    async (title: string, status = "todo") => {
      if (projectId == null) throw new Error("Invalid project.")
      if (!project?.can_edit) throw new Error("You do not have permission to add tasks.")
      if (!user) throw new Error("You must be signed in to add tasks.")
      const created = await taskService.create({
        project_id: projectId,
        title,
        status,
        priority: "medium",
        created_by_user_id: user.id,
      })
      setTasks((prev) => [...prev, created])
      return created
    },
    [projectId, project, user]
  )

  return {
    project,
    tasks,
    members,
    usersById,
    loading,
    error,
    errorStatus,
    reload,
    updateProject,
    addTask,
  }
}
