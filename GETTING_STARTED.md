# Getting Started with Micro Rush

Your privacy-first personal AI assistant that runs entirely on your local machine.

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama (for local LLM inference)

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows (WSL2 recommended)
# Follow instructions at https://ollama.com
```

### 2. Download the LLM

```bash
ollama pull llama3.2
```

### 3. Set Up Backend

```bash
cd micro-rush/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Copy environment file
cp .env.example .env

# Run the API
uvicorn microrush.api.app:app --reload --port 8000
```

### 4. Set Up Frontend

```bash
cd micro-rush/frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

### 5. Open in Browser

- Frontend: http://localhost:5173
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Docker Setup (Recommended)

```bash
cd micro-rush

# Start all services (backend, frontend, Ollama)
docker-compose up
```

> **Note:** The Docker setup includes Ollama with GPU support. Make sure you have [Docker NVIDIA runtime](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) configured.

---

## Project Structure

```
micro-rush/
├── backend/
│   ├── src/microrush/
│   │   ├── agents/         # LangGraph agent loop
│   │   ├── api/           # FastAPI routes
│   │   ├── memory/        # Recall + Archival memory
│   │   ├── plugins/        # Plugin base class
│   │   └── skills/         # Skill implementations
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   └── hooks/          # Custom React hooks
│   ├── package.json
│   └── Dockerfile
├── docs/
│   └── (architecture docs)
├── COMPANY.md              # Company mission & state
├── TASKS.md               # Task board
├── README.md              # Project overview
└── GETTING_STARTED.md     # This file
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│              React Web UI                    │
│         (localhost:5173)                    │
└─────────────────┬───────────────────────────┘
                  │ WebSocket / HTTP
                  ▼
┌─────────────────────────────────────────────┐
│              FastAPI Bridge                 │
│         (localhost:8000)                    │
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │        LangGraph Agent Loop          │   │
│  │                                      │   │
│  │  ┌──────────┐    ┌──────────────┐   │   │
│  │  │ Recall   │    │  Archival    │   │   │
│  │  │  (SQL)   │    │   (Vector)   │   │   │
│  │  └──────────┘    └──────────────┘   │   │
│  └─────────────────────────────────────┘   │
│                      │                      │
│                      ▼                      │
│  ┌─────────────────────────────────────┐   │
│  │        Ollama (Local LLM)           │   │
│  │       (localhost:11434)             │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## Key Components

### Tiered Memory System
- **Recall (SQL)**: Stores hard facts and preferences
  - User-stated information (coffee preferences, manager's name)
  - Exact data that shouldn't change

- **Archival (LanceDB)**: Stores conceptual history
  - Conversation summaries
  - Learned patterns
  - Contextual associations

### Plugin System
Skills are loaded dynamically at runtime:

```python
from microrush.plugins import PluginRegistry

registry = PluginRegistry()
registry.discover("src/microrush/skills")
skill = registry.get("calendar")
result = skill.execute({"action": "departure_time", "meeting_id": 1})
```

### Available Skills
- **Calendar**: Meeting prep with traffic awareness
- **Files**: Smart search and summarization

---

## API Reference

### Chat Endpoint

```bash
# HTTP POST
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello!", "session_id": "default"}'

# WebSocket
wscat -c ws://localhost:8000/api/chat/ws
```

### Health Check

```bash
curl http://localhost:8000/health
```

---

## Development

### Run Tests

```bash
cd backend
pytest tests/ -v
```

### Code Style

```bash
cd backend
black src/
ruff check src/
```

---

## Troubleshooting

### "Connection refused" to Ollama
```bash
# Verify Ollama is running
ollama list

# Pull the model if needed
ollama pull llama3.2
```

### Frontend can't connect to API
```bash
# Check CORS settings in .env
CORS_ORIGINS=http://localhost:5173

# Ensure backend is running on port 8000
curl http://localhost:8000/
```

### Database errors
```bash
# Delete local databases to reset
rm -f ./data/memory_recall.db
rm -rf ./data/memory_archival
```

---

## Next Steps

1. ⬜ Set up your first plugin
2. ⬜ Integrate with your calendar (Google Calendar, Apple Calendar)
3. ⬜ Add voice input
4. ⬜ Connect to smart home devices
5. ⬜ Train a custom local model

---

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [LanceDB Documentation](https://lancedb.github.io/lancedb/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Questions?** Check the docs folder or open an issue.