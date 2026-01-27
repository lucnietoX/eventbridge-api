from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="EventBridge API",
    description="""
    Event-driven integration backend.

    Receives webhooks (e.g. Stripe), validates, persists events and executes asynchronous actions for external systems (e.g. Notion).
    """,
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")
