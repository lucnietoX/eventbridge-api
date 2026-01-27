from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@192.168.1.225:5431/eventbridge"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
