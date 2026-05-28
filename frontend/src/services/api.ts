/**
 * services/api.ts
 *
 * Base HTTP client for all API calls.
 */

import type { ApiResponse } from "@/types/api"

const BASE_PATH = import.meta.env.BASE_URL.replace(/\/$/, "")
const TOKEN_KEY = "hive_auth_token"

export function getAuthToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function setAuthToken(token: string): void {
  sessionStorage.setItem(TOKEN_KEY, token)
}

export function clearAuthToken(): void {
  sessionStorage.removeItem(TOKEN_KEY)
}

async function request<T>(
  method: string,
  path: string,
  body?: unknown
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  }

  const token = getAuthToken()
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const options: RequestInit = { method, headers }

  if (body !== undefined) {
    options.body = JSON.stringify(body)
  }

  const response = await fetch(`${BASE_PATH}${path}`, options)
  const json = (await response.json()) as ApiResponse<T>

  if (!response.ok || !json.success) {
    const errorJson = json as Extract<ApiResponse<T>, { success: false }>
    throw new Error(errorJson.error?.message ?? `HTTP ${response.status}`)
  }

  return (json as Extract<ApiResponse<T>, { success: true }>).data
}

export function get<T>(path: string): Promise<T> {
  return request<T>("GET", path)
}

export function post<T>(path: string, body: unknown): Promise<T> {
  return request<T>("POST", path, body)
}

export function put<T>(path: string, body: unknown): Promise<T> {
  return request<T>("PUT", path, body)
}

export function del<T>(path: string): Promise<T> {
  return request<T>("DELETE", path)
}
