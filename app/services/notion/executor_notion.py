"""Executor for Notion-related events."""

import logging
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import models
from app.services.notion.notion_payments import create_notion_payment
from app.support.utils import stripe_map_execution_status


async def execute_event(
    event_id: int,
    execution_id: int,
    db: AsyncSession,
):
    """Execute the Notion event based on the Stripe event data."""
    start = time.time()

    try:
        # 1. fetch event
        stmt = select(models.Event).where(models.Event.id == event_id)
        result = await db.execute(stmt)
        event = result.scalar_one()

        logger = logging.getLogger("app.api.v1.webhooks.stripe")
        logger.info("Fetch Stripe event: %s of type %s", event.id, event.type)

        data = event.payload or {}

        attr_amount = (
            data.get("object", {}).get("amount", None)
            or data.get("object", {}).get("amount_paid", None)
            or data.get("object", {}).get("subtotal", None)
        ) / 100.0  # amount in cents or amount paid.
        attr_event_id = str(event.event_id)
        attr_event_type = str(event.type)
        attr_status = stripe_map_execution_status(attr_event_type)
        attr_customer_email = data.get("object", {}).get("customer_email", "None")
        attr_currency = data.get("object", {}).get("currency", "EUR")
        attr_customer_id = data.get("object", {}).get("customer", "")
        attr_invoice_number = (
            data.get("object", {})
            .get("lines", {})
            .get("data", [{}])[0]
            .get("invoice", "")
        )

        logger.info(
            "Creating Notion Payment: %s of type %s", attr_event_id, attr_event_type
        )
        resp = await create_notion_payment(
            event_id=attr_event_id,
            event_type=attr_event_type,
            status=attr_status,
            customer_email=attr_customer_email,
            amount=attr_amount,
            currency=attr_currency,
            customer=attr_customer_id,
            invoice_number=attr_invoice_number,
        )

        status = "success" if resp else "failed"
        response_code = 200 if resp else 400

    except Exception as e:
        logger.error("Executor error:", e)
        status = "failed"
        response_code = None

    duration_ms = int((time.time() - start) * 1000)

    # 2. update execution
    stmt = select(models.Execution).where(models.Execution.id == execution_id)
    result = await db.execute(stmt)
    execution = result.scalar_one()

    execution.status = status
    execution.response_code = response_code
    execution.duration_ms = duration_ms

    await db.commit()
