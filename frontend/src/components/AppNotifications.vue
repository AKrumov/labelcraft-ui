<template>
  <div class="toast toast-top toast-end">
    <div
      v-for="n in notify.items"
      :key="n.id"
      class="alert"
      :class="n.type === 'error' ? 'alert-error' : 'alert-success'"
    >
      <span>{{ n.message }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '../stores/notifications'
const notify = useNotificationStore()
</script>
