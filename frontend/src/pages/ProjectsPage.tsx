/**
 * pages/ProjectsPage.tsx
 *
 * Project management list and create.
 */

import { useState, useEffect, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { Search, Plus } from "lucide-react"

import { PageContainer } from "@/components/layout/PageContainer"
import { PageHeader } from "@/components/shared/PageHeader"
import { Divider } from "@/components/shared/Divider"
import { StatusBadge } from "@/components/shared/StatusBadge"
import { Card } from "@/components/ui/Card"
import { Input } from "@/components/ui/Input"
import { Select } from "@/components/ui/Select"
import { Button } from "@/components/ui/Button"
import { Label } from "@/components/ui/Label"
import { Textarea } from "@/components/ui/Textarea"
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogBody,
  DialogFooter,
} from "@/components/ui/Dialog"

import { useAuth } from "@/contexts/AuthContext"
import * as projectService from "@/services/projectService"
import * as taskService from "@/services/taskService"
import type { Project, ProjectFormData, ProjectStatus } from "@/types/project"

export function ProjectsPage() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [projects, setProjects] = useState<Project[]>([])
  const [taskCounts, setTaskCounts] = useState<Record<number, number>>({})
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState("")
  const [statusFilter, setStatusFilter] = useState<ProjectStatus | "">("")

  const [formOpen, setFormOpen] = useState(false)
  const [formData, setFormData] = useState<ProjectFormData>({
    name: "",
    description: "",
    status: "active",
    priority: "medium",
  })

  const loadProjects = async () => {
    setLoading(true)
    try {
      const data = await projectService.getAll({
        search: search.trim() !== "" ? search : undefined,
        status: statusFilter !== "" ? statusFilter : undefined,
      })
      setProjects(data)

      const counts: Record<number, number> = {}
      await Promise.all(
        data.map(async (project) => {
          const tasks = await taskService.getAll({ project_id: project.id })
          counts[project.id] = tasks.length
        })
      )
      setTaskCounts(counts)
    } catch (error) {
      toast.error("Failed to load projects", { description: String(error) })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const timer = setTimeout(() => {
      void loadProjects()
    }, 300)
    return () => clearTimeout(timer)
  }, [search, statusFilter])

  const priorityLabel = useMemo(
    () =>
      ({
        low: "Low",
        medium: "Medium",
        high: "High",
      }) as Record<string, string>,
    []
  )

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await projectService.create(formData)
      toast.success("Project created")
      setFormOpen(false)
      setFormData({
        name: "",
        description: "",
        status: "active",
        priority: "medium",
      })
      void loadProjects()
    } catch (error) {
      toast.error("Failed to create project", { description: String(error) })
    }
  }

  return (
    <PageContainer>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-6)" }}>
        <PageHeader
          overline="Projects"
          title="Project Management"
          subtitle={
            user
              ? `Signed in as ${user.full_name}. View and manage internal projects.`
              : "View and manage internal projects."
          }
        />

        <Divider />

        <section style={{ display: "flex", flexWrap: "wrap", gap: "var(--space-3)", alignItems: "stretch" }}>
          <div style={{ flex: 1, minWidth: "200px", position: "relative" }}>
            <Search
              style={{
                position: "absolute",
                left: "12px",
                top: "50%",
                transform: "translateY(-50%)",
                width: "16px",
                height: "16px",
                color: "var(--text-muted)",
              }}
            />
            <Input
              type="search"
              placeholder="Search by name or description..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ paddingLeft: "36px" }}
            />
          </div>

          <Select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as ProjectStatus | "")}
            style={{ minWidth: "160px" }}
          >
            <option value="">All Statuses</option>
            <option value="active">Active</option>
            <option value="on_hold">On Hold</option>
            <option value="completed">Completed</option>
            <option value="archived">Archived</option>
          </Select>

          <Dialog open={formOpen} onOpenChange={setFormOpen}>
            <DialogTrigger asChild>
              <Button variant="primary">
                <Plus className="w-4 h-4" />
                New Project
              </Button>
            </DialogTrigger>
            <DialogContent>
              <form onSubmit={handleFormSubmit}>
                <DialogHeader>
                  <DialogTitle>New Project</DialogTitle>
                </DialogHeader>
                <DialogBody>
                  <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
                    <div>
                      <Label htmlFor="name">Project Name *</Label>
                      <Input
                        id="name"
                        required
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      />
                    </div>
                    <div>
                      <Label htmlFor="description">Description</Label>
                      <Textarea
                        id="description"
                        rows={3}
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      />
                    </div>
                    <div style={{ display: "flex", gap: "var(--space-4)", flexWrap: "wrap" }}>
                      <div style={{ flex: 1, minWidth: "160px" }}>
                        <Label htmlFor="status">Status</Label>
                        <Select
                          id="status"
                          value={formData.status}
                          onChange={(e) =>
                            setFormData({ ...formData, status: e.target.value as ProjectStatus })
                          }
                        >
                          <option value="active">Active</option>
                          <option value="on_hold">On Hold</option>
                          <option value="completed">Completed</option>
                          <option value="archived">Archived</option>
                        </Select>
                      </div>
                      <div style={{ flex: 1, minWidth: "160px" }}>
                        <Label htmlFor="priority">Priority</Label>
                        <Select
                          id="priority"
                          value={formData.priority}
                          onChange={(e) =>
                            setFormData({
                              ...formData,
                              priority: e.target.value as ProjectFormData["priority"],
                            })
                          }
                        >
                          <option value="low">Low</option>
                          <option value="medium">Medium</option>
                          <option value="high">High</option>
                        </Select>
                      </div>
                    </div>
                  </div>
                </DialogBody>
                <DialogFooter>
                  <Button variant="secondary" type="button" onClick={() => setFormOpen(false)}>
                    Cancel
                  </Button>
                  <Button variant="primary" type="submit">
                    Create Project
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </section>

        <section>
          <Card style={{ padding: 0, overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.875rem" }}>
              <thead>
                <tr style={{ borderBottom: "1px solid var(--border-subtle)", background: "var(--bg-canvas)" }}>
                  <th style={{ padding: "var(--space-4) var(--space-6)", textAlign: "left", fontWeight: 700 }}>Name</th>
                  <th style={{ padding: "var(--space-4) var(--space-6)", textAlign: "left", fontWeight: 700 }}>Status</th>
                  <th style={{ padding: "var(--space-4) var(--space-6)", textAlign: "left", fontWeight: 700 }}>Priority</th>
                  <th style={{ padding: "var(--space-4) var(--space-6)", textAlign: "left", fontWeight: 700 }}>Tasks</th>
                  <th style={{ padding: "var(--space-4) var(--space-6)", textAlign: "left", fontWeight: 700 }}>Updated</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={5} style={{ padding: "var(--space-10)", textAlign: "center", color: "var(--text-muted)" }}>
                      Loading projects...
                    </td>
                  </tr>
                ) : projects.length === 0 ? (
                  <tr>
                    <td colSpan={5} style={{ padding: "var(--space-10)", textAlign: "center", color: "var(--text-muted)" }}>
                      No projects found.
                    </td>
                  </tr>
                ) : (
                  projects.map((project) => (
                    <tr
                      key={project.id}
                      onClick={() => navigate(`/projects/${project.id}`)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ") {
                          e.preventDefault()
                          navigate(`/projects/${project.id}`)
                        }
                      }}
                      tabIndex={0}
                      role="link"
                      style={{
                        borderBottom: "1px solid var(--border-subtle)",
                        cursor: "pointer",
                      }}
                    >
                      <td style={{ padding: "var(--space-3) var(--space-6)", fontWeight: 600 }}>
                        {project.name}
                        {project.description && (
                          <div style={{ fontWeight: 400, color: "var(--text-muted)", fontSize: "0.8125rem", marginTop: "4px" }}>
                            {project.description}
                          </div>
                        )}
                      </td>
                      <td style={{ padding: "var(--space-3) var(--space-6)" }}>
                        <StatusBadge status={project.status} />
                      </td>
                      <td style={{ padding: "var(--space-3) var(--space-6)" }}>
                        {priorityLabel[project.priority] ?? project.priority}
                      </td>
                      <td style={{ padding: "var(--space-3) var(--space-6)" }}>
                        {taskCounts[project.id] ?? "—"}
                      </td>
                      <td style={{ padding: "var(--space-3) var(--space-6)", color: "var(--text-muted)" }}>
                        {new Date(project.updated_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </Card>
        </section>
      </div>
    </PageContainer>
  )
}
