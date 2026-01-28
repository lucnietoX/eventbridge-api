"""Stripe Webhooks API Router."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import logging

from fastapi import BackgroundTasks
from fastapi import APIRouter, Depends, status
from app.services.notion.executor_notion import execute_event
from app.db.deps import get_db
from app.db import models
from app.api.v1.webhooks.schemas import StripeEvent


router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/stripe", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    event: StripeEvent,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Endpoint to receive Stripe webhooks."""
    db_event = models.Event(
        source="stripe",
        event_id=event.id,
        type=event.type,
        payload=event.data,
    )
    db.add(db_event)
    logger = logging.getLogger("app.api.v1.webhooks.stripe")
    logger.info("Received Stripe event: %s of type %s", event.id, event.type)

    try:
        await db.commit()
        logger.info("Committed Stripe event: %s of type %s", event.id, event.type)
    except IntegrityError:
        await db.rollback()
        logger.info(
            "Rolled back Stripe event: %s of type %s due to IntegrityError",
            event.id,
            event.type,
        )
        return {
            "status": "event is duplicate and has already been processed",
            "accepted": False,
        }
    except Exception as e:
        await db.rollback()
        return {"status": "error", "detail": str(e), "accepted": False}

    execution = models.Execution(
        event_id=db_event.id,
        status="pending",
    )

    db.add(execution)
    await db.commit()

    background_tasks.add_task(
        execute_event,
        db_event.id,
        execution.id,
        db,
    )

    return {"status": "webhook received", "accepted": True}
