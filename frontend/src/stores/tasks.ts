import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/client'
import type { Task, Category, TaskStatus, TaskPriority } from '@/types'

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])
  const categories = ref<Category[]>([])
  const filter = ref({ status: '', priority: '', category: '', search: '' })

  async function fetchTasks() {
    const params: Record<string, string> = {}
    if (filter.value.status) params.status = filter.value.status
    if (filter.value.priority) params.priority = filter.value.priority
    if (filter.value.category) params.category = filter.value.category
    if (filter.value.search) params.search = filter.value.search

    const res = await api.get<Task[]>('/tasks', { params })
    tasks.value = res.data
  }

  async function fetchCategories() {
    const res = await api.get<Category[]>('/categories')
    categories.value = res.data
  }

  async function addTask(data: {
    title: string
    description?: string
    status?: TaskStatus
    priority?: TaskPriority
    due_date?: string | null
    reminder_enabled?: boolean
    category_id?: string | null
  }) {
    await api.post('/tasks', data)
    await fetchTasks()
  }

  async function updateTask(id: string, data: Partial<Task>) {
    await api.put(`/tasks/${id}`, data)
    await fetchTasks()
  }

  async function deleteTask(id: string) {
    await api.delete(`/tasks/${id}`)
    await fetchTasks()
  }

  return { tasks, categories, filter, fetchTasks, fetchCategories, addTask, updateTask, deleteTask }
})
