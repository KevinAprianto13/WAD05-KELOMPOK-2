<template>
  <RouterView />
  <!-- Global toast notifications -->
  <div class="toast-container">
    <div
      v-for="t in toasts"
      :key="t.id"
      :class="['toast', `toast-${t.type}`]"
    >{{ t.message }}</div>
  </div>
  
  <ChatWidget />
</template>

<script setup>
import { ref, provide } from 'vue'
import ChatWidget from '@/components/ChatWidget.vue'

const toasts = ref([])
let toastId = 0

function showToast(message, type = 'info', duration = 3000) {
  const id = ++toastId
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, duration)
}

provide('toast', showToast)
</script>
