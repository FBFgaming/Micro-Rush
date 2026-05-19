"""Core agent — LangGraph-based agentic loop with tiered memory."""

from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama


class AgentState(BaseModel):
    """State carried through the agent graph."""

    messages: list[dict] = Field(default_factory=list)
    memory_context: str = ""
    current_task: str | None = None
    task_result: str | None = None
    should_respond: bool = False
    session_id: str = "default"


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

    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.llm = ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=0.7,
        )
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
        # TODO: Integrate actual memory system
        # - SQL lookup for hard facts (Recall)
        # - Vector search for conceptual history (Archival)
        return {"memory_context": "[Memory loading placeholder]"}

    def _think(self, state: AgentState) -> dict:
        """Run reasoning step."""
        # Placeholder for ReAct reasoning
        return {"should_respond": False}

    def _act(self, state: AgentState) -> dict:
        """Execute action based on reasoning."""
        return {"task_result": None}

    def _remember(self, state: AgentState) -> dict:
        """Store important info in memory."""
        return {}  # TODO: Persist to SQL + LanceDB

    def run(self, user_message: str, session_id: str = "default") -> dict:
        """
        Run the agent loop with a user message.

        Returns dict with 'response' key containing the LLM response.
        """
        initial_state = AgentState(
            messages=[{"role": "user", "content": user_message}],
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