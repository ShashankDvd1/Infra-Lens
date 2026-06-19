"""
LandScope AI — Pydantic Schemas for AI/Chat endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class AskAIRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
    filters: Optional[dict] = None
    conversation_id: Optional[str] = None


class CitedSource(BaseModel):
    project_id: Optional[UUID] = None
    project_name: Optional[str] = None
    source_url: Optional[str] = None
    relevance_score: float = 0.0
    title: Optional[str] = None
    url: Optional[str] = None


class RecommendedArea(BaseModel):
    area: str
    avg_price_sqft: Optional[float] = None
    growth_potential: Optional[str] = None
    distance_to_project_km: Optional[float] = None


class AskAIResponse(BaseModel):
    answer: str
    sources: list[CitedSource] = []
    recommended_areas: list[RecommendedArea] = []
    disclaimer: str = "This information is AI-generated from public sources. Verify independently before making investment decisions."


class SummaryGenerateRequest(BaseModel):
    project_id: UUID


class InvestRecommendationRequest(BaseModel):
    budget: float = Field(..., description="Budget in Lakhs")
    risk: str = Field(..., description="Risk tolerance: low, moderate, high")


class InvestRecommendationResponse(BaseModel):
    strategy: str
    target_areas: list[str]
    expected_roi: str
    rationale: str
    backed_projects: list[dict] = []
