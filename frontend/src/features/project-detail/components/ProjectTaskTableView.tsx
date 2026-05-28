/**
 * Default table view: tasks grouped by status with indented subtasks.
 */

import { useMemo, useState } from "react"
import { Plus } from "lucide-react"
import { toast } from "sonner"

import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { buildTaskStatusGroups } from "@/features/project-detail/utils/taskTableRows"
import type { Task } from "@/types/task"
import type { User } from "@/types/db"

interface ProjectTaskTableViewProps {
  tasks: Task[]
  usersById: Record<number, User>
  canEdit: boolean
  onAddTask: (title: string) => Promise<void>
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
  canEdit,
  onAddTask,
}: ProjectTaskTableViewProps) {
  const groups = useMemo(() => buildTaskStatusGroups(tasks), [tasks])
  const [newTitle, setNewTitle] = useState("")
  const [adding, setAdding] = useState(false)

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    const title = newTitle.trim()
    if (!title) return
    setAdding(true)
    try {
      await onAddTask(title)
      setNewTitle("")
      toast.success("Task added")
    } catch (err) {
      toast.error("Failed to add task", { description: String(err) })
    } finally {
      setAdding(false)
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

      {canEdit && (
        <form
          onSubmit={(e) => void handleAdd(e)}
          style={{
            display: "flex",
            gap: "var(--space-3)",
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          <Input
            placeholder="Add a task…"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            disabled={adding}
            style={{ flex: 1, minWidth: "200px" }}
          />
          <Button type="submit" variant="primary" disabled={adding || !newTitle.trim()}>
            <Plus className="w-4 h-4" />
            Add task
          </Button>
        </form>
      )}

      {groups.length === 0 ? (
        <Card style={{ padding: "var(--space-10)", textAlign: "center", color: "var(--text-muted)" }}>
          No tasks yet.{canEdit ? " Add one above to get started." : ""}
        </Card>
      ) : (
        groups.map((group) => (
          <div key={group.status} style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
            <h3
              style={{
                margin: 0,
                fontSize: "0.8125rem",
                fontWeight: 700,
                textTransform: "uppercase",
                letterSpacing: "0.05em",
                color: "var(--text-muted)",
                paddingLeft: "var(--space-2)",
              }}
            >
              {group.label}
              <span style={{ fontWeight: 500, marginLeft: "var(--space-2)" }}>({group.rows.length})</span>
            </h3>
            <Card style={{ padding: 0, overflowX: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.875rem" }}>
                <thead>
                  <tr style={{ borderBottom: "1px solid var(--border-subtle)", background: "var(--bg-canvas)" }}>
                    <th style={{ padding: cellPadding, textAlign: "left", fontWeight: 700, width: "40%" }}>Task</th>
                    <th style={{ padding: cellPadding, textAlign: "left", fontWeight: 700 }}>Assignee</th>
                    <th style={{ padding: cellPadding, textAlign: "left", fontWeight: 700 }}>Priority</th>
                    <th style={{ padding: cellPadding, textAlign: "left", fontWeight: 700 }}>Due</th>
                  </tr>
                </thead>
                <tbody>
                  {group.rows.map(({ task, depth }) => {
                    const assignee =
                      task.assignee_user_id != null ? usersById[task.assignee_user_id] : null
                    return (
                      <tr
                        key={task.id}
                        style={{ borderBottom: "1px solid var(--border-subtle)" }}
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
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </Card>
          </div>
        ))
      )}
    </section>
  )
}
