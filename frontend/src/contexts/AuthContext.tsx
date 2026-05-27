/**
 * contexts/AuthContext.tsx
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react"

import * as authService from "@/services/authService"
import { getAuthToken } from "@/services/api"
import type { User } from "@/types/user"

interface AuthContextValue {
  user: User | null
  loading: boolean
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  const refreshUser = useCallback(async () => {
    const token = getAuthToken()
    if (!token) {
      setUser(null)
      return
    }
    const me = await authService.getMe()
    setUser(me)
  }, [])

  useEffect(() => {
    const init = async () => {
      try {
        await refreshUser()
      } catch {
        authService.logout()
        setUser(null)
      } finally {
        setLoading(false)
      }
    }
    void init()
  }, [refreshUser])

  const login = useCallback(async (username: string, password: string) => {
    await authService.login(username, password)
    await refreshUser()
  }, [refreshUser])

  const logout = useCallback(() => {
    authService.logout()
    setUser(null)
  }, [])

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: user !== null,
      login,
      logout,
      refreshUser,
    }),
    [user, loading, login, logout, refreshUser]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider")
  }
  return ctx
}
