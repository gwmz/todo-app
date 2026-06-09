<template>
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="glass-card p-8 w-full max-w-md animate-scale-in">
      <h1 class="text-3xl font-bold text-center bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">
        TODO
      </h1>
      <p class="text-center text-gray-500 mb-8">Create your account</p>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input v-model="username" class="input-field" placeholder="your username" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input v-model="password" type="password" class="input-field" placeholder="••••••••" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email (optional)</label>
          <input v-model="email" type="email" class="input-field" placeholder="you@example.com" />
        </div>
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        <button type="submit" class="btn-primary w-full py-3" :disabled="loading">
          {{ loading ? 'Creating account...' : 'Register' }}
        </button>
      </form>

      <p class="text-center text-gray-500 mt-6">
        Already have an account?
        <router-link to="/login" class="text-indigo-500 hover:underline">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const email = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await auth.register(username.value, password.value, email.value)
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
