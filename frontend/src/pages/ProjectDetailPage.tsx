/**
 * pages/ProjectDetailPage.tsx
 *
 * Project workspace: metadata, members, and task views (table v1).
 */

import { useCallback, useEffect, useMemo } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { toast } from "sonner"

import { PageContainer } from "@/components/layout/PageContainer"
import { Divider } from "@/components/shared/Divider"
import { Card } from "@/components/ui/Card"
import { ProjectDetailBreadcrumb } from "@/features/project-detail/components/ProjectDetailBreadcrumb"
import { ProjectDetailHeader } from "@/features/project-detail/components/ProjectDetailHeader"
import {
  ProjectDetailErrorView,
  resolveProjectDetailErrorKind,
} from "@/features/project-detail/components/ProjectDetailErrorView"
import { ProjectMembersPanel } from "@/features/project-detail/components/ProjectMembersPanel"
import { ProjectViewToolbar } from "@/features/project-detail/components/ProjectViewToolbar"
import { ProjectTaskTableView } from "@/features/project-detail/components/ProjectTaskTableView"
import { TaskDetailPanel } from "@/features/project-detail/components/TaskDetailPanel"
import { TaskFormDialog } from "@/features/project-detail/components/TaskFormDialog"
import { useProjectDetail } from "@/features/project-detail/hooks/useProjectDetail"
import { useProjectWorkspace } from "@/features/project-detail/hooks/useProjectWorkspace"
import type { ProjectFormData } from "@/types/project"
import type { TaskFormValues } from "@/types/task"

function formatDueDate(value: string | null): string | null {
  if (!value) return null
  return `${value}T00:00:00`
}

export function ProjectDetailPage() {
  const { projectId: projectIdParam } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const projectId = useMemo(() => {
    const id = Number(projectIdParam)
    return Number.isFinite(id) ? id : null
  }, [projectIdParam])

  const {
    project,
    tasks,
    members,
    usersById,
    loading,
    error,
    errorStatus,
    updateProject,
    createTask,
    updateTask,
    deleteTask,
  } = useProjectDetail(projectId)

  const {
    selectedTaskId,
    openTask,
    closeTask,
    newTaskOpen,
    newTaskOptions,
    openNewTask,
    closeNewTask,
  } = useProjectWorkspace()

  const selectedTask = useMemo(
    () => (selectedTaskId != null ? tasks.find((task) => task.id === selectedTaskId) ?? null : null),
    [selectedTaskId, tasks]
  )

  const parentTaskForDialog = useMemo(() => {
    if (newTaskOptions.parentTaskId == null) return null
    return tasks.find((task) => task.id === newTaskOptions.parentTaskId) ?? null
  }, [newTaskOptions.parentTaskId, tasks])

  const handleSaveProject = async (data: Partial<ProjectFormData>) => {
    try {
      await updateProject(data)
      toast.success("Project updated")
    } catch (err) {
      toast.error("Failed to update project", { description: String(err) })
      throw err
    }
  }

  const handleCreateTask = useCallback(
    async (values: TaskFormValues & { parent_task_id?: number | null }) => {
      const created = await createTask({
        title: values.title,
        description: values.description || null,
        status: values.status,
        priority: values.priority,
        assignee_user_id: values.assignee_user_id,
        parent_task_id: values.parent_task_id ?? null,
        due_date: formatDueDate(values.due_date),
      })
      openTask(created.id)
      return created
    },
    [createTask, openTask]
  )

  const handleUpdateTask = useCallback(
    async (taskId: number, values: TaskFormValues) => {
      return updateTask(taskId, {
        title: values.title,
        description: values.description || null,
        status: values.status,
        priority: values.priority,
        assignee_user_id: values.assignee_user_id,
        due_date: formatDueDate(values.due_date),
      })
    },
    [updateTask]
  )

  const handleDeleteTask = useCallback(
    async (taskId: number) => {
      await deleteTask(taskId)
      if (selectedTaskId === taskId) closeTask()
    },
    [deleteTask, selectedTaskId, closeTask]
  )

  // Clear stale ?task= when the ID is not in the loaded project
  useEffect(() => {
    if (loading || selectedTaskId == null) return
    if (tasks.some((task) => task.id === selectedTaskId)) return
    closeTask()
    toast.error("Task not found", { description: "That task is not part of this project." })
  }, [loading, selectedTaskId, tasks, closeTask])

  if (projectId == null) {
    return (
      <PageContainer>
        <ProjectDetailErrorView
          kind="invalid_id"
          onBack={() => navigate("/projects")}
        />
      </PageContainer>
    )
  }

  if (loading) {
    return (
      <PageContainer>
        <p style={{ color: "var(--text-muted)", padding: "var(--space-10) 0" }}>Loading project…</p>
      </PageContainer>
    )
  }

  if (error || !project) {
    return (
      <PageContainer>
        <ProjectDetailErrorView
          kind={resolveProjectDetailErrorKind(errorStatus, Boolean(error))}
          message={error}
          onBack={() => navigate("/projects")}
        />
      </PageContainer>
    )
  }

  return (
    <PageContainer>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-8)",
        }}
      >
        <ProjectDetailBreadcrumb projectName={project.name} />

        <div className="grid grid-cols-1 gap-[var(--space-8)] lg:grid-cols-[minmax(0,1fr)_280px] lg:items-start">
          <ProjectDetailHeader project={project} onSave={handleSaveProject} />
          <Card style={{ padding: "var(--space-5)" }}>
            <ProjectMembersPanel
              members={members}
              usersById={usersById}
              ownerUserId={project.owner_user_id}
            />
          </Card>
        </div>

        <Divider />

        <ProjectViewToolbar activeView="table" />

        <ProjectTaskTableView
          tasks={tasks}
          usersById={usersById}
          selectedTaskId={selectedTaskId}
          canEdit={project.can_edit}
          onOpenTask={openTask}
          onNewTask={() => openNewTask()}
          onAddSubtask={(parentTaskId) => {
            const parent = tasks.find((task) => task.id === parentTaskId)
            openNewTask({ parentTaskId, defaultStatus: parent?.status ?? "todo" })
          }}
          onDeleteTask={handleDeleteTask}
        />
      </div>

      <TaskDetailPanel
        open={selectedTaskId != null}
        onOpenChange={(open) => {
          if (!open) closeTask()
        }}
        task={selectedTask}
        tasks={tasks}
        canEdit={project.can_edit}
        ownerUserId={project.owner_user_id}
        members={members}
        usersById={usersById}
        onSave={handleUpdateTask}
        onDelete={handleDeleteTask}
        onOpenTask={openTask}
        onAddSubtask={(parentTaskId) => {
          const parent = tasks.find((task) => task.id === parentTaskId)
          openNewTask({ parentTaskId, defaultStatus: parent?.status ?? "todo" })
        }}
      />

      <TaskFormDialog
        open={newTaskOpen}
        onOpenChange={(open) => {
          if (open) return
          closeNewTask()
        }}
        canEdit={project.can_edit}
        ownerUserId={project.owner_user_id}
        members={members}
        usersById={usersById}
        options={newTaskOptions}
        parentTaskTitle={parentTaskForDialog?.title ?? null}
        onSubmit={handleCreateTask}
      />
    </PageContainer>
  )
}
