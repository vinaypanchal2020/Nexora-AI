<script setup>
import '../styles/sidebar.css'

const emit = defineEmits(['reset-chat'])

defineProps({
  activeDocument: { type: String, default: null },
  messageCount: { type: Number, default: 0 },
  currentMode: { type: String, default: null },
  connected: { type: Boolean, default: true }
})
</script>

<template>
  <aside class="sidebar">
    <div class="brand">
      <span class="brand-mark">A&amp;A</span>
      <div>
        <h1>Archive &amp; Answer</h1>
        <p>Document-aware chat</p>
      </div>
    </div>

    <div class="ledger">
      <div class="ledger-title">Session ledger</div>

      <dl>
        <div class="row">
          <dt>Status</dt>
          <dd>
            <span class="dot" :class="connected ? 'ok' : 'bad'"></span>
            {{ connected ? 'Ready' : 'Unreachable' }}
          </dd>
        </div>
        <div class="row">
          <dt>Mode</dt>
          <dd>{{ currentMode || '—' }}</dd>
        </div>
        <div class="row">
          <dt>Document</dt>
          <dd class="doc" :title="activeDocument || ''">{{ activeDocument || 'none attached' }}</dd>
        </div>
        <div class="row">
          <dt>Messages</dt>
          <dd>{{ messageCount }}</dd>
        </div>
      </dl>
    </div>

    <div class="how">
      <div class="ledger-title">How it works</div>
      <ol>
        <li>Ask a question directly for general chat.</li>
        <li>Attach a PDF, DOCX, TXT, or image to ground answers in that document.</li>
        <li>Cited excerpts appear beneath grounded answers.</li>
      </ol>
    </div>

    <button class="new-chat-btn" type="button" @click="$emit('reset-chat')">
      New chat
    </button>
  </aside>
</template>

