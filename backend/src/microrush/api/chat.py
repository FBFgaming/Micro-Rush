"""Chat API — WebSocket bridge for React UI."""

from typing import Optional
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from ..agents import MicroRushAgent


router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    """Incoming chat message."""

    content: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    """Outgoing chat response."""

    content: str
    timestamp: datetime
    session_id: str
    done: bool = True


class agent:
    """Shared agent instance."""

    _instance: Optional[MicroRushAgent] = None

    @classmethod
    def get(cls) -> MicroRushAgent:
        if cls._instance is None:
            cls._instance = MicroRushAgent()
        return cls._instance


@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat.

    Protocol:
    - Client sends: {"content": "message", "session_id": "optional"}
    - Server sends: {"content": "response", "timestamp": "...", "done": true}
    """
    await websocket.accept()

    # Start with session context
    session_id = "default"
    agent_instance = agent.get()

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            user_message = data.get("content", "")
            session_id = data.get("session_id", session_id)

            if not user_message:
                continue

            # Run agent
            result = agent_instance.run(user_message, session_id=session_id)
            response = ChatResponse(
                content=result.get("response", "No response"),
                timestamp=datetime.utcnow(),
                session_id=session_id,
                done=True,
            )

            # Send response
            await websocket.send_json(response.model_dump(mode="json"))

    except WebSocketDisconnect:
        pass  # Normal disconnect
    except Exception as e:
        error_response = ChatResponse(
            content=f"Error: {str(e)}",
            timestamp=datetime.utcnow(),
            session_id=session_id,
            done=True,
        )
        try:
            await websocket.send_json(error_response.model_dump(mode="json"))
        except:
            pass


@router.post("/", response_model=ChatResponse)
async def send_message(message: ChatMessage) -> ChatResponse:
    """HTTP endpoint for single-shot chat."""

    agent_instance = agent.get()
    result = agent_instance.run(message.content, session_id=message.session_id)

    return ChatResponse(
        content=result.get("response", "No response"),
        timestamp=datetime.utcnow(),
        session_id=message.session_id,
        done=True,
    )