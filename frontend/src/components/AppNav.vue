<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="navbar bg-base-300">
    <div class="flex-1">
      <RouterLink to="/projects" class="btn btn-ghost normal-case text-xl">LabelCraft</RouterLink>
    </div>
    <div class="flex-none">
      <button class="btn btn-ghost" @click="$emit('logout')">Logout</button>
    </div>
  </div>
</template>
