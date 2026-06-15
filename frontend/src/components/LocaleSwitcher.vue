<template>
  <div class="relative">
    <button
      @click="open = !open"
      class="fixed top-4 right-16 z-50 h-10 rounded-full glass-card-dark flex items-center gap-1.5
             hover:scale-110 active:scale-95 transition-all duration-200 shadow-lg px-3"
      title="Switch language"
    >
      <!-- Globe icon -->
      <svg class="w-5 h-5 text-gray-600 dark:text-gray-300 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="9" />
        <ellipse cx="12" cy="12" rx="4.5" ry="9" />
        <line x1="3" y1="12" x2="21" y2="12" />
        <line x1="12" y1="3" x2="12" y2="9" />
        <line x1="12" y1="15" x2="12" y2="21" />
      </svg>
      <span class="text-sm font-medium text-gray-600 dark:text-gray-300 shrink-0">{{ langLabel }}</span>
    </button>
    <div v-if="open" class="fixed top-14 right-20 z-50 w-36 glass-card-dark shadow-xl overflow-hidden">
      <button
        v-for="opt in options"
        :key="opt.value"
        @click="select(opt.value as 'zh' | 'en')"
        class="w-full px-3 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors flex items-center gap-2"
        :class="{ 'font-bold text-indigo-600 dark:text-indigo-400': locale === opt.value }"
      >
        {{ opt.label }}
        <svg v-if="locale === opt.value" class="w-3 h-3 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { locale, setLocale } from '@/i18n'

const open = ref(false)

const langLabel = computed(() => locale.value === 'zh' ? 'CN' : 'EN')

const options = [
  { label: 'CN 中文', value: 'zh' },
  { label: 'EN English', value: 'en' },
]

function select(lang: 'zh' | 'en') {
  setLocale(lang)
  open.value = false
}

// Close dropdown on outside click
document.addEventListener('click', (e) => {
  if (!open.value) return
  const btn = document.querySelector('button[title="Switch language"]')
  const dropdown = document.querySelector('.fixed.top-14.right-20')
  if (btn && !btn.contains(e.target as Node) && dropdown && !dropdown.contains(e.target as Node)) {
    open.value = false
  }
})
</script>
