"""
Main FastAPI application entry point.
"""

import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router

# ─────────────────────────────────────────────────────────────────────────────
# SENTRY — Error Monitoring (only activates when SENTRY_DSN env var is set)
# ─────────────────────────────────────────────────────────────────────────────
_sentry_dsn = os.environ.get("SENTRY_DSN", "")
if _sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    sentry_sdk.init(
        dsn=_sentry_dsn,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.2,
    )

# ─────────────────────────────────────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Adaptive RAG API",
    description="Agentic AI Chatbot with Adaptive Retrieval-Augmented Generation",
    version="1.0.0",
)

# ─────────────────────────────────────────────────────────────────────────────
# CORS — restrict to allowed origins in production via ALLOWED_ORIGINS env var
# Falls back to localhost for local development
# ─────────────────────────────────────────────────────────────────────────────
_allowed_origins = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:8501,http://localhost:7860,http://127.0.0.1:8501"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(router)
app.state.description_ = ""

# Track startup time for uptime reporting
_start_time = time.time()


# ─────────────────────────────────────────────────────────────────────────────
# ROOT
# ─────────────────────────────────────────────────────────────────────────────
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    """Root endpoint to verify API is running."""
    return {"message": "Adaptive RAG API is running"}


# ─────────────────────────────────────────────────────────────────────────────
# HEALTH CHECK ENDPOINTS
# Supports GET & HEAD methods for UptimeRobot, Render, Docker & CI probes
# ─────────────────────────────────────────────────────────────────────────────
@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    """Full health check — confirms API is running and responsive."""
    return {
        "status": "ok",
        "service": "adaptive-rag-api",
        "uptime_seconds": round(time.time() - _start_time, 2),
    }


@app.api_route("/ready", methods=["GET", "HEAD"])
async def ready():
    """Readiness probe — used by orchestrators to route traffic."""
    return {"status": "ready"}


@app.api_route("/live", methods=["GET", "HEAD"])
async def live():
    """Liveness probe — used by orchestrators to detect crashes."""
    return {"status": "alive"}
