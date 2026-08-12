// Talks to the FastAPI backend defined in app/routes/chat_route.py.
// POST /chat expects multipart/form-data: `message` (required) and
// `file` (optional). It returns either:
//   { mode: "General Chat", response: string }
// or
//   { mode: "RAG", message: string, response: string, sources: any[] }

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

export async function sendChatMessage(message, file, history = []) {
  const form = new FormData()
  form.append('message', message)

  const normalizedHistory = history
    .filter((entry) => entry && typeof entry.text === 'string' && entry.text.trim())
    .map((entry) => ({
      role: entry.role === 'assistant' ? 'assistant' : 'user',
      content: entry.text
    }))

  form.append('history', JSON.stringify(normalizedHistory))

  if (file) {
    form.append('file', file)
  }

  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    body: form
  })

  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Request failed (${res.status}): ${text || res.statusText}`)
  }

  return res.json()
}
