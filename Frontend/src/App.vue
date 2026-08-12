<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import Sidebar from './components/Sidebar.vue'
import MessageBubble from './components/MessageBubble.vue'
import ComposerBar from './components/ComposerBar.vue'
import LimitationsView from './components/LimitationsView.vue'
import { sendChatMessage } from './api.js'
import './styles/app.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const STORAGE_KEY = 'archive-answer-current-chat'

function loadSavedChat() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed || !Array.isArray(parsed.messages)) return null
    return parsed
  } catch (error) {
    return null
  }
}

const savedChat = loadSavedChat()
const messages = ref(savedChat?.messages || [])
const sending = ref(false)
const connected = ref(true)
const activeDocument = ref(savedChat?.activeDocument || null)
const currentMode = ref(savedChat?.currentMode || null)
const threadEl = ref(null)

watch(
  [messages, activeDocument, currentMode],
  () => {
    try {
      sessionStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          messages: messages.value,
          activeDocument: activeDocument.value,
          currentMode: currentMode.value
        })
      )
    } catch (error) {
      // ignore storage issues in restricted environments
    }
  },
  { deep: true }
)

const messageCount = computed(() => messages.value.length)

function timestamp() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function resetChat() {
  messages.value = []
  activeDocument.value = null
  currentMode.value = null
  sessionStorage.removeItem(STORAGE_KEY)
}

async function scrollToEnd() {
  await nextTick()
  threadEl.value?.scrollTo({ top: threadEl.value.scrollHeight, behavior: 'smooth' })
}

async function handleSend({ message, file }) {
  const historyForRequest = messages.value.map((entry) => ({
    role: entry.role,
    text: entry.text
  }))

  messages.value.push({
    role: 'user',
    text: message,
    fileName: file ? file.name : null,
    time: timestamp()
  })
  scrollToEnd()

  sending.value = true
  try {
    const data = await sendChatMessage(message, file, historyForRequest)
    connected.value = true
    currentMode.value = data.mode || null
    if (file) activeDocument.value = file.name

    messages.value.push({
      role: 'assistant',
      text: data.response ?? '(no response returned)',
      mode: data.mode,
      sources: data.sources || [],
      time: timestamp()
    })
  } catch (err) {
    connected.value = false
    messages.value.push({
      role: 'error',
      text: `Something went wrong reaching the backend: ${err.message}`,
      time: timestamp()
    })
  } finally {
    sending.value = false
    scrollToEnd()
  }
}
</script>

<template>
  <div class="shell">
    <Sidebar
      :active-document="activeDocument"
      :message-count="messageCount"
      :current-mode="currentMode"
      :connected="connected"
      @reset-chat="resetChat"
    />

    <main class="thread-col">
      <div class="thread" ref="threadEl">
        <div v-if="messages.length === 0" class="empty">
          <LimitationsView />
        </div>

        <MessageBubble
          v-for="(m, i) in messages"
          :key="i"
          :role="m.role"
          :text="m.text"
          :mode="m.mode"
          :sources="m.sources"
          :file-name="m.fileName"
          :time="m.time"
        />

        <div v-if="sending" class="row assistant thinking">
          <div class="bubble">
            <span class="dot-flash"></span>
            <span class="dot-flash"></span>
            <span class="dot-flash"></span>
          </div>
        </div>
      </div>

      <ComposerBar :disabled="sending" @send="handleSend" />
    </main>
  </div>
</template>

