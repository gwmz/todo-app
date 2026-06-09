<template>
  <div class="glass-card p-4 animate-slide-up">
    <form @submit.prevent="handleSubmit" class="space-y-3">
      <input
        v-model="title"
        class="input-field text-base font-medium"
        placeholder="What needs to be done?"
        autofocus
      />
      <div v-if="showDetails" class="space-y-3">
        <textarea
          v-model="description"
          class="input-field"
          rows="2"
          placeholder="Description..."
        />
        <div class="flex flex-wrap gap-2">
          <select v-model="priority" class="input-field text-sm">
            <option value="HIGH">High Priority</option>
            <option value="MEDIUM">Medium Priority</option>
            <option value="LOW">Low Priority</option>
          </select>
          <select v-model="status" class="input-field text-sm">
            <option value="TODO">To Do</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="DONE">Done</option>
          </select>
          <select v-model="categoryId" class="input-field text-sm">
            <option value="">No Category</option>
            <option v-for="cat in store.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
          <input v-model="dueDate" type="date" class="input-field text-sm" />
        </div>
      </div>
      <div class="flex items-center justify-between">
        <button type="button" @click="showDetails = !showDetails" class="text-sm text-gray-400 hover:text-gray-600 transition-colors">
          {{ showDetails ? '↑ Advanced' : '↓ Details' }}
        </button>
        <button type="submit" class="btn-primary px-6 py-2 text-sm">Add Task</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import type { TaskPriority, TaskStatus } from '@/types'

const store = useTaskStore()
const title = ref('')
const description = ref('')
const priority = ref<TaskPriority>('MEDIUM')
const status = ref<TaskStatus>('TODO')
const categoryId = ref('')
const dueDate = ref('')
const showDetails = ref(false)

function handleSubmit() {
  if (!title.value.trim()) return
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
