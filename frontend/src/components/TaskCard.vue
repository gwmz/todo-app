<template>
  <div
    class="glass-card p-4 transition-all duration-200 hover:shadow-xl hover:-translate-y-0.5 animate-fade-in"
  >
    <div class="flex items-start gap-3">
      <!-- Checkbox -->
      <button
        @click="toggleDone"
        class="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all duration-200"
        :class="[
          task.status === 'DONE'
            ? 'bg-gradient-to-r from-green-400 to-emerald-500 border-transparent'
            : 'border-gray-300 hover:border-indigo-400',
        ]"
      >
        <svg v-if="task.status === 'DONE'" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </button>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <h3
          class="font-medium"
          :class="[
            task.status === 'DONE' ? 'line-through text-gray-400' : 'text-gray-800',
          ]"
        >
          {{ task.title }}
        </h3>
        <p v-if="task.description" class="text-sm text-gray-500 mt-1 line-clamp-2">{{ task.description }}</p>

        <!-- Tags -->
        <div class="flex flex-wrap gap-1.5 mt-2">
          <span
            v-if="task.category"
            class="text-xs px-2 py-0.5 rounded-full"
            :style="{ backgroundColor: task.category.color + '20', color: task.category.color }"
          >
            {{ task.category.name }}
          </span>
          <span
            v-if="task.priority === 'HIGH'"
            class="text-xs px-2 py-0.5 rounded-full bg-red-100 text-red-600"
          >
            High
          </span>
          <span
            v-if="task.priority === 'MEDIUM'"
            class="text-xs px-2 py-0.5 rounded-full bg-orange-100 text-orange-600"
          >
            Medium
          </span>
          <span
            v-if="task.priority === 'LOW'"
            class="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-600"
          >
            Low
          </span>
          <span
            v-if="task.due_date"
            class="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-500"
          >
            Due: {{ new Date(task.due_date).toLocaleDateString() }}
          </span>
        </div>
      </div>

      <!-- Delete -->
      <button @click="handleDelete" class="text-gray-300 hover:text-red-400 transition-colors">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '@/types'

const props = defineProps<{ task: Task }>()
const emit = defineEmits<{
  'update:status': [{ id: string; status: string }]
  delete: [id: string]
}>()

function toggleDone() {
  const next = props.task.status === 'DONE' ? 'TODO' : 'DONE'
  emit('update:status', { id: props.task.id, status: next })
}

function handleDelete() {
  emit('delete', props.task.id)
}
</script>
