"""Core agent — LangGraph-based agentic loop with tiered memory."""

from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from ..memory import RecallMemory, ArchivalMemory


class AgentState(BaseModel):
    """State carried through the agent graph."""

    messages: list[dict] = Field(default_factory=list)
    memory_context: str = ""
    current_task: str | None = None
    task_result: str | None = None
    should_respond: bool = False
    session_id: str = "default"


SYSTEM_PROMPT = """You are Micro Rush, a privacy-first personal AI assistant.

Your traits:
- You are helpful, concise, and practical
- You respect the user's privacy — all processing happens locally
- You are proactive when it comes to calendar and scheduling
- You remember user preferences over time
- You communicate naturally, not like a corporate chatbot

When you don't know something, say so honestly."""


class MicroRushAgent:
    """
    The core Micro Rush agent powered by LangGraph.

    Flow:
    1. Receives user message
    2. Loads memory context (Recall + Archival)
    3. Runs ReAct loop with local LLM (Ollama)
    4. Updates memory
    5. Returns response
    """

    def __init__(
        self,
        model_name: str = "llama3.2",
        base_url: str = "http://localhost:11434",
        recall_db: str = "memory_recall.db",
        archival_dir: str = "memory_archival",
    ):
        self.llm = ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=0.7,
        )
        self.recall = RecallMemory(db_path=recall_db)
        self.archival = ArchivalMemory(db_path=archival_dir)
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state machine."""
        builder = StateGraph(AgentState)

        # Nodes
        builder.add_node("load_memory", self._load_memory)
        builder.add_node("think", self._think)
        builder.add_node("act", self._act)
        builder.add_node("remember", self._remember)

        # Edges
        builder.add_edge("load_memory", "think")
        builder.add_edge("think", "act")
        builder.add_edge("act", "remember")
        builder.add_edge("remember", END)

        builder.set_entry_point("load_memory")
        return builder.compile()

    def _load_memory(self, state: AgentState) -> dict:
        """Load relevant context from tiered memory."""
        context_parts = []

        # Load recent messages for context
        recent_messages = state.messages[-5:] if state.messages else []
        if recent_messages:
            msg_summary = "\n".join([
                f"{m.get('role', 'user')}: {m.get('content', '')}"
                for m in recent_messages
            ])
            context_parts.append(f"Recent conversation:\n{msg_summary}")

        # Load user preferences from Recall
        try:
            prefs = self.recall.search("preference", category="preference", limit=5)
            if prefs:
                prefs_text = "\n".join([f"- {p.key}: {p.value}" for p in prefs])
                context_parts.append(f"User preferences:\n{prefs_text}")
        except Exception:
            pass

        # Load conversational history from Archival
        try:
            # TODO: Use proper embedding search
            context_parts.append("[Archival memory placeholder]")
        except Exception:
            pass

        memory_context = "\n\n".join(context_parts) if context_parts else "No prior context available."
        return {"memory_context": memory_context}

    def _think(self, state: AgentState) -> dict:
        """Run reasoning step with actual LLM."""
        # Build messages for LLM
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
        ]

        # Add memory context as system info
        if state.memory_context:
            messages.append(SystemMessage(content=f"Context from memory:\n{state.memory_context}"))

        # Add conversation history
        for msg in state.messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(SystemMessage(content=content))

        # Invoke LLM
        try:
            response = self.llm.invoke(messages)
            return {"task_result": response.content, "should_respond": True}
        except Exception as e:
            return {"task_result": f"I'm having trouble connecting to my brain right now. Error: {str(e)}", "should_respond": True}

    def _act(self, state: AgentState) -> dict:
        """Execute action based on reasoning."""
        # For now, the LLM response IS the action
        # In future, this will route to skills/plugins
        return {"task_result": state.task_result or "Processing..."}

    def _remember(self, state: AgentState) -> dict:
        """Store important info in memory."""
        updates = {}

        # Extract and store any preferences mentioned
        if state.task_result and len(state.messages) == 1:
            # First exchange - check if user shared preferences
            last_message = state.messages[0].get("content", "")
            # Simple heuristic: store things user says about themselves
            # TODO: Better preference extraction with LLM

        return updates

    def run(self, user_message: str, session_id: str = "default") -> dict:
        """
        Run the agent loop with a user message.

        Returns dict with 'response' key containing the LLM response.
        """
        # Append user message to history
        messages = [
            {"role": "user", "content": user_message}
        ]

        initial_state = AgentState(
            messages=messages,
            session_id=session_id,
        )

        result = self.graph.invoke(initial_state)
        return {"response": result.get("task_result", "No response generated")}


# Convenience function for quick testing
def create_agent() -> MicroRushAgent:
    """Create a default configured agent."""
    return MicroRushAgent()


if __name__ == "__main__":
    print("🧠 Micro Rush Agent initialized")
    print("   Connect to Ollama at http://localhost:11434")
    print("   Model: llama3.2")