/**
 * Default table view: tasks grouped by status with indented subtasks.
 */

import { Fragment, useMemo, useState } from "react"
import { ChevronDown, ChevronRight, MoreHorizontal, Plus } from "lucide-react"
import { toast } from "sonner"

import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/DropdownMenu"
import { TaskDeleteConfirmDialog } from "@/features/project-detail/components/TaskDeleteConfirmDialog"
import { buildTaskStatusGroups } from "@/features/project-detail/utils/taskTableRows"
import type { Task } from "@/types/task"
import type { User } from "@/types/db"

interface ProjectTaskTableViewProps {
  tasks: Task[]
  usersById: Record<number, User>
  selectedTaskId?: number | null
  canEdit: boolean
  onOpenTask: (taskId: number) => void
  onNewTask: () => void
  onAddSubtask: (parentTaskId: number) => void
  onDeleteTask: (taskId: number) => Promise<void>
}

const priorityLabels: Record<string, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
}

const cellPadding = "var(--space-4) var(--space-6)"

export function ProjectTaskTableView({
  tasks,
  usersById,
  selectedTaskId = null,
  canEdit,
  onOpenTask,
  onNewTask,
  onAddSubtask,
  onDeleteTask,
}: ProjectTaskTableViewProps) {
  const groups = useMemo(() => buildTaskStatusGroups(tasks), [tasks])
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(() => new Set())
  const [deleteTarget, setDeleteTarget] = useState<Task | null>(null)
  const [deleting, setDeleting] = useState(false)

  const toggleGroup = (status: string) => {
    setCollapsedGroups((prev) => {
      const next = new Set(prev)
      if (next.has(status)) next.delete(status)
      else next.add(status)
      return next
    })
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    setDeleting(true)
    try {
      await onDeleteTask(deleteTarget.id)
      toast.success("Task deleted")
      setDeleteTarget(null)
    } catch (err) {
      toast.error("Failed to delete task", { description: String(err) })
    } finally {
      setDeleting(false)
    }
  }

  return (
    <section aria-labelledby="project-tasks-heading" style={{ display: "flex", flexDirection: "column", gap: "var(--space-6)" }}>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "var(--space-4)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-4)", flexWrap: "wrap" }}>
          <h2
            id="project-tasks-heading"
            style={{
              margin: 0,
              fontFamily: "var(--font-display)",
              fontSize: "1.25rem",
              fontWeight: 700,
            }}
          >
            Tasks
          </h2>
          <span style={{ fontSize: "0.875rem", color: "var(--text-muted)" }}>
            {tasks.length} {tasks.length === 1 ? "task" : "tasks"}
          </span>
        </div>
        {canEdit ? (
          <Button variant="primary" type="button" onClick={onNewTask}>
            <Plus className="w-4 h-4" />
            New task
          </Button>
        ) : null}
      </div>

      {groups.length === 0 ? (
        <Card style={{ padding: "var(--space-10)", textAlign: "center", color: "var(--text-muted)" }}>
          No tasks yet.{canEdit ? " Create one to get started." : ""}
          {canEdit ? (
            <div style={{ marginTop: "var(--space-4)" }}>
              <Button variant="primary" type="button" onClick={onNewTask}>
                <Plus className="w-4 h-4" />
                Add task
              </Button>
            </div>
          ) : null}
        </Card>
      ) : (
        <Card style={{ padding: 0, overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.875rem" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid var(--border-subtle)", background: "var(--bg-canvas)" }}>
                <th style={{ padding: cellPadding, textAlign: "left", fontWeight: 700, width: "40%" }}>Task</th>
                <th style={{ padding: cellPadding, textAlign: "left", fontWeight: 700 }}>Assignee</th>
                <th style={{ padding: cellPadding, textAlign: "left", fontWeight: 700 }}>Priority</th>
                <th style={{ padding: cellPadding, textAlign: "left", fontWeight: 700 }}>Due</th>
                {canEdit ? (
                  <th
                    style={{ padding: cellPadding, textAlign: "right", fontWeight: 700, width: "48px" }}
                    aria-label="Actions"
                  />
                ) : null}
              </tr>
            </thead>
            <tbody>
              {groups.map((group) => {
                const collapsed = collapsedGroups.has(group.status)
                return (
                  <Fragment key={group.status}>
                    <tr
                      style={{
                        borderBottom: "1px solid var(--border-subtle)",
                        background: "var(--bg-canvas)",
                      }}
                    >
                      <td colSpan={canEdit ? 5 : 4} style={{ padding: 0 }}>
                        <button
                          type="button"
                          onClick={() => toggleGroup(group.status)}
                          aria-expanded={!collapsed}
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "var(--space-2)",
                            width: "100%",
                            padding: "var(--space-3) var(--space-6)",
                            border: "none",
                            background: "transparent",
                            cursor: "pointer",
                            font: "inherit",
                            textAlign: "left",
                          }}
                        >
                          {collapsed ? (
                            <ChevronRight className="w-4 h-4" style={{ color: "var(--text-muted)" }} />
                          ) : (
                            <ChevronDown className="w-4 h-4" style={{ color: "var(--text-muted)" }} />
                          )}
                          <span
                            style={{
                              fontSize: "0.8125rem",
                              fontWeight: 700,
                              textTransform: "uppercase",
                              letterSpacing: "0.05em",
                              color: "var(--text-muted)",
                            }}
                          >
                            {group.label}
                          </span>
                          <span style={{ fontSize: "0.8125rem", fontWeight: 500, color: "var(--text-muted)" }}>
                            ({group.rows.length})
                          </span>
                        </button>
                      </td>
                    </tr>
                    {!collapsed &&
                      group.rows.map(({ task, depth }) => {
                        const assignee =
                          task.assignee_user_id != null ? usersById[task.assignee_user_id] : null
                        const isSelected = selectedTaskId === task.id
                        return (
                          <tr
                            key={task.id}
                            style={{
                              borderBottom: "1px solid var(--border-subtle)",
                              cursor: "pointer",
                              background: isSelected ? "var(--brand-primary-soft)" : undefined,
                            }}
                            onClick={() => onOpenTask(task.id)}
                            onKeyDown={(e) => {
                              if (e.key === "Enter" || e.key === " ") {
                                e.preventDefault()
                                onOpenTask(task.id)
                              }
                            }}
                            tabIndex={0}
                            aria-label={`Open task ${task.title}`}
                          >
                            <td style={{ padding: cellPadding }}>
                              <div
                                style={{
                                  paddingLeft: depth > 0 ? `calc(${depth} * var(--space-6))` : 0,
                                  fontWeight: depth === 0 ? 600 : 400,
                                }}
                              >
                                {task.title}
                              </div>
                            </td>
                            <td style={{ padding: cellPadding, color: "var(--text-muted)" }}>
                              {assignee?.full_name ?? "—"}
                            </td>
                            <td style={{ padding: cellPadding }}>
                              {priorityLabels[task.priority] ?? task.priority}
                            </td>
                            <td style={{ padding: cellPadding, color: "var(--text-muted)" }}>
                              {task.due_date ? new Date(task.due_date).toLocaleDateString() : "—"}
                            </td>
                            {canEdit ? (
                              <td style={{ padding: cellPadding, textAlign: "right" }}>
                                <DropdownMenu>
                                  <DropdownMenuTrigger asChild>
                                    <Button
                                      variant="ghost"
                                      size="icon"
                                      type="button"
                                      aria-label={`Actions for ${task.title}`}
                                      onClick={(e) => e.stopPropagation()}
                                    >
                                      <MoreHorizontal className="w-4 h-4" />
                                    </Button>
                                  </DropdownMenuTrigger>
                                  <DropdownMenuContent align="end" onClick={(e) => e.stopPropagation()}>
                                    <DropdownMenuItem onSelect={() => onOpenTask(task.id)}>
                                      Open
                                    </DropdownMenuItem>
                                    <DropdownMenuItem onSelect={() => onAddSubtask(task.id)}>
                                      Add subtask
                                    </DropdownMenuItem>
                                    <DropdownMenuSeparator />
                                    <DropdownMenuItem
                                      className="text-[var(--danger)]"
                                      onSelect={() => setDeleteTarget(task)}
                                    >
                                      Delete
                                    </DropdownMenuItem>
                                  </DropdownMenuContent>
                                </DropdownMenu>
                              </td>
                            ) : null}
                          </tr>
                        )
                      })}
                  </Fragment>
                )
              })}
            </tbody>
          </table>
          {canEdit ? (
            <div
              style={{
                borderTop: "1px solid var(--border-subtle)",
                padding: "var(--space-4) var(--space-6)",
                background: "var(--bg-canvas)",
              }}
            >
              <Button variant="ghost" type="button" onClick={onNewTask}>
                <Plus className="w-4 h-4" />
                Add task
              </Button>
            </div>
          ) : null}
        </Card>
      )}

      <TaskDeleteConfirmDialog
        open={deleteTarget != null}
        onOpenChange={(open) => {
          if (!open) setDeleteTarget(null)
        }}
        taskTitle={deleteTarget?.title ?? "this task"}
        loading={deleting}
        onConfirm={handleDelete}
      />
    </section>
  )
}
