import { useState, useRef, useEffect } from 'react'
import './Chat.css'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hi! I'm Micro Rush, your privacy-first personal AI assistant. Everything here stays on your machine. How can I help you today?",
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [connected, setConnected] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('/api/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: userMessage.content,
          session_id: 'default'
        })
      })

      if (response.ok) {
        const data = await response.json()
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.content,
          timestamp: new Date(data.timestamp)
        }])
        setConnected(true)
      } else {
        throw new Error('API error')
      }
    } catch (error) {
      // Fallback demo response if API not available
      const demoResponses = [
        "I'm running locally on your machine! No data is being sent anywhere.",
        "Your privacy is protected — all processing happens right here.",
        "I'd love to help you get organized. Want me to check your calendar?",
        "I'm here to assist you. What would you like to work on today?"
      ]
      setTimeout(() => {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: demoResponses[Math.floor(Math.random() * demoResponses.length)],
          timestamp: new Date()
        }])
      }, 500)
    }

    setLoading(false)
  }

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-status">
          <span className={`status-dot ${connected ? 'connected' : ''}`} />
          <span className="status-text">{connected ? 'Connected to Micro Rush' : 'Ready'}</span>
        </div>
        <div className="chat-title">
          <span className="logo-icon">◈</span>
          <span>Micro Rush</span>
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'assistant' ? '◈' : '👤'}
            </div>
            <div className="message-content">
              <p>{msg.content}</p>
              <span className="message-time">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-avatar">◈</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form className="chat-input" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything..."
          disabled={loading}
        />
        <button type="submit" disabled={!input.trim() || loading}>
          {loading ? '...' : '→'}
        </button>
      </form>
    </div>
  )
}