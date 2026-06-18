"""
LandScope AI — Pydantic Schemas for Projects, Sources, and AI Summaries.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID

from app.models.project import ProjectType, ProjectStatus, SourceType, VerificationStatus


# --- Source Schemas ---


class SourceBase(BaseModel):
    source_type: SourceType
    title: str
    url: Optional[str] = None
    authority_name: Optional[str] = None
    published_date: Optional[date] = None
    is_active: bool = True


class SourceCreate(SourceBase):
    content_text: Optional[str] = None


class SourceResponse(SourceBase):
    id: UUID
    project_id: UUID
    last_checked: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- AI Summary Schemas ---


class AISummaryResponse(BaseModel):
    id: UUID
    project_id: UUID
    what_is_being_built: Optional[str] = None
    why_it_matters: Optional[str] = None
    expected_impact: Optional[str] = None
    nearby_benefiting_areas: Optional[str] = None
    model_used: Optional[str] = None
    generated_at: datetime

    class Config:
        from_attributes = True


# --- Project Schemas ---


class ProjectBase(BaseModel):
    name: str = Field(..., max_length=500)
    project_type: ProjectType
    status: ProjectStatus
    description: Optional[str] = None
    city: str = "Lucknow"
    district: Optional[str] = None
    authority: Optional[str] = None
    announced_date: Optional[date] = None
    expected_completion: Optional[date] = None
    budget_crore: Optional[float] = None
    impact_radius_km: Optional[float] = 5.0


class ProjectCreate(ProjectBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    sources: list[SourceCreate] = []


class ProjectListResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    project_type: ProjectType
    status: ProjectStatus
    city: str
    authority: Optional[str] = None
    announced_date: Optional[date] = None
    expected_completion: Optional[date] = None
    budget_crore: Optional[float] = None
    verification_status: VerificationStatus
    is_verified: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectListResponse):
    description: Optional[str] = None
    district: Optional[str] = None
    impact_radius_km: Optional[float] = None
    confidence_score: Optional[float] = None
    sources: list[SourceResponse] = []
    ai_summary: Optional[AISummaryResponse] = None
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectsListParams(BaseModel):
    """Query parameters for listing projects."""
    city: Optional[str] = None
    project_type: Optional[ProjectType] = None
    status: Optional[ProjectStatus] = None
    is_verified: Optional[bool] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class NearbyParams(BaseModel):
    """Query parameters for nearby projects."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(5.0, gt=0, le=100)
    project_type: Optional[ProjectType] = None


# --- Pagination ---


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
