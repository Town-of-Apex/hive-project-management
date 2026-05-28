/**
 * User avatar with image URL or initials / icon placeholder.
 */

import { CircleUser } from "lucide-react"

interface UserAvatarProps {
  fullName: string
  profileImageUrl?: string | null
  size?: number
}

function initialsFromName(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) return "?"
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
}

export function UserAvatar({ fullName, profileImageUrl, size = 32 }: UserAvatarProps) {
  const dimension = `${size}px`
  const fontSize = `${Math.max(10, Math.round(size * 0.38))}px`

  if (profileImageUrl) {
    return (
      <img
        src={profileImageUrl}
        alt=""
        width={size}
        height={size}
        style={{
          width: dimension,
          height: dimension,
          borderRadius: "50%",
          objectFit: "cover",
          flexShrink: 0,
          background: "var(--bg-canvas)",
        }}
      />
    )
  }

  const initials = initialsFromName(fullName)
  if (initials !== "?") {
    return (
      <span
        aria-hidden
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          width: dimension,
          height: dimension,
          borderRadius: "50%",
          flexShrink: 0,
          fontSize,
          fontWeight: 700,
          color: "var(--text-main)",
          background: "var(--bg-canvas)",
          border: "1px solid var(--border-subtle)",
        }}
      >
        {initials}
      </span>
    )
  }

  return (
    <CircleUser
      aria-hidden
      style={{
        width: dimension,
        height: dimension,
        flexShrink: 0,
        color: "var(--text-muted)",
      }}
    />
  )
}
