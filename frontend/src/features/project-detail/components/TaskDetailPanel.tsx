/**
 * URL-synced side panel for viewing and editing a task.
 */

import { useEffect, useMemo, useState } from "react"
import { Plus, Trash2 } from "lucide-react"
import { toast } from "sonner"

import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Label } from "@/components/ui/Label"
import { Select } from "@/components/ui/Select"
import {
  Sheet,
  SheetBody,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/Sheet"
import { Textarea } from "@/components/ui/Textarea"
import { TaskAssigneeSelect } from "@/features/project-detail/components/TaskAssigneeSelect"
import { TaskDeleteConfirmDialog } from "@/features/project-detail/components/TaskDeleteConfirmDialog"
import { DEFAULT_TASK_STATUSES } from "@/features/project-detail/constants/taskStatuses"
import type { ProjectMember } from "@/types/projectMember"
import type { Task, TaskFormValues } from "@/types/task"
import type { User } from "@/types/db"

const priorityOptions = [
  { id: "low", label: "Low" },
  { id: "medium", label: "Medium" },
  { id: "high", label: "High" },
]

function toDateInputValue(value: string | null): string {
  if (!value) return ""
  return value.slice(0, 10)
}

function taskToForm(task: Task): TaskFormValues {
  return {
    title: task.title,
    description: task.description ?? "",
    status: task.status,
    priority: task.priority,
    assignee_user_id: task.assignee_user_id,
    due_date: toDateInputValue(task.due_date),
  }
}

interface TaskDetailPanelProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  task: Task | null
  tasks: Task[]
  canEdit: boolean
  ownerUserId: number
  members: ProjectMember[]
  usersById: Record<number, User>
  onSave: (taskId: number, values: TaskFormValues) => Promise<Task>
  onDelete: (taskId: number) => Promise<void>
  onOpenTask: (taskId: number) => void
  onAddSubtask: (parentTaskId: number) => void
}

