/**
 * services/authService.ts
 */

import { get, post, setAuthToken, clearAuthToken } from "@/services/api"
import type { User } from "@/types/user"

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface MeResponse {
  user: User
}

export async function login(username: string, password: string): Promise<LoginResponse> {
  const data = await post<LoginResponse>("/api/auth/login", { username, password })
  setAuthToken(data.access_token)
  return data
}

export async function getMe(): Promise<User> {
  const data = await get<MeResponse>("/api/auth/me")
  return data.user
}

export function logout(): void {
  clearAuthToken()
}
