/**
 * pages/ProjectDetailPage.tsx
 *
 * Project workspace: metadata, members, and task views (table v1).
 */

import { useMemo } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { toast } from "sonner"

import { PageContainer } from "@/components/layout/PageContainer"
import { Divider } from "@/components/shared/Divider"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { ProjectDetailBreadcrumb } from "@/features/project-detail/components/ProjectDetailBreadcrumb"
import { ProjectDetailHeader } from "@/features/project-detail/components/ProjectDetailHeader"
import { ProjectMembersPanel } from "@/features/project-detail/components/ProjectMembersPanel"
import { ProjectViewToolbar } from "@/features/project-detail/components/ProjectViewToolbar"
import { ProjectTaskTableView } from "@/features/project-detail/components/ProjectTaskTableView"
import { useProjectDetail } from "@/features/project-detail/hooks/useProjectDetail"
import type { ProjectFormData } from "@/types/project"

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
    updateProject,
    addTask,
  } = useProjectDetail(projectId)

  const handleSaveProject = async (data: Partial<ProjectFormData>) => {
    try {
      await updateProject(data)
      toast.success("Project updated")
    } catch (err) {
      toast.error("Failed to update project", { description: String(err) })
      throw err
    }
  }

  if (projectId == null) {
    return (
      <PageContainer>
        <p style={{ color: "var(--text-muted)" }}>Invalid project link.</p>
        <Button variant="secondary" onClick={() => navigate("/projects")}>
          Back to projects
        </Button>
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
        <p style={{ color: "var(--text-muted)" }}>{error ?? "Project not found."}</p>
        <Button variant="secondary" onClick={() => navigate("/projects")}>
          Back to projects
        </Button>
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

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "minmax(0, 1fr) minmax(200px, 280px)",
            gap: "var(--space-8)",
            alignItems: "start",
          }}
        >
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
          canEdit={project.can_edit}
          onAddTask={(title) => addTask(title)}
        />
      </div>
    </PageContainer>
  )
}