export function TaskDetailPanel({
  open,
  onOpenChange,
  task,
  tasks,
  canEdit,
  ownerUserId,
  members,
  usersById,
  onSave,
  onDelete,
  onOpenTask,
  onAddSubtask,
}: TaskDetailPanelProps) {
  const [draft, setDraft] = useState<TaskFormValues | null>(null)
  const [saving, setSaving] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    if (task) setDraft(taskToForm(task))
  }, [task])

  const parentTask = useMemo(() => {
    if (!task?.parent_task_id) return null
    return tasks.find((item) => item.id === task.parent_task_id) ?? null
  }, [task, tasks])

  const subtasks = useMemo(() => {
    if (!task) return []
    return tasks.filter((item) => item.parent_task_id === task.id)
  }, [task, tasks])

  const isDirty = useMemo(() => {
    if (!task || !draft) return false
    return JSON.stringify(draft) !== JSON.stringify(taskToForm(task))
  }, [task, draft])

  const handleSave = async () => {
    if (!task || !draft || !canEdit) return
    const trimmedTitle = draft.title.trim()
    if (!trimmedTitle) {
      toast.error("Title is required")
      return
    }
    setSaving(true)
    try {
      await onSave(task.id, { ...draft, title: trimmedTitle, description: draft.description.trim() })
      toast.success("Task updated")
    } catch (err) {
      toast.error("Failed to update task", { description: String(err) })
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!task || !canEdit) return
    setDeleting(true)
    try {
      await onDelete(task.id)
      toast.success("Task deleted")
      setDeleteOpen(false)
      onOpenChange(false)
    } catch (err) {
      toast.error("Failed to delete task", { description: String(err) })
    } finally {
      setDeleting(false)
    }
  }

  const handleOpenChange = (nextOpen: boolean) => {
    if (nextOpen) {
      onOpenChange(true)
      return
    }
    if (isDirty && canEdit) {
      const discard = window.confirm("Discard unsaved changes?")
      if (!discard) return
    }
    onOpenChange(false)
  }

  return (
    <>
      <Sheet open={open} onOpenChange={handleOpenChange}>
        <SheetContent aria-describedby={undefined}>
          <SheetHeader>
            <SheetTitle>{task ? "Task details" : "Task"}</SheetTitle>
            {task && !canEdit ? (
              <p style={{ margin: 0, fontSize: "0.8125rem", color: "var(--text-muted)" }}>
                View only — you do not have permission to edit this project.
              </p>
            ) : null}
            {parentTask ? (
              <button
                type="button"
                onClick={() => onOpenTask(parentTask.id)}
                style={{
                  margin: 0,
                  padding: 0,
                  border: "none",
                  background: "transparent",
                  color: "var(--brand-primary)",
                  font: "inherit",
                  fontSize: "0.875rem",
                  cursor: "pointer",
                  textAlign: "left",
                }}
              >
                Parent: {parentTask.title}
              </button>
            ) : null}
          </SheetHeader>

          {task && draft ? (
            <>
              <SheetBody>
                <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
                  <div>
                    <Label htmlFor="detail-task-title">Title</Label>
                    <Input
                      id="detail-task-title"
                      value={draft.title}
                      disabled={!canEdit || saving}
                      onChange={(e) => setDraft((prev) => (prev ? { ...prev, title: e.target.value } : prev))}
                    />
                  </div>
                  <div>
                    <Label htmlFor="detail-task-description">Description</Label>
                    <Textarea
                      id="detail-task-description"
                      rows={4}
                      value={draft.description}
                      disabled={!canEdit || saving}
                      onChange={(e) =>
                        setDraft((prev) => (prev ? { ...prev, description: e.target.value } : prev))
                      }
                    />
                  </div>
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                      gap: "var(--space-4)",
                    }}
                  >
                    <div>
                      <Label htmlFor="detail-task-status">Status</Label>
                      <Select
                        id="detail-task-status"
                        value={draft.status}
                        disabled={!canEdit || saving}
                        onChange={(e) =>
                          setDraft((prev) => (prev ? { ...prev, status: e.target.value } : prev))
                        }
                      >
                        {DEFAULT_TASK_STATUSES.map((status) => (
                          <option key={status.id} value={status.id}>
                            {status.label}
                          </option>
                        ))}
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="detail-task-priority">Priority</Label>
                      <Select
                        id="detail-task-priority"
                        value={draft.priority}
                        disabled={!canEdit || saving}
                        onChange={(e) =>
                          setDraft((prev) => (prev ? { ...prev, priority: e.target.value } : prev))
                        }
                      >
                        {priorityOptions.map((priority) => (
                          <option key={priority.id} value={priority.id}>
                            {priority.label}
                          </option>
                        ))}
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="detail-task-due-date">Due date</Label>
                      <Input
                        id="detail-task-due-date"
                        type="date"
                        value={draft.due_date}
                        disabled={!canEdit || saving}
                        onChange={(e) =>
                          setDraft((prev) => (prev ? { ...prev, due_date: e.target.value } : prev))
                        }
                      />
                    </div>
                  </div>
                  <TaskAssigneeSelect
                    id="detail-task-assignee"
                    value={draft.assignee_user_id}
                    onChange={(assignee_user_id) =>
                      setDraft((prev) => (prev ? { ...prev, assignee_user_id } : prev))
                    }
                    ownerUserId={ownerUserId}
                    members={members}
                    usersById={usersById}
                    disabled={!canEdit || saving}
                  />

                  <section style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        gap: "var(--space-3)",
                      }}
                    >
                      <h3
                        style={{
                          margin: 0,
                          fontFamily: "var(--font-ui)",
                          fontSize: "0.9375rem",
                          fontWeight: 700,
                        }}
                      >
                        Subtasks
                      </h3>
                      {canEdit ? (
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => onAddSubtask(task.id)}
                        >
                          <Plus className="w-4 h-4" />
                          Add subtask
                        </Button>
                      ) : null}
                    </div>
                    {subtasks.length === 0 ? (
                      <p style={{ margin: 0, fontSize: "0.875rem", color: "var(--text-muted)" }}>
                        No subtasks yet.
                      </p>
                    ) : (
                      <ul
                        style={{
                          margin: 0,
                          padding: 0,
                          listStyle: "none",
                          display: "flex",
                          flexDirection: "column",
                          gap: "var(--space-2)",
                        }}
                      >
                        {subtasks.map((subtask) => (
                          <li key={subtask.id}>
                            <button
                              type="button"
                              onClick={() => onOpenTask(subtask.id)}
                              style={{
                                width: "100%",
                                padding: "var(--space-3) var(--space-4)",
                                border: "1px solid var(--border-subtle)",
                                borderRadius: "var(--radius-btn)",
                                background: "var(--bg-canvas)",
                                textAlign: "left",
                                cursor: "pointer",
                                font: "inherit",
                                fontSize: "0.875rem",
                              }}
                            >
                              {subtask.title}
                            </button>
                          </li>
                        ))}
                      </ul>
                    )}
                  </section>
                </div>
              </SheetBody>
              <SheetFooter>
                {canEdit ? (
                  <>
                    <Button
                      type="button"
                      variant="danger"
                      disabled={saving || deleting}
                      onClick={() => setDeleteOpen(true)}
                    >
                      <Trash2 className="w-4 h-4" />
                      Delete
                    </Button>
                    <Button
                      type="button"
                      variant="primary"
                      disabled={!isDirty || saving}
                      onClick={() => void handleSave()}
                    >
                      Save changes
                    </Button>
                  </>
                ) : (
                  <Button type="button" variant="secondary" onClick={() => onOpenChange(false)}>
                    Close
                  </Button>
                )}
              </SheetFooter>
            </>
          ) : (
            <>
              <SheetBody>
                <p style={{ margin: 0, color: "var(--text-muted)" }}>
                  This task does not exist in this project or may have been deleted.
                </p>
              </SheetBody>
              <SheetFooter>
                <Button type="button" variant="secondary" onClick={() => onOpenChange(false)}>
                  Close
                </Button>
              </SheetFooter>
            </>
          )}
        </SheetContent>
      </Sheet>

      {task ? (
        <TaskDeleteConfirmDialog
          open={deleteOpen}
          onOpenChange={setDeleteOpen}
          taskTitle={task.title}
          loading={deleting}
          onConfirm={handleDelete}
        />
      ) : null}
    </>
  )
}
