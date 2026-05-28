/**
 * Project metadata header with view/edit toggle.
 */

import { useEffect, useState } from "react"
import { Pencil, X, Check } from "lucide-react"

import { StatusBadge } from "@/components/shared/StatusBadge"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Label } from "@/components/ui/Label"
import { Select } from "@/components/ui/Select"
import { Textarea } from "@/components/ui/Textarea"
import type { ProjectDetail, ProjectFormData, ProjectPriority, ProjectStatus } from "@/types/project"

interface ProjectDetailHeaderProps {
  project: ProjectDetail
  onSave: (data: Partial<ProjectFormData>) => Promise<void>
}

const priorityLabels: Record<string, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
}

export function ProjectDetailHeader({ project, onSave }: ProjectDetailHeaderProps) {
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [draft, setDraft] = useState<ProjectFormData>({
    name: project.name,
    description: project.description ?? "",
    status: project.status as ProjectStatus,
    priority: project.priority as ProjectPriority,
  })

  useEffect(() => {
    if (!editing) {
      setDraft({
        name: project.name,
        description: project.description ?? "",
        status: project.status as ProjectStatus,
        priority: project.priority as ProjectPriority,
      })
    }
  }, [project, editing])

  const handleCancel = () => {
    setDraft({
      name: project.name,
      description: project.description ?? "",
      status: project.status as ProjectStatus,
      priority: project.priority as ProjectPriority,
    })
    setEditing(false)
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      await onSave({
        name: draft.name.trim(),
        description: draft.description.trim() || "",
        status: draft.status,
        priority: draft.priority,
      })
      setEditing(false)
    } finally {
      setSaving(false)
    }
  }

  return (
    <header style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "flex-start",
          justifyContent: "space-between",
          gap: "var(--space-4)",
        }}
      >
        {editing ? (
          <div style={{ flex: 1, minWidth: "240px" }}>
            <Label htmlFor="project-name-edit">Project name</Label>
            <Input
              id="project-name-edit"
              value={draft.name}
              onChange={(e) => setDraft({ ...draft, name: e.target.value })}
              style={{ fontSize: "1.5rem", fontWeight: 700, fontFamily: "var(--font-display)" }}
            />
          </div>
        ) : (
          <h1
            style={{
              margin: 0,
              fontFamily: "var(--font-display)",
              fontSize: "clamp(1.75rem, 3vw, 2.25rem)",
              fontWeight: 700,
              lineHeight: 1.2,
              color: "var(--text-main)",
            }}
          >
            {project.name}
          </h1>
        )}

        {project.can_edit && !editing && (
          <Button variant="secondary" type="button" onClick={() => setEditing(true)}>
            <Pencil className="w-4 h-4" />
            Edit
          </Button>
        )}
        {editing && (
          <div style={{ display: "flex", gap: "var(--space-2)" }}>
            <Button variant="secondary" type="button" onClick={handleCancel} disabled={saving}>
              <X className="w-4 h-4" />
              Cancel
            </Button>
            <Button variant="primary" type="button" onClick={() => void handleSave()} disabled={saving}>
              <Check className="w-4 h-4" />
              {saving ? "Saving…" : "Save"}
            </Button>
          </div>
        )}
      </div>

      {editing ? (
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
          <div>
            <Label htmlFor="project-desc-edit">Description</Label>
            <Textarea
              id="project-desc-edit"
              rows={3}
              value={draft.description}
              onChange={(e) => setDraft({ ...draft, description: e.target.value })}
            />
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--space-4)" }}>
            <div style={{ minWidth: "160px" }}>
              <Label htmlFor="project-status-edit">Status</Label>
              <Select
                id="project-status-edit"
                value={draft.status}
                onChange={(e) => setDraft({ ...draft, status: e.target.value as ProjectStatus })}
              >
                <option value="active">Active</option>
                <option value="on_hold">On Hold</option>
                <option value="completed">Completed</option>
                <option value="archived">Archived</option>
              </Select>
            </div>
            <div style={{ minWidth: "160px" }}>
              <Label htmlFor="project-priority-edit">Priority</Label>
              <Select
                id="project-priority-edit"
                value={draft.priority}
                onChange={(e) => setDraft({ ...draft, priority: e.target.value as ProjectPriority })}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </Select>
            </div>
          </div>
        </div>
      ) : (
        <>
          {project.description ? (
            <p
              style={{
                margin: 0,
                fontSize: "1rem",
                lineHeight: 1.6,
                color: "var(--text-muted)",
                maxWidth: "52rem",
              }}
            >
              {project.description}
            </p>
          ) : (
            <p style={{ margin: 0, color: "var(--text-muted)", fontStyle: "italic" }}>
              No description yet.
            </p>
          )}
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "var(--space-4)",
              alignItems: "center",
              fontSize: "0.875rem",
            }}
          >
            <StatusBadge status={project.status} />
            <span style={{ color: "var(--text-muted)" }}>
              Priority: <strong style={{ color: "var(--text-main)" }}>{priorityLabels[project.priority] ?? project.priority}</strong>
            </span>
            <span style={{ color: "var(--text-muted)" }}>
              Visibility: <strong style={{ color: "var(--text-main)" }}>{project.visibility}</strong>
            </span>
            <span style={{ color: "var(--text-muted)" }}>
              Updated {new Date(project.updated_at).toLocaleDateString()}
            </span>
          </div>
        </>
      )}
    </header>
  )
}
