"""Schemas for webhook payloads."""

from typing import Any, Dict
from pydantic import BaseModel


class StripeEvent(BaseModel):
    """Schema for Stripe webhook event payload."""

    id: str
    type: str
    data: Dict[str, Any]
