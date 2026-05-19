"""FastAPI application entry point."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .. import __version__
from .chat import router as chat_router
from .health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print(f"🚀 Micro Rush v{__version__} starting...")
    print("📡 API ready at /api/chat")
    print("🧠 Agent ready (connect to Ollama at localhost:11434)")
    yield
    # Shutdown
    print("👋 Micro Rush shutting down...")


app = FastAPI(
    title="Micro Rush API",
    description="Privacy-first personal AI assistant",
    version=__version__,
    lifespan=lifespan,
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for React build in production)
build_path = os.path.join(os.path.dirname(__file__), "../../../frontend/dist")
if os.path.exists(build_path):
    app.mount("/", StaticFiles(directory=build_path, html=True), name="static")

# Routes
app.include_router(health_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Micro Rush",
        "version": __version__,
        "tagline": "Your privacy-first personal AI assistant",
    }