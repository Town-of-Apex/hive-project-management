/**
 * Confirm dialog for deleting a task.
 */

import { Button } from "@/components/ui/Button"
import {
  Dialog,
  DialogBody,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/Dialog"

interface TaskDeleteConfirmDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  taskTitle: string
  loading?: boolean
  onConfirm: () => void | Promise<void>
}

export function TaskDeleteConfirmDialog({
  open,
  onOpenChange,
  taskTitle,
  loading = false,
  onConfirm,
}: TaskDeleteConfirmDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete task</DialogTitle>
        </DialogHeader>
        <DialogBody>
          <p style={{ margin: 0, color: "var(--text-main)", lineHeight: 1.6 }}>
            Delete <strong>{taskTitle}</strong> and any subtasks? This cannot be undone.
          </p>
        </DialogBody>
        <DialogFooter>
          <Button variant="secondary" type="button" disabled={loading} onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button
            variant="danger"
            type="button"
            disabled={loading}
            onClick={() => void onConfirm()}
          >
            Delete task
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
