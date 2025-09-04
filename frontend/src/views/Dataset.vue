<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

interface ImageAsset {
  id: number
  rel_path: string
  width: number | null
  height: number | null
}

interface Dataset {
  id: number
  name: string
  images: ImageAsset[]
}

const route = useRoute()
const dataset = ref<Dataset | null>(null)

const load = async () => {
  const { data } = await api.get(`/datasets/${route.params.id}`)
  dataset.value = data
}

const upload = async (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (!files || files.length === 0) return
  const file = files[0]
  const form = new FormData()
  form.append('file', file)
  await api.post(`/datasets/${route.params.id}/upload`, form)
  await load()
}

const fileUrl = (rel: string) => `http://127.0.0.1:8000/files/${rel}`

onMounted(load)
</script>

<template>
  <div class="p-4" v-if="dataset">
    <h1 class="text-2xl mb-4">{{ dataset.name }}</h1>
    <input type="file" @change="upload" class="mb-4" />
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="img in dataset.images" :key="img.id" class="border p-1">
        <img :src="fileUrl(img.rel_path)" class="w-full" />
      </div>
    </div>
  </div>
</template>
