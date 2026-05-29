/**
 * components/ui/Sheet.tsx
 *
 * Side panel built on Radix UI Dialog with slide-from-right animation.
 * Use for detail views that should stay in page context (e.g. task drill-in).
 */

import * as React from "react"
import * as SheetPrimitive from "@radix-ui/react-dialog"
import { X } from "lucide-react"
import { cn } from "@/lib/utils"

const Sheet = SheetPrimitive.Root
const SheetTrigger = SheetPrimitive.Trigger
const SheetClose = SheetPrimitive.Close
const SheetPortal = SheetPrimitive.Portal

const SheetOverlay = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-[rgba(15,17,19,0.45)] backdrop-blur-sm",
      "data-[state=open]:animate-in data-[state=closed]:animate-out",
      "data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
  />
))
SheetOverlay.displayName = SheetPrimitive.Overlay.displayName

const SheetContent = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <SheetPortal>
    <SheetOverlay />
    <SheetPrimitive.Content
      ref={ref}
      className={cn(
        "fixed inset-y-0 right-0 z-50 flex h-full w-full max-w-[480px] flex-col",
        "border-l border-[var(--border-subtle)] bg-[var(--bg-surface)] shadow-[-8px_0_24px_-8px_rgba(0,0,0,0.15)]",
        "data-[state=open]:animate-in data-[state=closed]:animate-out",
        "data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right",
        "data-[state=closed]:duration-200 data-[state=open]:duration-300",
        className
      )}
      {...props}
    >
      {children}
      <SheetPrimitive.Close
        className={cn(
          "absolute right-4 top-4 rounded-[var(--radius-btn)] p-1",
          "text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-inner)]",
          "transition-colors duration-[var(--duration-fast)]",
          "focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--brand-primary)]"
        )}
        aria-label="Close panel"
      >
        <X className="h-4 w-4" />
      </SheetPrimitive.Close>
    </SheetPrimitive.Content>
  </SheetPortal>
))
SheetContent.displayName = SheetPrimitive.Content.displayName

const SheetHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col gap-2 border-b border-[var(--border-subtle)] px-[var(--space-6)] py-[var(--space-5)] pr-14",
      className
    )}
    {...props}
  />
)
SheetHeader.displayName = "SheetHeader"

const SheetTitle = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Title>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Title
    ref={ref}
    className={cn(
      "m-0 text-left font-[var(--font-ui)] text-[1.125rem] font-extrabold text-[var(--text-main)]",
      className
    )}
    {...props}
  />
))
SheetTitle.displayName = SheetPrimitive.Title.displayName

const SheetBody = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn("flex-1 overflow-y-auto px-[var(--space-6)] py-[var(--space-6)]", className)}
    {...props}
  />
)
SheetBody.displayName = "SheetBody"

const SheetFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-wrap items-center justify-end gap-[var(--space-3)]",
      "border-t border-[var(--border-subtle)] bg-[var(--bg-canvas)] px-[var(--space-6)] py-[var(--space-4)]",
      className
    )}
    {...props}
  />
)
SheetFooter.displayName = "SheetFooter"

export {
  Sheet,
  SheetTrigger,
  SheetClose,
  SheetPortal,
  SheetOverlay,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetBody,
  SheetFooter,
}
