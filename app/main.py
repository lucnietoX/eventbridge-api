"""Main application entry point."""

from fastapi import FastAPI
from app.api.v1.router import api_router
from app.log.logger_setup import setup_logging

setup_logging()

app = FastAPI(
    title="EventBridge API",
    description="""
    Event-driven integration backend.

    Receives webhooks (e.g. Stripe), validates, persists events and executes asynchronous actions for external systems (e.g. Notion).

    Author: Luciano Nieto
    """,
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")
