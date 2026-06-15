<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-slate-900 dark:to-indigo-950 transition-colors duration-300">
    <!-- Theme Toggle -->
    <LocaleSwitcher />
    <button
      @click="themeStore.toggle"
      class="fixed top-4 right-4 z-50 w-10 h-10 rounded-full glass-card-dark flex items-center justify-center
             hover:scale-110 active:scale-95 transition-all duration-200 shadow-lg"
      :title="themeStore.isDark ? 'Light mode' : 'Dark mode'"
    >
      <svg v-if="!themeStore.isDark" class="w-5 h-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
      </svg>
      <svg v-else class="w-5 h-5 text-amber-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
    </button>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { useThemeStore } from '@/stores/theme'
import LocaleSwitcher from '@/components/LocaleSwitcher.vue'
const themeStore = useThemeStore()
themeStore.init()
</script>
