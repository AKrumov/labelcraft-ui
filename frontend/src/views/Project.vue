<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import api from '../api'

interface Dataset {
  id: number
  name: string
  description: string
}

interface Project {
  id: number
  name: string
  datasets: Dataset[]
}

const route = useRoute()
const project = ref<Project | null>(null)
const newDataset = ref('')

const load = async () => {
  const { data } = await api.get(`/projects/${route.params.id}`)
  project.value = data
}

const createDataset = async () => {
  const name = newDataset.value.trim()
  if (!name) return
  const { data } = await api.post(`/datasets/${route.params.id}`, { name })
  project.value?.datasets.push(data)
  newDataset.value = ''
}

onMounted(load)
</script>

<template>
  <div class="p-4" v-if="project">
    <h1 class="text-2xl mb-4">{{ project.name }}</h1>

    <form @submit.prevent="createDataset" class="mb-4 flex gap-2">
      <input
        v-model="newDataset"
        placeholder="New dataset name"
        class="input input-bordered flex-1"
      />
      <button class="btn btn-primary" type="submit">Add Dataset</button>
    </form>

    <h2 class="text-xl mb-2">Datasets</h2>
    <ul class="space-y-2">
      <li
        v-for="d in project.datasets"
        :key="d.id"
        class="p-2 bg-base-200 rounded hover:bg-base-300"
      >
        <RouterLink :to="`/datasets/${d.id}`">{{ d.name }}</RouterLink>
      </li>
    </ul>
  </div>
</template>
