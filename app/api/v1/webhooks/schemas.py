from pydantic import BaseModel
from typing import Any, Dict


class StripeEvent(BaseModel):
    id: str
    type: str
    data: Dict[str, Any]
