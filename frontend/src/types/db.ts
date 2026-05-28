/**
 * types/db.ts
 *
 * Types for database connection status, metrics, and template users.
 */

export interface DbDetails {
  version?: string;
  active_connections?: number;
  database_size?: string;
  dialect?: string;
}

export interface DbStatus {
  connected: boolean;
  engine: string;
  url: string;
  fallback_active: boolean;
  error: string | null;
  warning?: string;
  tables?: string[];
  details?: DbDetails;
  meta_error?: string;
}

export interface Department {
  id: number;
  name: string;
  description: string | null;
  owner_user_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  username: string;
  full_name: string;
  profile_image_url?: string | null;
  email: string | null;
  role: string;
  department_id: number | null;
  department_name?: string | null;
  is_active: boolean;
  team_id?: number | null;
  created_at: string;
  updated_at: string;
}

export interface UserFormData {
  username: string;
  full_name: string;
  password?: string;
  email?: string;
  role?: string;
  department_id?: number;
}
