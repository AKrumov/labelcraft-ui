<script setup lang="ts">
import AppNav from './components/AppNav.vue'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-base-200 text-base-content">
    <AppNav v-if="auth.token" @logout="handleLogout" />
    <router-view />
  </div>
</template>
