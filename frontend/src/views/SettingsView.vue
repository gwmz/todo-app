<template>
  <div class="max-w-2xl mx-auto p-6">
    <header class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Categories</h1>
      <p class="text-sm text-gray-500 mt-0.5">Organize your tasks</p>
    </header>

    <!-- Add Category -->
    <div class="glass-card p-4 mb-6">
      <form @submit.prevent="addCategory" class="flex gap-3">
        <input v-model="newName" class="input-field" placeholder="Category name" required />
        <input v-model="newColor" type="color" class="w-10 h-10 rounded-lg border-0 cursor-pointer" />
        <button type="submit" class="btn-primary">Add</button>
      </form>
    </div>

    <!-- Category List -->
    <div class="space-y-2">
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="glass-card p-4 flex items-center justify-between"
      >
        <div class="flex items-center gap-3">
          <div class="w-4 h-4 rounded-full" :style="{ backgroundColor: cat.color }" />
          <span class="font-medium">{{ cat.name }}</span>
        </div>
        <button @click="deleteCategory(cat.id)" class="text-gray-300 hover:text-red-400 transition-colors">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/tasks'

const store = useTaskStore()

const newName = ref('')
const newColor = ref('#6366f1')

const categories = computed(() => store.categories)

async function addCategory() {
  if (!newName.value.trim()) return
  await store.addCategory({ name: newName.value.trim(), color: newColor.value })
  newName.value = ''
}

async function deleteCategory(id: string) {
  await store.deleteCategory(id)
}

onMounted(() => store.fetchCategories())
</script>
