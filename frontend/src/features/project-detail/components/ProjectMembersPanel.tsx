/**
 * Read-only project members list.
 */

import type { ReactNode } from "react"

import { Badge } from "@/components/ui/Badge"
import { UserAvatar } from "@/components/shared/UserAvatar"
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

function MemberRow({
  user,
  badge,
  emphasizeName = false,
}: {
  user: User
  badge: ReactNode
  emphasizeName?: boolean
}) {
  return (
    <li
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "var(--space-3)",
        padding: "var(--space-2) 0",
      }}
    >
      <span
        style={{
          display: "flex",
          alignItems: "center",
          gap: "var(--space-3)",
          minWidth: 0,
        }}
      >
        <UserAvatar
          fullName={user.full_name}
          profileImageUrl={user.profile_image_url}
          size={28}
        />
        <span style={{ fontWeight: emphasizeName ? 600 : 400, overflow: "hidden", textOverflow: "ellipsis" }}>
          {user.full_name}
        </span>
      </span>
      {badge}
    </li>
  )
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
          <MemberRow
            user={owner}
            emphasizeName
            badge={<Badge variant="info">Owner</Badge>}
          />
        )}
        {members.map((member) => {
          const user = usersById[member.user_id]
          if (!user) return null
          if (member.user_id === ownerUserId) return null
          return (
            <MemberRow
              key={member.id}
              user={user}
              badge={<Badge>{roleLabels[member.role] ?? member.role}</Badge>}
            />
          )
        })}
        {members.length === 0 && !owner && (
          <li style={{ color: "var(--text-muted)", fontSize: "0.875rem" }}>No members listed.</li>
        )}
      </ul>
    </section>
  )
}
