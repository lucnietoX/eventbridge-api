"""API V1 Router."""

from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.webhooks.stripe import router as stripe_webhook_router

# from app.api.v1.test import router as db_test_router
from app.api.v1.events import routes as events_router
from app.api.v1.execution import routes as execution_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(stripe_webhook_router)
# api_router.include_router(db_test_router)
api_router.include_router(events_router.router)
api_router.include_router(execution_router.router)
