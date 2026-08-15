<script setup>
import { ref } from 'vue'
import '../styles/composer.css'

const props = defineProps({
  disabled: { type: Boolean, default: false }
})
const emit = defineEmits(['send'])

const text = ref('')
const file = ref(null)
const fileInput = ref(null)

function pickFile() {
  fileInput.value?.click()
}

function onFileChange(e) {
  file.value = e.target.files?.[0] || null
}

function clearFile() {
  file.value = null
  if (fileInput.value) fileInput.value.value = ''
}

function submit() {
  const trimmed = text.value.trim()
  if (!trimmed || props.disabled) return
  emit('send', { message: trimmed, file: file.value })
  text.value = ''
  clearFile()
}

function onKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submit()
  }
}
</script>

<template>
  <div class="composer">
    <div v-if="file" class="staged">
      <span class="pin"></span>
      <span class="staged-name">{{ file.name }}</span>
      <button type="button" class="staged-remove" @click="clearFile" aria-label="Remove attached file">
        ×
      </button>
    </div>

    <div class="input-row">
      <button
        type="button"
        class="attach-btn"
        @click="pickFile"
        :disabled="disabled"
        title="Attach a document"
        aria-label="Attach a document"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M21 11.5V7a2 2 0 0 0-2-2H8.5L4 9.5V19a2 2 0 0 0 2 2h6" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M4 9.5H8.5V5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M15 15v4M13 17h4" stroke-linecap="round"/>
        </svg>
      </button>
      <input
        ref="fileInput"
        type="file"
        class="hidden-input"
        accept=".pdf,.docx,.txt"
        @change="onFileChange"
      />

      <textarea
        v-model="text"
        rows="1"
        class="text-input"
        placeholder="Ask a question, or attach a document first…"
        :disabled="disabled"
        @keydown="onKeydown"
      ></textarea>

      <button type="button" class="send-btn" :disabled="disabled || !text.trim()" @click="submit">
        {{ disabled ? 'Sending…' : 'Send' }}
      </button>
    </div>
    <p class="hint">Enter to send · Shift+Enter for a new line</p>
  </div>
</template>

