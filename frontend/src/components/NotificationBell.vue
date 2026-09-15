<template>
  <div class="notification-wrapper" v-click-outside="closeDropdown">
    <!-- Bell Button -->
    <div class="bell-btn" @click="toggleDropdown">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      <span v-if="unreadCount > 0" class="notif-badge bounce-in">{{ unreadCount > 9 ? '9+' : unreadCount }}</span>
    </div>

    <!-- Dropdown Panel -->
    <transition name="dropdown-fade">
      <div v-if="isOpen" class="notif-dropdown glass">
        <div class="notif-header">
          <h4>Notifikasi</h4>
          <button v-if="unreadCount > 0" class="btn-text" @click="markAllAsRead">Tandai semua dibaca</button>
        </div>
        
        <div class="notif-list">
          <div v-if="loading" class="empty-state">Memuat...</div>
          <div v-else-if="notifications.length === 0" class="empty-state">Belum ada notifikasi</div>
          
          <div 
            v-else 
            v-for="notif in notifications" 
            :key="notif.id" 
            class="notif-item" 
            :class="{ 'unread': !notif.is_read }"
            @click="markAsRead(notif.id, notif.is_read)"
          >
            <div class="notif-icon">
              <span v-if="notif.type === 'order'">📦</span>
              <span v-else-if="notif.type === 'chat'">💬</span>
              <span v-else>ℹ️</span>
            </div>
            <div class="notif-content">
              <h5>{{ notif.title }}</h5>
              <p>{{ notif.message }}</p>
              <span class="time">{{ formatTime(notif.created_at) }}</span>
            </div>
            <div class="unread-dot" v-if="!notif.is_read"></div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { notificationApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isOpen = ref(false)
const notifications = ref([])
const loading = ref(false)
let pollInterval = null

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.is_read).length
})

const vClickOutside = {
  beforeMount(el, binding) {
    el.__clickOutsideHandler__ = (e) => {
      if (!el.contains(e.target)) binding.value(e)
    }
    document.addEventListener('click', el.__clickOutsideHandler__)
  },
  unmounted(el) {
    document.removeEventListener('click', el.__clickOutsideHandler__)
  }
}

function toggleDropdown() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    fetchNotifications()
  }
}

function closeDropdown() {
  isOpen.value = false
}

async function fetchNotifications() {
  if (!auth.isLoggedIn) return
  try {
    const res = await notificationApi.getNotifications()
    notifications.value = res.data
  } catch (err) {
    console.error("Gagal mengambil notifikasi", err)
  }
}

async function markAsRead(id, isRead) {
  if (isRead) return
  
  try {
    await notificationApi.markAsRead(id)
    const notif = notifications.value.find(n => n.id === id)
    if (notif) notif.is_read = true
  } catch (err) {
    console.error("Gagal menandai dibaca", err)
  }
}

async function markAllAsRead() {
  try {
    await notificationApi.markAllAsRead()
    notifications.value.forEach(n => n.is_read = true)
  } catch (err) {
    console.error("Gagal menandai semua dibaca", err)
  }
}

function formatTime(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString('id-ID', {
    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
  })
}

onMounted(() => {
  if (auth.isLoggedIn) {
    fetchNotifications()
    pollInterval = setInterval(fetchNotifications, 5000)
  }
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<style scoped>
.notification-wrapper {
  position: relative;
}

.bell-btn {
  position: relative;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  color: var(--text-secondary);
  transition: var(--transition-bounce);
  display: flex;
  align-items: center;
  justify-content: center;
}
.bell-btn:hover {
  color: var(--accent);
  background: var(--accent-light);
  transform: scale(1.05);
}

.notif-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: var(--danger);
  color: white;
  font-size: 0.65rem;
  font-weight: 800;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
}

.notif-dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: -10px;
  width: 340px;
  max-height: 480px;
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-glass);
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow: hidden;
  transform-origin: top right;
}

@media (max-width: 768px) {
  .notif-dropdown {
    position: fixed;
    top: auto;
    bottom: 80px;
    right: 20px;
    left: 20px;
    width: auto;
    transform-origin: bottom right;
  }
}

.notif-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--border);
  background: rgba(255,255,255,0.8);
}
.notif-header h4 { margin: 0; font-size: 1.1rem; }
.btn-text {
  background: none;
  border: none;
  color: var(--accent);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}
.btn-text:hover { text-decoration: underline; }

.notif-list {
  overflow-y: auto;
  max-height: 400px;
}
.empty-state {
  padding: 32px 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.notif-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: 0.2s;
  background: white;
}
.notif-item:hover { background: var(--bg-primary); }
.notif-item.unread { background: var(--accent-light); }

.notif-icon {
  width: 32px;
  height: 32px;
  background: var(--bg-secondary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.notif-item.unread .notif-icon { background: white; }

.notif-content {
  flex: 1;
}
.notif-content h5 { margin: 0 0 4px 0; font-size: 0.9rem; color: var(--text-primary); }
.notif-content p { margin: 0; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.4; }
.time { display: block; font-size: 0.75rem; color: var(--text-muted); margin-top: 6px; }

.unread-dot {
  width: 8px;
  height: 8px;
  background: var(--accent);
  border-radius: 50%;
  margin-top: 6px;
  flex-shrink: 0;
}

/* Animations */
.dropdown-fade-enter-active, .dropdown-fade-leave-active { transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
.dropdown-fade-enter-from, .dropdown-fade-leave-to { opacity: 0; transform: scale(0.95) translateY(10px); }
.bounce-in { animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes popIn { 0% { transform: scale(0); } 80% { transform: scale(1.2); } 100% { transform: scale(1); } }
</style>
