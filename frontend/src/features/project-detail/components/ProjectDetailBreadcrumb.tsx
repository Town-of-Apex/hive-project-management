/**
 * Breadcrumb navigation for the project workspace.
 */

import { Link } from "react-router-dom"
import { ChevronRight } from "lucide-react"

interface ProjectDetailBreadcrumbProps {
  projectName: string
}

export function ProjectDetailBreadcrumb({ projectName }: ProjectDetailBreadcrumbProps) {
  return (
    <nav
      aria-label="Breadcrumb"
      style={{
        display: "flex",
        alignItems: "center",
        gap: "var(--space-2)",
        fontSize: "0.875rem",
        color: "var(--text-muted)",
      }}
    >
      <Link
        to="/projects"
        style={{
          color: "var(--brand-primary)",
          textDecoration: "none",
          fontWeight: 600,
        }}
      >
        Projects
      </Link>
      <ChevronRight style={{ width: 14, height: 14, flexShrink: 0 }} aria-hidden />
      <span style={{ color: "var(--text-main)", fontWeight: 600 }}>{projectName}</span>
    </nav>
  )
}
