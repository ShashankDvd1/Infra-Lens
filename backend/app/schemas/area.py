"""
LandScope AI — Pydantic Schemas for Areas and Growth Indicators.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class GrowthIndicatorResponse(BaseModel):
    id: UUID
    indicator_type: str
    value: float
    unit: Optional[str] = None
    measured_date: Optional[date] = None

    class Config:
        from_attributes = True


class AreaListResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    city: str
    avg_price_sqft: Optional[float] = None
    growth_rate_pct: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    project_count: int = 0

    class Config:
        from_attributes = True


class AreaDetailResponse(AreaListResponse):
    description: Optional[str] = None
    connectivity_data: Optional[dict] = None
    growth_indicators: list[GrowthIndicatorResponse] = []
    nearby_projects: list = []  # Will be ProjectListResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
