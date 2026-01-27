from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.deps import get_db

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/db")
async def test_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db": result.scalar()}
