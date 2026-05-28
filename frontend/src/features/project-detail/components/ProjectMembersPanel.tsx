/**
 * Read-only project members list.
 */

import { Badge } from "@/components/ui/Badge"
import type { ProjectMember } from "@/types/projectMember"
import type { User } from "@/types/db"

const roleLabels: Record<string, string> = {
  manager: "Manager",
  member: "Member",
  viewer: "Viewer",
}

interface ProjectMembersPanelProps {
  members: ProjectMember[]
  usersById: Record<number, User>
  ownerUserId: number | null
}

export function ProjectMembersPanel({
  members,
  usersById,
  ownerUserId,
}: ProjectMembersPanelProps) {
  const owner = ownerUserId != null ? usersById[ownerUserId] : null

  return (
    <section aria-labelledby="project-members-heading">
      <h2
        id="project-members-heading"
        style={{
          fontSize: "0.75rem",
          fontWeight: 700,
          textTransform: "uppercase",
          letterSpacing: "0.06em",
          color: "var(--text-muted)",
          marginBottom: "var(--space-3)",
        }}
      >
        Members
      </h2>
      <ul
        style={{
          listStyle: "none",
          margin: 0,
          padding: 0,
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-2)",
        }}
      >
        {owner && (
          <li
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "var(--space-3)",
              padding: "var(--space-2) 0",
            }}
          >
            <span style={{ fontWeight: 600 }}>{owner.full_name}</span>
            <Badge variant="info">Owner</Badge>
          </li>
        )}
        {members.map((member) => {
          const user = usersById[member.user_id]
          if (!user) return null
          if (member.user_id === ownerUserId) return null
          return (
            <li
              key={member.id}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "var(--space-3)",
                padding: "var(--space-2) 0",
              }}
            >
              <span>{user.full_name}</span>
              <Badge>{roleLabels[member.role] ?? member.role}</Badge>
            </li>
          )
        })}
        {members.length === 0 && !owner && (
          <li style={{ color: "var(--text-muted)", fontSize: "0.875rem" }}>No members listed.</li>
        )}
      </ul>
    </section>
  )
}
