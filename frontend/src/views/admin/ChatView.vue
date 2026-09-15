<template>
  <div class="chat-dashboard">
    <div class="dash-header">
      <h1>Chat Inbox</h1>
      <p class="text-secondary">Kelola pesan dari pelanggan</p>
    </div>

    <div class="chat-container card">
      <!-- Sidebar (Sessions) -->
      <div class="chat-sidebar">
        <div v-if="sessionsLoading" class="loading-center"><div class="spinner"></div></div>
        <div v-else-if="sessions.length === 0" class="empty-state">
          Belum ada percakapan
        </div>
        <div v-else class="session-list">
          <div 
            v-for="session in sessions" 
            :key="session.user.id" 
            class="session-item"
            :class="{ active: selectedUser?.id === session.user.id }"
            @click="selectUser(session.user)"
          >
            <div class="session-avatar">
              <img :src="`https://ui-avatars.com/api/?name=${session.user.full_name}&background=random&color=fff`" />
              <div v-if="session.unread_count > 0" class="unread-badge">{{ session.unread_count }}</div>
            </div>
            <div class="session-info">
              <div class="session-name">{{ session.user.full_name }}</div>
              <div class="session-last-msg text-muted">{{ session.last_message.content }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Chat Area -->
      <div class="chat-main">
        <div v-if="!selectedUser" class="empty-state">
          <div class="icon">💬</div>
          <h3>Pilih percakapan</h3>
          <p>Pilih dari daftar di sebelah kiri untuk mulai mengobrol.</p>
        </div>
        <template v-else>
          <div class="chat-main-header">
            <h4>{{ selectedUser.full_name }}</h4>
            <span class="text-sm text-muted">{{ selectedUser.email }}</span>
          </div>

          <div class="chat-messages" ref="messagesContainer">
            <div v-if="messagesLoading" class="loading-center"><div class="spinner"></div></div>
            <div v-else v-for="msg in messages" :key="msg.id" class="message-row" :class="{'my-message': msg.sender_id === auth.user.id}">
              <div class="message-bubble">{{ msg.content }}</div>
              <div class="message-time">{{ formatTime(msg.created_at) }}</div>
            </div>
          </div>

          <div class="chat-input-area">
            <input type="text" v-model="newMessage" placeholder="Ketik balasan..." @keyup.enter="sendMessage" :disabled="sending" />
            <button @click="sendMessage" :disabled="!newMessage.trim() || sending" class="btn btn-primary">
              Kirim
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { chatApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const sessions = ref([])
const messages = ref([])
const selectedUser = ref(null)

const sessionsLoading = ref(false)
const messagesLoading = ref(false)
const sending = ref(false)
const newMessage = ref('')

const messagesContainer = ref(null)
let pollInterval = null

async function loadSessions() {
  try {
    const res = await chatApi.getSessions()
    sessions.value = res.data
  } catch (error) {
    console.error("Gagal memuat sesi", error)
  }
}

async function selectUser(user) {
  selectedUser.value = user
  messagesLoading.value = true
  await loadMessages()
  messagesLoading.value = false
  
  loadSessions()
}

async function loadMessages() {
  if (!selectedUser.value) return
  try {
    const res = await chatApi.getMessages(selectedUser.value.id)
    messages.value = res.data
    scrollToBottom()
  } catch (error) {
    console.error("Gagal memuat pesan", error)
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || sending.value || !selectedUser.value) return
  
  const content = newMessage.value
  newMessage.value = ''
  sending.value = true
  
  try {
    const res = await chatApi.sendMessage({ receiver_id: selectedUser.value.id, content })
    messages.value.push(res.data)
    scrollToBottom()
    loadSessions()
  } catch (error) {
    console.error("Gagal mengirim chat", error)
  } finally {
    sending.value = false
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function formatTime(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })
}

function startPolling() {
  pollInterval = setInterval(() => {
    loadSessions()
    if (selectedUser.value) {
      loadMessages()
    }
  }, 3000)
}

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

onMounted(() => {
  sessionsLoading.value = true
  loadSessions().finally(() => {
    sessionsLoading.value = false
  })
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.chat-dashboard { max-width: 1200px; }
.dash-header { margin-bottom: 32px; }
.chat-container {
  display: flex;
  height: 70vh;
  min-height: 500px;
  overflow: hidden;
  padding: 0;
}

/* Sidebar */
.chat-sidebar {
  width: 320px;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
}
.session-list {
  flex: 1;
  overflow-y: auto;
}
.session-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  cursor: pointer;
  border-bottom: 1px solid var(--border);
  transition: var(--transition);
}
.session-item:hover {
  background: rgba(255,255,255,0.5);
}
.session-item.active {
  background: white;
  border-left: 4px solid var(--accent);
}
.session-avatar {
  position: relative;
}
.session-avatar img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}
.unread-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--danger);
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}
.session-info {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.session-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.session-last-msg {
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Main Chat Area */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}
.chat-main-header {
  padding: 20px;
  border-bottom: 1px solid var(--border);
  background: white;
}
.chat-main-header h4 { margin: 0 0 4px 0; }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #f8fafc;
}
.message-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 70%;
}
.message-row.my-message {
  align-items: flex-end;
  align-self: flex-end;
}
.message-bubble {
  padding: 12px 16px;
  border-radius: 16px;
  background: white;
  color: var(--text-primary);
  border: 1px solid var(--border);
  border-bottom-left-radius: 4px;
  font-size: 0.95rem;
}
.message-row.my-message .message-bubble {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 4px;
}
.message-time {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 6px;
}

.chat-input-area {
  padding: 20px;
  background: white;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 16px;
}
.chat-input-area input {
  flex: 1;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  outline: none;
  font-size: 0.95rem;
}
.chat-input-area input:focus {
  border-color: var(--accent);
}
.chat-input-area button {
  min-width: 100px;
}
</style>
