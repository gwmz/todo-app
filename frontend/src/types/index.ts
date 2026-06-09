export interface User {
  id: string
  username: string
  email: string | null
  created_at: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface Category {
  id: string
  name: string
  color: string
  user_id: string
  created_at: string
}

export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE'
export type TaskPriority = 'HIGH' | 'MEDIUM' | 'LOW'

export interface Task {
  id: string
  title: string
  description: string | null
  status: TaskStatus
  priority: TaskPriority
  due_date: string | null
  reminder_enabled: boolean
  category_id: string | null
  created_at: string
  updated_at: string
  completed_at: string | null
  user_id: string
  category: Category | null
}
