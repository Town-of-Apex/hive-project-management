/**
 * Assignee picker limited to project owner and members.
 */

import { Label } from "@/components/ui/Label"
import { Select } from "@/components/ui/Select"
import type { ProjectMember } from "@/types/projectMember"
import type { User } from "@/types/db"

interface AssigneeOption {
  userId: number
  label: string
}

interface TaskAssigneeSelectProps {
  id?: string
  label?: string
  value: number | null
  onChange: (userId: number | null) => void
  ownerUserId: number
  members: ProjectMember[]
  usersById: Record<number, User>
  disabled?: boolean
}

export function buildAssigneeOptions(
  ownerUserId: number,
  members: ProjectMember[],
  usersById: Record<number, User>
): AssigneeOption[] {
  const seen = new Set<number>()
  const options: AssigneeOption[] = []

  const addUser = (userId: number) => {
    if (seen.has(userId)) return
    seen.add(userId)
    const user = usersById[userId]
    options.push({
      userId,
      label: user?.full_name ?? `User #${userId}`,
    })
  }

  addUser(ownerUserId)
  for (const member of members) addUser(member.user_id)

  return options.sort((a, b) => a.label.localeCompare(b.label))
}

export function TaskAssigneeSelect({
  id = "task-assignee",
  label = "Assignee",
  value,
  onChange,
  ownerUserId,
  members,
  usersById,
  disabled = false,
}: TaskAssigneeSelectProps) {
  const options = buildAssigneeOptions(ownerUserId, members, usersById)

  return (
    <div>
      <Label htmlFor={id}>{label}</Label>
      <Select
        id={id}
        value={value ?? ""}
        disabled={disabled}
        onChange={(e) => {
          const next = e.target.value
          onChange(next === "" ? null : Number(next))
        }}
      >
        <option value="">Unassigned</option>
        {options.map((option) => (
          <option key={option.userId} value={option.userId}>
            {option.label}
          </option>
        ))}
      </Select>
    </div>
  )
}
