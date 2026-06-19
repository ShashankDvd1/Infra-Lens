from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class DistressPropertyResponse(BaseModel):
    id: UUID
    title: str
    location: str
    city: str
    property_type: str
    market_value: float
    reserve_price: float
    discount: float
    auction_date: Optional[str] = None
    backing_authority: Optional[str] = None
    project_id: Optional[UUID] = None

    class Config:
        from_attributes = True
