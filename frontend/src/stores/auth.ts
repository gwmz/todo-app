import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/client'
import type { User, Token } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  async function login(username: string, password: string) {
    const res = await api.post<Token>('/auth/login', { username, password })
    token.value = res.data.access_token
    localStorage.setItem('token', res.data.access_token)
    await fetchUser()
  }

  async function register(username: string, password: string, email?: string) {
    await api.post('/auth/register', { username, password, email })
  }

  async function fetchUser() {
    try {
      const res = await api.get<User>('/auth/me')
      user.value = res.data
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return { user, token, login, register, fetchUser, logout }
})
