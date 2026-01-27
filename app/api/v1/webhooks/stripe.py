"""Stripe Webhooks API Router."""

from fastapi import APIRouter, Depends, status
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.deps import get_db
from app.db import models
from app.api.v1.webhooks.schemas import StripeEvent

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/stripe", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    event: StripeEvent,
    db: AsyncSession = Depends(get_db),
):
    """Endpoint to receive Stripe webhooks."""
    db_event = models.Event(
        source="stripe",
        event_id=event.id,
        type=event.type,
        payload=event.data,
    )

    db.add(db_event)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
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

    return {"status": "webhook received", "accepted": True}
