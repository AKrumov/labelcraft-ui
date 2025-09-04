<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../api'

interface Project {
  id: number
  name: string
}

const projects = ref<Project[]>([])
const newName = ref('')

const createProject = async () => {
  const name = newName.value.trim()
  if (!name) return
  const { data } = await api.post('/projects', { name })
  projects.value.push(data)
  newName.value = ''
}

onMounted(async () => {
  const { data } = await api.get('/projects')
  projects.value = data
})
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">Projects</h1>
    <form @submit.prevent="createProject" class="mb-4 flex gap-2">
      <input
        v-model="newName"
        placeholder="New project name"
        class="input input-bordered flex-1"
      />
      <button class="btn btn-primary" type="submit">Add</button>
    </form>
    <ul class="space-y-2">
      <li v-for="p in projects" :key="p.id" class="p-2 bg-base-200 rounded">
        {{ p.name }}
      </li>
    </ul>
  </div>
</template>
