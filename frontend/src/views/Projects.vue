<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../api'

interface Project {
  id: number
  name: string
}

const projects = ref<Project[]>([])

onMounted(async () => {
  const { data } = await api.get('/projects')
  projects.value = data
})
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">Projects</h1>
    <ul class="space-y-2">
      <li v-for="p in projects" :key="p.id" class="p-2 bg-base-200 rounded">
        {{ p.name }}
      </li>
    </ul>
  </div>
</template>
