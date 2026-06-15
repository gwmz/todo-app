<template>
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="glass-card p-8 w-full max-w-md animate-scale-in">
      <h1 class="text-3xl font-bold text-center bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">
        {{ t('login.title') }}
      </h1>
      <p class="text-center text-gray-500 dark:text-gray-400 mb-8">{{ t('login.subtitle') }}</p>

      <form @submit.prevent="handleLogin" class="space-y-4" novalidate>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('login.username') }}</label>
          <input v-model="username" class="input-field" :placeholder="t('login.usernamePlaceholder')" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('login.password') }}</label>
          <input v-model="password" type="password" class="input-field" :placeholder="t('login.passwordPlaceholder')" />
        </div>
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        <button type="submit" class="btn-primary w-full py-3" :disabled="loading">
          {{ loading ? t('login.signingIn') : t('login.signIn') }}
        </button>
      </form>

      <p class="text-center text-gray-500 dark:text-gray-400 mt-6">
        {{ t('login.noAccount') }}
        <router-link to="/register" class="text-indigo-500 hover:underline">{{ t('login.register') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTranslation } from '@/i18n'

const { t } = useTranslation()
const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  if (!username.value.trim()) {
    error.value = t.value('login.required')
    return
  }
  if (!password.value) {
    error.value = t.value('login.required')
    return
  }
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
