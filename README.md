# Micro Rush — Autonomous Agent Company

## Overview
This is a self-running company powered by 5 AI agents. They plan, assign work, execute, and drive progress autonomously.

## The 5 Agents
| Agent | Role |
|-------|------|
| LEAD | CEO/Orchestrator — analyzes state, sets goals, assigns tasks |
| DESIGNER | Brand, UI/UX, landing page, design system |
| ENGINEER | Infrastructure, LangGraph, Ollama, CI/CD |
| SOFTWARE-ENGINEER | Features, code, APIs, FastAPI bridge |
| RESEARCHER | Market research, competitor analysis, validation |

## Directory Structure
```
micro-rush/
├── COMPANY.md          # Mission, goals, current state
├── TASKS.md            # Task board with all assignments
├── README.md           # This file
├── agents/
│   ├── LEAD.md         # CEO persona + orchestration loop
│   ├── DESIGNER.md     # Design persona
│   ├── ENGINEER.md     # Infrastructure persona
│   ├── SOFTWARE-ENGINEER.md  # Dev persona
│   └── RESEARCHER.md   # Research persona
├── state/
│   └── loop-log.md     # Execution history
└── projects/
    ├── designer/       # Design work
    ├── engineer/        # Infrastructure work
    ├── researcher/      # Research reports
    └── swe/             # Software engineering
```

## How the Loop Works
1. **LEAD reads state** — COMPANY.md, TASKS.md, loop-log.md
2. **LEAD analyzes** — What's done? What's blocked? What's next?
3. **LEAD assigns tasks** — Routes work to appropriate agent
4. **Agents execute** — Work on their tasks
5. **LEAD reviews** — Approves or sends back for revision
6. **Loop repeats** — Forever

## Initial Task Assignments
| Agent | Task | Status |
|-------|------|--------|
| ENGINEER | ENG-001: Phase 1 project initialization + LangGraph | Backlog |
| ENGINEER | ENG-002: Ollama local LLM integration | Backlog |
| RESEARCHER | RES-001: Market research - local AI assistants | Backlog |
| RESEARCHER | RES-002: Framework analysis - LanceDB vs alternatives | Backlog |
| DESIGNER | BRAND-001: Brand identity | Backlog |
| DESIGNER | WEB-001: Landing page | Backlog |

## Running the Company
The company runs continuously. Each agent cycle:
```
# Check status
cat micro-rush/COMPANY.md
cat micro-rush/TASKS.md

# Agent works on their task
# Updates TASKS.md when complete
# Writes status to projects/<agent>/status.md

# LEAD reviews and logs
# Append to state/loop-log.md
```

## Current Phase
Phase 3: Core Skills Implementation

## Company Status
Status: ACTIVE
Last Loop: Initialized