from sqlalchemy import String, DateTime, JSON, Integer, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(50))
    event_id: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSON)
    received_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("source", "event_id", name="uq_event_source_eventid"),
    )


class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    status: Mapped[str] = mapped_column(String(20))
    response_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    event = relationship("Event")
