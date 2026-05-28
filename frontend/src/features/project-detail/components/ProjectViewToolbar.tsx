/**
 * View switcher toolbar (table active; other views reserved for later).
 */

import { LayoutList } from "lucide-react"

export type ProjectViewId = "table" | "board" | "calendar" | "timeline"

interface ProjectViewToolbarProps {
  activeView: ProjectViewId
  onViewChange?: (view: ProjectViewId) => void
}

const VIEWS: { id: ProjectViewId; label: string; enabled: boolean }[] = [
  { id: "table", label: "Table", enabled: true },
  { id: "board", label: "Board", enabled: false },
  { id: "calendar", label: "Calendar", enabled: false },
  { id: "timeline", label: "Timeline", enabled: false },
]

export function ProjectViewToolbar({ activeView }: ProjectViewToolbarProps) {
  return (
    <div
      role="tablist"
      aria-label="Project views"
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "var(--space-2)",
        borderBottom: "1px solid var(--border-subtle)",
        paddingBottom: "var(--space-4)",
      }}
    >
      {VIEWS.map((view) => {
        const isActive = view.id === activeView
        const disabled = !view.enabled
        return (
          <button
            key={view.id}
            type="button"
            role="tab"
            aria-selected={isActive}
            disabled={disabled}
            title={disabled ? "Coming soon" : undefined}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "var(--space-2)",
              padding: "var(--space-2) var(--space-4)",
              borderRadius: "var(--radius-btn)",
              border: "none",
              fontSize: "0.875rem",
              fontWeight: 600,
              cursor: disabled ? "not-allowed" : "pointer",
              opacity: disabled ? 0.45 : 1,
              background: isActive ? "var(--brand-primary-soft)" : "transparent",
              color: isActive ? "var(--brand-primary)" : "var(--text-muted)",
            }}
          >
            {view.id === "table" && <LayoutList style={{ width: 16, height: 16 }} />}
            {view.label}
          </button>
        )
      })}
    </div>
  )
}
