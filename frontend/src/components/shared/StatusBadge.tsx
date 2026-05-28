/**
 * components/shared/StatusBadge.tsx
 */

import { Badge } from "@/components/ui/Badge"
import type { BadgeProps } from "@/components/ui/Badge"
import type { ProjectStatus } from "@/types/project"

interface StatusBadgeProps {
  status: string
}

const PROJECT_STATUS_VARIANT: Record<ProjectStatus, BadgeProps["variant"]> = {
  active: "success",
  on_hold: "warning",
  completed: "info",
  archived: "default",
}

function variantForStatus(status: string): BadgeProps["variant"] {
  if (status in PROJECT_STATUS_VARIANT) {
    return PROJECT_STATUS_VARIANT[status as ProjectStatus]
  }
  return "default"
}

function labelForStatus(status: string): string {
  return status.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
}

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <Badge variant={variantForStatus(status)}>
      {labelForStatus(status)}
    </Badge>
  )
}
