<template>
  <div class="tutor-view">
    <el-card class="chat-card">
      <template #header>
        <span>AI Tutor</span>
      </template>

      <div class="chat-container" ref="chatContainer">
        <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
          <div class="message-content">{{ msg.content }}</div>
        </div>
      </div>

      <div class="chat-input">
        <el-input v-model="inputMessage" placeholder="Ask me anything..." @keyup.enter="sendMessage">
          <template #append>
            <el-button :disabled="!inputMessage.trim() || sending" @click="sendMessage">
              Send
            </el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '@/api/axios'
import type { ChatMessage } from '@/types'

const sessionId = ref(`session_${Date.now()}`)
const messages = ref<ChatMessage[]>([])
const inputMessage = ref('')
const sending = ref(false)
const chatContainer = ref<HTMLElement>()

async function sendMessage() {
  if (!inputMessage.value.trim() || sending.value) return

  const userMessage = inputMessage.value.trim()
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  sending.value = true

  try {
    const response = await apiClient.post('/tutor/chat', {
      session_id: sessionId.value,
      message: userMessage,
    })
    messages.value.push({ role: 'assistant', content: response.data.response })
    await scrollToBottom()
  } catch (error: any) {
    ElMessage.error('Failed to get response')
  } finally {
    sending.value = false
  }
}

async function scrollToBottom() {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.tutor-view {
  padding: 20px;
  height: calc(100vh - 120px);
}

.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 70%;
}

.message.user {
  align-self: flex-end;
}

.message.assistant {
  align-self: flex-start;
}

.message-content {
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
}

.message.user .message-content {
  background: #409eff;
  color: white;
}

.message.assistant .message-content {
  background: #f5f5f5;
  color: #333;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #eee;
}
</style>
