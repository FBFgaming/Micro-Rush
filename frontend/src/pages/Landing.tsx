import { useState } from 'react'
import './Landing.css'

export default function Landing() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email) return

    setLoading(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    setSubmitted(true)
    setLoading(false)
  }

  return (
    <div className="landing">
      {/* Navigation */}
      <nav className="nav">
        <div className="nav-content container">
          <div className="logo">
            <span className="logo-icon">◈</span>
            <span className="logo-text">Micro Rush</span>
          </div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#privacy">Privacy</a>
            <a href="#tech">Tech</a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="hero">
        <div className="hero-bg" />
        <div className="container">
          <div className="hero-badge">
            <span className="badge-dot" />
            Privacy-first AI for your local machine
          </div>
          <h1 className="hero-title">
            Your AI Companion,
            <br />
            <span className="gradient-text">Truly Yours</span>
          </h1>
          <p className="hero-subtitle">
            Unlike cloud chatbots that forget who you are, Micro Rush lives on your hardware.
            It monitors your world, learns your preferences, and grows with you — privately.
          </p>
          <div className="hero-actions">
            {!submitted ? (
              <form onSubmit={handleSubmit} className="waitlist-form">
                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
                  {loading ? 'Joining...' : 'Join Waitlist'}
                </button>
              </form>
            ) : (
              <div className="waitlist-success">
                <span className="success-icon">✓</span>
                You're on the list! We'll be in touch soon.
              </div>
            )}
          </div>
          <div className="hero-note">
            No cloud. No subscriptions. Your data stays on your machine.
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="features">
        <div className="container">
          <h2 className="section-title">The AI You Actually Want</h2>
          <div className="features-grid">
            <FeatureCard
              icon="🛡️"
              title="Privacy First"
              description="Your personal data never leaves your hardware. Local LLMs via Ollama mean full control."
            />
            <FeatureCard
              icon="🧠"
              title="Persistent Memory"
              description="A sophisticated tiered memory system that remembers your preferences, habits, and history over months and years."
            />
            <FeatureCard
              icon="⚡"
              title="Proactive Intelligence"
              description="It doesn't wait for you to ask. Monitors your calendar, calculates traffic, and nudges you when it matters."
            />
            <FeatureCard
              icon="🔌"
              title="Extensible Skills"
              description="Dynamic plugin system means new capabilities can be added at runtime. Your AI grows with your needs."
            />
            <FeatureCard
              icon="🎨"
              title="Beautiful Interface"
              description="Dark mode React UI that feels native and responsive. Talk to your AI through a modern, intuitive interface."
            />
            <FeatureCard
              icon="🚀"
              title="Fast & Local"
              description="No API calls to distant servers. Everything runs on your machine for instant responses."
            />
          </div>
        </div>
      </section>

      {/* Privacy */}
      <section id="privacy" className="privacy">
        <div className="container">
          <div className="privacy-content">
            <h2 className="section-title">Your Data Stays Yours</h2>
            <p className="privacy-text">
              In a world where AI companies harvest your conversations to train models,
              Micro Rush takes a different approach. Everything runs locally.
            </p>
            <div className="privacy-comparison">
              <div className="comparison-item">
                <div className="item-header">
                  <span className="item-icon cloud">☁️</span>
                  <span className="item-label">Cloud AI Assistants</span>
                </div>
                <ul>
                  <li>Conversations stored on external servers</li>
                  <li>Data may be used for model training</li>
                  <li>Requires internet connection</li>
                  <li>Privacy depends on company policy</li>
                </ul>
              </div>
              <div className="comparison-item">
                <div className="item-header">
                  <span className="item-icon local">⚙️</span>
                  <span className="item-label">Micro Rush</span>
                </div>
                <ul>
                  <li>All processing happens locally</li>
                  <li>Your data never leaves your machine</li>
                  <li>Works offline after initial setup</li>
                  <li>Full privacy by architecture</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tech */}
      <section id="tech" className="tech">
        <div className="container">
          <h2 className="section-title">Built on Proven Technology</h2>
          <div className="tech-stack">
            <TechBadge name="LangGraph" description="Agent orchestration" />
            <TechBadge name="Ollama" description="Local LLM inference" />
            <TechBadge name="LanceDB" description="Vector memory" />
            <TechBadge name="FastAPI" description="Fast Python API" />
            <TechBadge name="React" description="Modern web UI" />
            <TechBadge name="SQLite" description="Persistent storage" />
          </div>
          <div className="architecture">
            <h3>The Architecture</h3>
            <div className="arch-diagram">
              <div className="arch-layer">
                <div className="arch-label">UI Layer</div>
                <div className="arch-box">React Web Interface</div>
              </div>
              <div className="arch-arrow">↑</div>
              <div className="arch-layer">
                <div className="arch-label">API Layer</div>
                <div className="arch-box">FastAPI Bridge</div>
              </div>
              <div className="arch-arrow">↑</div>
              <div className="arch-layer">
                <div className="arch-label">Agent Layer</div>
                <div className="arch-box">LangGraph Agent Loop</div>
              </div>
              <div className="arch-arrow">↑</div>
              <div className="arch-layer">
                <div className="arch-label">Memory Layer</div>
                <div className="arch-boxes">
                  <div className="arch-box small">Recall (SQL)</div>
                  <div className="arch-box small">Archival (Vector)</div>
                </div>
              </div>
              <div className="arch-arrow">↑</div>
              <div className="arch-layer">
                <div className="arch-label">Model Layer</div>
                <div className="arch-box">Ollama (Local LLM)</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-logo">
              <span className="logo-icon">◈</span>
              <span className="logo-text">Micro Rush</span>
            </div>
            <p className="footer-tagline">
              The future of personal computing, one proactive nudge at a time.
            </p>
          </div>
          <div className="footer-bottom">
            <p>Built with privacy in mind. Open source coming soon.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <div className="feature-card">
      <span className="feature-icon">{icon}</span>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  )
}

function TechBadge({ name, description }: { name: string; description: string }) {
  return (
    <div className="tech-badge">
      <span className="tech-name">{name}</span>
      <span className="tech-desc">{description}</span>
    </div>
  )
}