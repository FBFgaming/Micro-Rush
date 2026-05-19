"""Health check endpoint."""

from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

from .. import __version__


router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    timestamp: datetime
    components: dict


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check service health."""

    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.utcnow(),
        components={
            "api": "up",
            "agent": "up",  # TODO: Add actual check
            "memory_recall": "up",  # TODO: Add actual check
            "memory_archival": "up",  # TODO: Add actual check
        },
    )