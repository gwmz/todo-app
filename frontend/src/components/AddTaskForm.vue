<template>
  <div class="glass-card p-4 animate-slide-up">
    <form @submit.prevent="handleSubmit" class="space-y-3" novalidate>
      <input
        v-model="title"
        class="input-field text-base font-medium"
        :placeholder="t('addTask.titlePlaceholder')"
        autofocus
      />
      <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
      <div v-if="showDetails" class="space-y-3">
        <textarea
          v-model="description"
          class="input-field"
          rows="2"
          :placeholder="t('addTask.descriptionPlaceholder')"
        />
        <div class="flex flex-wrap gap-2">
          <select v-model="priority" class="input-field text-sm">
            <option value="HIGH">{{ t('addTask.highPriority') }}</option>
            <option value="MEDIUM">{{ t('addTask.mediumPriority') }}</option>
            <option value="LOW">{{ t('addTask.lowPriority') }}</option>
          </select>
          <select v-model="status" class="input-field text-sm">
            <option value="TODO">{{ t('addTask.toDo') }}</option>
            <option value="IN_PROGRESS">{{ t('addTask.inProgress') }}</option>
            <option value="DONE">{{ t('addTask.done') }}</option>
          </select>
          <select v-model="categoryId" class="input-field text-sm">
            <option value="">{{ t('addTask.noCategory') }}</option>
            <option v-for="cat in store.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
          <input v-model="dueDate" type="date" class="input-field text-sm" />
        </div>
      </div>
      <div class="flex items-center justify-between">
        <button type="button" @click="showDetails = !showDetails" class="text-sm text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors">
          {{ showDetails ? t('addTask.advanced') : t('addTask.details') }}
        </button>
        <button type="submit" class="btn-primary px-6 py-2 text-sm">{{ t('addTask.addTask') }}</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import type { TaskPriority, TaskStatus } from '@/types'
import { useTranslation } from '@/i18n'

const { t } = useTranslation()
const store = useTaskStore()
const title = ref('')
const error = ref('')
const description = ref('')
const priority = ref<TaskPriority>('MEDIUM')
const status = ref<TaskStatus>('TODO')
const categoryId = ref('')
const dueDate = ref('')
const showDetails = ref(false)

function handleSubmit() {
  if (!title.value.trim()) {
    error.value = t.value('addTask.titleRequired')
    return
  }
  error.value = ''
  store.addTask({
    title: title.value.trim(),
    description: description.value || undefined,
    priority: priority.value,
    status: status.value,
    category_id: categoryId.value || null,
    due_date: dueDate.value || null,
  })
  title.value = ''
  description.value = ''
  showDetails.value = false
}
</script>
