/**
 * pages/LoginPage.tsx
 */

import { useState, type FormEvent } from "react"
import { Navigate, useLocation, useNavigate } from "react-router-dom"
import { toast } from "sonner"

import { useAuth } from "@/contexts/AuthContext"
import { Button } from "@/components/ui/Button"
import { Card } from "@/components/ui/Card"
import { Input } from "@/components/ui/Input"
import { Label } from "@/components/ui/Label"

export function LoginPage() {
  const { login, isAuthenticated, loading } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname ?? "/projects"

  const [username, setUsername] = useState("devadmin")
  const [password, setPassword] = useState("devadmin123")
  const [submitting, setSubmitting] = useState(false)

  if (!loading && isAuthenticated) {
    return <Navigate to={from} replace />
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      await login(username, password)
      toast.success("Signed in")
      navigate(from, { replace: true })
    } catch (error) {
      toast.error("Sign in failed", { description: String(error) })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "var(--space-6)",
        background: "var(--bg-canvas)",
      }}
    >
      <Card style={{ width: "100%", maxWidth: "420px", padding: "var(--space-8)" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-6)" }}>
          <div>
            <p style={{ margin: 0, fontSize: "0.75rem", fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase" }}>
              Hive
            </p>
            <h1 style={{ margin: "var(--space-2) 0 0", fontSize: "1.5rem" }}>Sign in</h1>
            <p style={{ margin: "var(--space-2) 0 0", color: "var(--text-muted)", fontSize: "0.875rem" }}>
              Development auth stub. Use seeded credentials below.
            </p>
          </div>

          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
            <div>
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                autoComplete="username"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <Button variant="primary" type="submit" disabled={submitting}>
              {submitting ? "Signing in..." : "Sign in"}
            </Button>
          </form>

          <p style={{ margin: 0, fontSize: "0.8125rem", color: "var(--text-muted)" }}>
            Dev seed: <strong>devadmin</strong> / <strong>devadmin123</strong>
          </p>
        </div>
      </Card>
    </div>
  )
}
