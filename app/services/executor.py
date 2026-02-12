"""Service for executing events."""

import time
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import models


async def execute_event(event_id: int, execution_id: int, db: AsyncSession):
    """Execute the event by simulating an external API call."""
    start = time.time()

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post(
                "https://httpbin.org/post",
                json={"event_id": event_id},
            )

        status = "success"
        response_code = resp.status_code

    except Exception:
        status = "failed"
        response_code = None

    duration_ms = int((time.time() - start) * 1000)

    stmt = select(models.Execution).where(models.Execution.id == execution_id)
    result = await db.execute(stmt)
    execution = result.scalar_one()

    execution.status = status
    execution.response_code = response_code
    execution.duration_ms = duration_ms

    await db.commit()
