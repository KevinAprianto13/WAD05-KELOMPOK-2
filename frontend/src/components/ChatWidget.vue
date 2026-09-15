<template>
  <div class="chat-widget" v-if="auth.isLoggedIn && auth.user?.role === 'customer'">
    <!-- Chat Button -->
    <button class="chat-toggle-btn" @click="toggleChat">
      <svg v-if="!isOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>

    <!-- Chat Box -->
    <div class="chat-box glass" :class="{ 'open': isOpen }">
      <div class="chat-header">
        <h4>Chat dengan Admin</h4>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div v-if="loading" class="chat-loading">Memuat pesan...</div>
        <div v-else-if="messages.length === 0" class="chat-empty">
          Belum ada pesan. Silakan tanya sesuatu!
        </div>
        <div v-else v-for="msg in messages" :key="msg.id" class="message-row" :class="{'my-message': msg.sender_id === auth.user.id}">
          <div class="message-bubble">{{ msg.content }}</div>
          <div class="message-time">{{ formatTime(msg.created_at) }}</div>
        </div>
      </div>
      
      <div class="chat-input-area">
        <input type="text" v-model="newMessage" placeholder="Ketik pesan..." @keyup.enter="sendMessage" :disabled="sending" />
        <button @click="sendMessage" :disabled="!newMessage.trim() || sending">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, nextTick } from 'vue'
import { chatApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isOpen = ref(false)
const messages = ref([])
const newMessage = ref('')
const loading = ref(false)
const sending = ref(false)
const messagesContainer = ref(null)
let pollInterval = null

function toggleChat() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    fetchMessages()
    startPolling()
  } else {
    stopPolling()
  }
}

async function fetchMessages() {
  if (!auth.isLoggedIn || auth.user.role !== 'customer') return
  try {
    // 0 is passed so the backend can infer the correct admin ID
    const res = await chatApi.getMessages(0) 
    messages.value = res.data
    scrollToBottom()
  } catch (error) {
    console.error("Gagal mengambil chat", error)
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || sending.value) return
  
  const content = newMessage.value
  newMessage.value = ''
  sending.value = true
  
  try {
    const res = await chatApi.sendMessage({ receiver_id: 0, content })
    messages.value.push(res.data)
    scrollToBottom()
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
    fetchMessages()
  }, 3000)
}

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.chat-widget {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.chat-toggle-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--accent-gradient);
  color: white;
  border: none;
  box-shadow: 0 4px 12px var(--accent-glow);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s;
}
.chat-toggle-btn:hover {
  transform: scale(1.05);
}

.chat-box {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 320px;
  height: 400px;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  border: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  opacity: 0;
  pointer-events: none;
  transform: translateY(20px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-box.open {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}

.chat-header {
  padding: 16px;
  background: var(--accent);
  color: white;
  font-weight: 600;
}
.chat-header h4 { margin: 0; }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: var(--bg-primary);
}

.chat-loading, .chat-empty {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-top: 20px;
}

.message-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.message-row.my-message {
  align-items: flex-end;
}

.message-bubble {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 0.9rem;
  line-height: 1.4;
  background: white;
  color: var(--text-primary);
  border: 1px solid var(--border);
  border-bottom-left-radius: 4px;
}
.message-row.my-message .message-bubble {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 4px;
}

.message-time {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-top: 4px;
}

.chat-input-area {
  padding: 12px;
  background: white;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 8px;
}
.chat-input-area input {
  flex: 1;
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 8px 12px;
  font-size: 0.9rem;
  outline: none;
}
.chat-input-area input:focus {
  border-color: var(--accent);
}
.chat-input-area button {
  background: var(--accent);
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.2s;
}
.chat-input-area button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
