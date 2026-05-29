/**
 * View-agnostic dialog for creating tasks and subtasks.
 */

import { useEffect, useState } from "react"
import { toast } from "sonner"

import { Button } from "@/components/ui/Button"
import {
  Dialog,
  DialogBody,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/Dialog"
import { Input } from "@/components/ui/Input"
import { Label } from "@/components/ui/Label"
import { Select } from "@/components/ui/Select"
import { Textarea } from "@/components/ui/Textarea"
import { TaskAssigneeSelect } from "@/features/project-detail/components/TaskAssigneeSelect"
import { DEFAULT_TASK_STATUSES } from "@/features/project-detail/constants/taskStatuses"
import type { ProjectMember } from "@/types/projectMember"
import type { NewTaskOptions, Task, TaskFormValues } from "@/types/task"
import type { User } from "@/types/db"

const priorityOptions = [
  { id: "low", label: "Low" },
  { id: "medium", label: "Medium" },
  { id: "high", label: "High" },
]

function emptyForm(defaultStatus = "todo"): TaskFormValues {
  return {
    title: "",
    description: "",
    status: defaultStatus,
    priority: "medium",
    assignee_user_id: null,
    due_date: "",
  }
}

interface TaskFormDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  canEdit: boolean
  ownerUserId: number
  members: ProjectMember[]
  usersById: Record<number, User>
  options?: NewTaskOptions
  parentTaskTitle?: string | null
  onSubmit: (values: TaskFormValues & { parent_task_id?: number | null }) => Promise<Task>
}

export function TaskFormDialog({
  open,
  onOpenChange,
  canEdit,
  ownerUserId,
  members,
  usersById,
  options = {},
  parentTaskTitle,
  onSubmit,
}: TaskFormDialogProps) {
  const [form, setForm] = useState<TaskFormValues>(() => emptyForm(options.defaultStatus))
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (open) {
      setForm(emptyForm(options.defaultStatus))
    }
  }, [open, options.defaultStatus])

  const isSubtask = options.parentTaskId != null
  const title = isSubtask ? "Add subtask" : "New task"

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!canEdit) return
    const trimmedTitle = form.title.trim()
    if (!trimmedTitle) {
      toast.error("Title is required")
      return
    }

    setSubmitting(true)
    try {
      await onSubmit({
        ...form,
        title: trimmedTitle,
        description: form.description.trim() || "",
        due_date: form.due_date || null,
        parent_task_id: options.parentTaskId ?? null,
      })
      toast.success(isSubtask ? "Subtask created" : "Task created")
      onOpenChange(false)
    } catch (err) {
      toast.error(isSubtask ? "Failed to create subtask" : "Failed to create task", {
        description: String(err),
      })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <form onSubmit={(e) => void handleSubmit(e)}>
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            {isSubtask && parentTaskTitle ? (
              <p style={{ margin: 0, fontSize: "0.875rem", color: "var(--text-muted)" }}>
                Parent: {parentTaskTitle}
              </p>
            ) : null}
          </DialogHeader>
          <DialogBody>
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
              <div>
                <Label htmlFor="task-title">Title *</Label>
                <Input
                  id="task-title"
                  required
                  value={form.title}
                  disabled={!canEdit || submitting}
                  onChange={(e) => setForm((prev) => ({ ...prev, title: e.target.value }))}
                />
              </div>
              <div>
                <Label htmlFor="task-description">Description</Label>
                <Textarea
                  id="task-description"
                  rows={3}
                  value={form.description}
                  disabled={!canEdit || submitting}
                  onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
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
                  <Label htmlFor="task-status">Status</Label>
                  <Select
                    id="task-status"
                    value={form.status}
                    disabled={!canEdit || submitting}
                    onChange={(e) => setForm((prev) => ({ ...prev, status: e.target.value }))}
                  >
                    {DEFAULT_TASK_STATUSES.map((status) => (
                      <option key={status.id} value={status.id}>
                        {status.label}
                      </option>
                    ))}
                  </Select>
                </div>
                <div>
                  <Label htmlFor="task-priority">Priority</Label>
                  <Select
                    id="task-priority"
                    value={form.priority}
                    disabled={!canEdit || submitting}
                    onChange={(e) => setForm((prev) => ({ ...prev, priority: e.target.value }))}
                  >
                    {priorityOptions.map((priority) => (
                      <option key={priority.id} value={priority.id}>
                        {priority.label}
                      </option>
                    ))}
                  </Select>
                </div>
                <div>
                  <Label htmlFor="task-due-date">Due date</Label>
                  <Input
                    id="task-due-date"
                    type="date"
                    value={form.due_date}
                    disabled={!canEdit || submitting}
                    onChange={(e) => setForm((prev) => ({ ...prev, due_date: e.target.value }))}
                  />
                </div>
              </div>
              <TaskAssigneeSelect
                value={form.assignee_user_id}
                onChange={(assignee_user_id) =>
                  setForm((prev) => ({ ...prev, assignee_user_id }))
                }
                ownerUserId={ownerUserId}
                members={members}
                usersById={usersById}
                disabled={!canEdit || submitting}
              />
            </div>
          </DialogBody>
          <DialogFooter>
            <Button
              variant="secondary"
              type="button"
              disabled={submitting}
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button variant="primary" type="submit" disabled={!canEdit || submitting}>
              {isSubtask ? "Create subtask" : "Create task"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
