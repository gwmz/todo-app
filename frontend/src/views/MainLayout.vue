<template>
  <div class="max-w-3xl mx-auto p-6">
    <!-- Header -->
    <header class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          My Tasks
        </h1>
        <p class="text-sm text-gray-500 mt-0.5">{{ taskCount }} tasks remaining</p>
      </div>
      <nav class="flex items-center gap-4">
        <router-link to="/settings" class="text-sm text-gray-400 hover:text-gray-600 transition-colors">Settings</router-link>
        <button @click="handleLogout" class="text-sm text-gray-400 hover:text-gray-600 transition-colors">Logout</button>
      </nav>
    </header>

    <!-- Add Task -->
    <AddTaskForm />

    <!-- Filters -->
    <div class="flex flex-wrap gap-2 mt-4 mb-4">
      <input v-model="search" class="input-field text-sm !py-2" placeholder="Search tasks..." />
      <select v-model="filterStatus" class="input-field text-sm !py-2">
        <option value="">All Status</option>
        <option value="TODO">To Do</option>
        <option value="IN_PROGRESS">In Progress</option>
        <option value="DONE">Done</option>
      </select>
      <select v-model="filterPriority" class="input-field text-sm !py-2">
        <option value="">All Priority</option>
        <option value="HIGH">High</option>
        <option value="MEDIUM">Medium</option>
        <option value="LOW">Low</option>
      </select>
    </div>

    <!-- Task List -->
    <div class="space-y-3">
      <TaskCard
        v-for="task in filteredTasks"
        :key="task.id"
        :task="task"
        @update:status="updateTaskStatus"
        @delete="deleteTask"
      />
      <p v-if="filteredTasks.length === 0" class="text-center text-gray-400 py-12 text-sm">
        No tasks yet. Add one above!
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTaskStore } from '@/stores/tasks'
import TaskCard from '@/components/TaskCard.vue'
import AddTaskForm from '@/components/AddTaskForm.vue'

const auth = useAuthStore()
const taskStore = useTaskStore()

const search = ref('')
const filterStatus = ref('')
const filterPriority = ref('')

const filteredTasks = computed(() => {
  let result = [...taskStore.tasks]
  if (filterStatus.value) result = result.filter((t) => t.status === filterStatus.value)
  if (filterPriority.value) result = result.filter((t) => t.priority === filterPriority.value)
  if (search.value) {
    const s = search.value.toLowerCase()
    result = result.filter((t) => t.title.toLowerCase().includes(s) || (t.description?.toLowerCase().includes(s)))
  }
  return result
})

const taskCount = computed(() => taskStore.tasks.filter((t) => t.status !== 'DONE').length)

function updateTaskStatus(data: { id: string; status: string }) {
  taskStore.updateTask(data.id, { status: data.status as 'TODO' | 'IN_PROGRESS' | 'DONE' })
}

function deleteTask(id: string) {
  taskStore.deleteTask(id)
}

function handleLogout() {
  auth.logout()
}

watch([filterStatus, filterPriority, search], () => {
  taskStore.filter.status = filterStatus.value
  taskStore.filter.priority = filterPriority.value
  taskStore.filter.search = search.value
  taskStore.fetchTasks()
})

onMounted(async () => {
  await Promise.all([taskStore.fetchTasks(), taskStore.fetchCategories()])
})
</script>
