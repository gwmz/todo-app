<template>
  <div class="max-w-3xl mx-auto p-6">
    <!-- Header -->
    <header class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          {{ t('main.title') }}
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{{ taskCount }} {{ t('main.tasksRemaining') }}</p>
      </div>
      <nav class="flex items-center gap-4">
        <router-link to="/settings" class="text-sm text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors">{{ t('main.settings') }}</router-link>
        <button @click="handleLogout" class="text-sm text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors">{{ t('main.logout') }}</button>
      </nav>
    </header>

    <!-- Add Task -->
    <AddTaskForm />

    <!-- Filters -->
    <div class="flex flex-wrap gap-2 mt-4 mb-4">
      <input v-model="search" class="input-field text-sm !py-2" :placeholder="t('main.searchPlaceholder')" />
      <select v-model="filterStatus" class="input-field text-sm !py-2">
        <option value="">{{ t('main.allStatus') }}</option>
        <option value="TODO">{{ t('main.toDo') }}</option>
        <option value="IN_PROGRESS">{{ t('main.inProgress') }}</option>
        <option value="DONE">{{ t('main.done') }}</option>
      </select>
      <select v-model="filterPriority" class="input-field text-sm !py-2">
        <option value="">{{ t('main.allPriority') }}</option>
        <option value="HIGH">{{ t('main.high') }}</option>
        <option value="MEDIUM">{{ t('main.medium') }}</option>
        <option value="LOW">{{ t('main.low') }}</option>
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
      <p v-if="filteredTasks.length === 0" class="text-center text-gray-400 dark:text-gray-500 py-12 text-sm">
        {{ t('main.noTasks') }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTaskStore } from '@/stores/tasks'
import TaskCard from '@/components/TaskCard.vue'
import AddTaskForm from '@/components/AddTaskForm.vue'
import { useTranslation } from '@/i18n'

const { t } = useTranslation()
const router = useRouter()

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
  router.push('/login')
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
