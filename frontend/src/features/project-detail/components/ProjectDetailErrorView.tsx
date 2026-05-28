/**
 * Humorous empty/error states for project detail (404, 403, invalid link).
 */

import { Button } from "@/components/ui/Button"

export type ProjectDetailErrorKind = "invalid_id" | "not_found" | "forbidden" | "unknown"

interface ProjectDetailErrorViewProps {
  kind: ProjectDetailErrorKind
  message?: string | null
  onBack: () => void
}

const copyByKind: Record<
  ProjectDetailErrorKind,
  { title: string; body: string }
> = {
  invalid_id: {
    title: "That link doesn't look like a project",
    body: "The URL has a project ID that isn't a number. Maybe a typo, maybe a raccoon walked on the keyboard.",
  },
  not_found: {
    title: "This project is in another castle",
    body: "We searched high and low (well, one database query) and couldn't find that project. It may have been deleted, renamed, or never existed outside a planning meeting.",
  },
  forbidden: {
    title: "Members only — and you're not on the list",
    body: "This project exists, but you don't have permission to view it. Ask the owner nicely, or check whether you're in the right department.",
  },
  unknown: {
    title: "Something went sideways",
    body: "We couldn't load this project. Try again in a moment, or head back to the project list.",
  },
}

export function ProjectDetailErrorView({
  kind,
  message,
  onBack,
}: ProjectDetailErrorViewProps) {
  const copy = copyByKind[kind]

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-5)",
        maxWidth: "36rem",
        padding: "var(--space-8) 0",
      }}
    >
      <h1
        style={{
          margin: 0,
          fontFamily: "var(--font-display)",
          fontSize: "clamp(1.5rem, 2.5vw, 1.875rem)",
          fontWeight: 700,
          lineHeight: 1.25,
          color: "var(--text-main)",
        }}
      >
        {copy.title}
      </h1>
      <p style={{ margin: 0, fontSize: "1rem", lineHeight: 1.6, color: "var(--text-muted)" }}>
        {copy.body}
      </p>
      {message && kind === "unknown" && (
        <p
          style={{
            margin: 0,
            fontSize: "0.875rem",
            color: "var(--text-muted)",
            fontFamily: "var(--font-mono, monospace)",
          }}
        >
          {message}
        </p>
      )}
      <div>
        <Button variant="secondary" type="button" onClick={onBack}>
          Back to projects
        </Button>
      </div>
    </div>
  )
}

export function resolveProjectDetailErrorKind(
  errorStatus: number | null,
  hasError: boolean
): ProjectDetailErrorKind {
  if (errorStatus === 403) return "forbidden"
  if (errorStatus === 404) return "not_found"
  if (hasError) return "unknown"
  return "not_found"
}
