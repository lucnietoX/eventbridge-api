"""API routes for event management."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.db.deps import get_db
from app.db import models

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("")
async def list_events(
    source: str | None = Query(None),
    limit: int = Query(50, le=200),
    skip: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List events with optional filtering by source."""
    stmt = select(models.Event).order_by(desc(models.Event.received_at))

    if source:
        stmt = stmt.where(models.Event.source == source)

    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)
    events = result.scalars().all()

    return events
