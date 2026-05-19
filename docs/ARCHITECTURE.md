# Micro Rush Architecture

## Overview

Micro Rush is a privacy-first personal AI assistant that runs entirely on local hardware. The architecture is designed around three core principles:

1. **Local-first**: All data processing happens on-device
2. **Agentic**: Autonomous agents that proactively help
3. **Extensible**: Plugin system for adding capabilities at runtime

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                                │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    React Web Application                         │  │
│  │                    (Dark Mode, Real-time)                       │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │ WebSocket / HTTP
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          API LAYER                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │  FastAPI Server  │  │  WebSocket Hub   │  │   REST Endpoints     │  │
│  │  (Bridge)        │  │  (Chat Loop)     │  │   (Health, Config)   │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        AGENT LAYER                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    LangGraph Agent Loop                          │   │
│  │                                                                   │   │
│  │   ┌───────────┐   ┌──────────┐   ┌─────────┐   ┌────────────┐   │   │
│  │   │ Load      │──▶│ Think    │──▶│ Act     │──▶│ Remember   │   │   │
│  │   │ Memory    │   │ (ReAct)  │   │ (Skill) │   │ (Update)   │   │   │
│  │   └───────────┘   └──────────┘   └─────────┘   └────────────┘   │   │
│  │                                                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
┌──────────────────────────────┐     ┌──────────────────────────────────────┐
│       MEMORY LAYER           │     │          SKILL LAYER                  │
│  ┌────────────────────────┐ │     │  ┌─────────────┐  ┌─────────────┐    │
│  │  RECALL (SQLite)        │ │     │  │  Calendar   │  │   Files     │    │
│  │                         │ │     │  │  Plugin     │  │   Plugin    │    │
│  │  Hard facts & prefs     │ │     │  └─────────────┘  └─────────────┘    │
│  │  - Stated preferences   │ │     │  ┌─────────────┐  ┌─────────────┐    │
│  │  - Exact rememberings   │ │     │  │  Health     │  │  Finance    │    │
│  │  - Key-value facts     │ │     │  │  Plugin     │  │  Plugin     │    │
│  └────────────────────────┘ │     │  └─────────────┘  └─────────────┘    │
│  ┌────────────────────────┐ │     │                                      │
│  │  ARCHIVAL (LanceDB)     │ │     │           Plugin Registry           │
│  │                         │ │     │        (Dynamic Loading)           │
│  │  Conceptual history    │ │     └──────────────────────────────────────┘
│  │  - Conversation summary │
│  │  - Learned patterns    │
│  │  - Vector embeddings   │
│  └────────────────────────┘ │
└──────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       MODEL LAYER                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Ollama (Local LLM)                           │   │
│  │                                                                   │   │
│  │   Model: llama3.2                                                 │   │
│  │   Embeddings: nomic-embed-text                                    │   │
│  │   Base URL: http://localhost:11434                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### The Brain — Tiered Memory

Two complementary memory systems work together:

#### Recall Memory (SQLite)
- **Purpose**: Store hard facts and explicit preferences
- **Schema**: Key-value with categories
- **Use cases**:
  - User-stated preferences ("black coffee, no sugar")
  - Important dates and commitments
  - Relationships and roles
  - Configuration settings

#### Archival Memory (LanceDB)
- **Purpose**: Store conceptual history and learned patterns
- **Implementation**: Vector embeddings for semantic search
- **Use cases**:
  - Conversation summaries
  - Behavioral patterns over time
  - Contextual associations
  - Broader historical context

### The Body — Plugin System

Skills are implemented as plugins with a common interface:

```python
class Plugin(ABC):
    name: str
    description: str
    
    def execute(self, context: dict) -> dict:
        """Main execution method."""
        ...
    
    def validate(self, context: dict) -> bool:
        """Check if this plugin should handle the request."""
        ...
```

**Lifecycle**:
1. Plugin discovered at startup
2. Registry maintains plugin instances
3. Agent routes requests based on skill match
4. Plugin returns structured result

### The Face — Web UI

React application with:
- Dark mode interface
- Real-time WebSocket chat
- Responsive design
- Waitlist signup form

---

## Data Flow

### Chat Flow
```
1. User types message in React UI
2. WebSocket sends to FastAPI /api/chat/ws
3. FastAPI passes to Agent
4. Agent loads context from Recall + Archival
5. Agent runs ReAct loop with Ollama
6. Agent updates memory if needed
7. Response streamed back via WebSocket
8. React UI displays response
```

### Proactive Flow
```
1. Skill (Calendar) triggers on schedule
2. Skill checks for upcoming meetings
3. Skill calculates traffic/commute time
4. Skill formats proactive nudge
5. Agent sends notification via UI
6. Memory updated with action taken
```

---

## Directory Structure

```
micro-rush/
├── backend/
│   ├── src/microrush/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── app.py          # FastAPI entry point
│   │   │   ├── chat.py         # WebSocket chat endpoint
│   │   │   └── health.py       # Health check
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── agent.py        # LangGraph agent
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   ├── recall.py       # SQL memory
│   │   │   └── archival.py     # Vector memory
│   │   ├── plugins/
│   │   │   ├── __init__.py    # Plugin base class + registry
│   │   ├── skills/
│   │   │   ├── calendar/
│   │   │   │   ├── __init__.py
│   │   │   │   └── plugin.py
│   │   │   └── files/
│   │   │       ├── __init__.py
│   │   │       └── plugin.py
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Landing.tsx
│   │   │   └── Landing.css
│   │   └── hooks/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docs/
│   └── ARCHITECTURE.md
├── COMPANY.md
├── TASKS.md
├── README.md
├── GETTING_STARTED.md
└── docker-compose.yml
```

---

## Security Model

- **No external data transmission**: All processing local
- **User-controlled models**: Can swap LLM anytime
- **Isolated memory**: Each user has separate database
- **No telemetry**: Zero tracking or analytics

---

## Scaling Considerations

### Current (Single User)
- SQLite for memory (sufficient for personal use)
- Single Ollama instance
- One WebSocket connection

### Future (Multi-User)
- PostgreSQL replacement for Recall
- LanceDB server mode
- Ollama with multiple model slots
- Redis for session management

---

## Technology Choices

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Agent Framework | LangGraph | Best-in-class for agentic workflows |
| LLM | Ollama | Mature local inference solution |
| Vector DB | LanceDB | Fast, embedded, no server needed |
| SQL | SQLite | Zero config, sufficient for single user |
| API | FastAPI | Fast, async, great docs |
| Frontend | React + Vite | Modern, fast HMR |
| Deployment | Docker Compose | Simple local development |