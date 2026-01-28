"""API routes for event management."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.db.deps import get_db
from app.db import models

router = APIRouter(prefix="/executions", tags=["Executions"])


@router.get("")
async def list_executions(
    status: str | None = Query(None),
    limit: int = Query(50, le=200),
    skip: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List executions with optional filtering by status."""
    stmt = select(models.Execution).order_by(desc(models.Execution.created_at))

    if status:
        stmt = stmt.where(models.Execution.status == status)

    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)
    executions = result.scalars().all()

    return executions
