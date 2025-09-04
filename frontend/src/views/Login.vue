<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

async function submit() {
  await auth.login(email.value, password.value)
  router.push('/projects')
}
</script>

<template>
  <div class="flex items-center justify-center h-screen bg-base-200">
    <form @submit.prevent="submit" class="p-8 rounded shadow bg-base-100 space-y-4 w-80">
      <h1 class="text-xl font-bold text-center">Login</h1>
      <input v-model="email" type="email" placeholder="Email" class="input input-bordered w-full" />
      <input v-model="password" type="password" placeholder="Password" class="input input-bordered w-full" />
      <button type="submit" class="btn btn-primary w-full">Login</button>
    </form>
  </div>
</template>
