<script setup lang="ts">
import AppNav from './components/AppNav.vue'
import AppNotifications from './components/AppNotifications.vue'
import { useAuthStore } from './stores/auth'
import { useNotificationStore } from './stores/notifications'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const notify = useNotificationStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  notify.notify('Logged out', 'success')
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-base-200 text-base-content">
    <AppNav v-if="auth.token" @logout="handleLogout" />
    <AppNotifications />
    <router-view />
  </div>
</template>
