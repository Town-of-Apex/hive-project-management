/**
 * hooks/useProjectWorkspace.ts
 *
 * URL-synced task panel and view-agnostic new-task dialog state.
 */

import { useCallback, useEffect, useMemo, useState } from "react"
import { useSearchParams } from "react-router-dom"

import type { NewTaskOptions } from "@/types/task"

export interface UseProjectWorkspaceResult {
  selectedTaskId: number | null
  openTask: (taskId: number) => void
  closeTask: () => void
  newTaskOpen: boolean
  newTaskOptions: NewTaskOptions
  openNewTask: (options?: NewTaskOptions) => void
  closeNewTask: () => void
}

function parseTaskId(raw: string | null): number | null {
  if (!raw) return null
  const id = Number(raw)
  if (!Number.isFinite(id) || id <= 0 || !Number.isInteger(id)) return null
  return id
}

export function useProjectWorkspace(): UseProjectWorkspaceResult {
  const [searchParams, setSearchParams] = useSearchParams()
  const [newTaskOpen, setNewTaskOpen] = useState(false)
  const [newTaskOptions, setNewTaskOptions] = useState<NewTaskOptions>({})

  const selectedTaskId = useMemo(
    () => parseTaskId(searchParams.get("task")),
    [searchParams]
  )

  // Strip malformed ?task= values from the URL
  useEffect(() => {
    const raw = searchParams.get("task")
    if (raw && parseTaskId(raw) == null) {
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev)
          next.delete("task")
          return next
        },
        { replace: true }
      )
    }
  }, [searchParams, setSearchParams])

  const openTask = useCallback(
    (taskId: number) => {
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev)
          next.set("task", String(taskId))
          return next
        },
        { replace: true }
      )
    },
    [setSearchParams]
  )

  const closeTask = useCallback(() => {
    setSearchParams(
      (prev) => {
        const next = new URLSearchParams(prev)
        next.delete("task")
        return next
      },
      { replace: true }
    )
  }, [setSearchParams])

  const openNewTask = useCallback((options: NewTaskOptions = {}) => {
    setNewTaskOptions(options)
    setNewTaskOpen(true)
  }, [])

  const closeNewTask = useCallback(() => {
    setNewTaskOpen(false)
    setNewTaskOptions({})
  }, [])

  useEffect(() => {
    if (newTaskOpen) closeTask()
  }, [newTaskOpen, closeTask])

  return {
    selectedTaskId,
    openTask,
    closeTask,
    newTaskOpen,
    newTaskOptions,
    openNewTask,
    closeNewTask,
  }
}
