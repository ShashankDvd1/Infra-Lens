"""
LandScope AI — Projects API endpoints.
"""

import math
from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from geoalchemy2.functions import ST_DWithin, ST_MakePoint, ST_SetSRID, ST_X, ST_Y

from app.db.session import get_db
from app.models import Project, Source, AISummary, ProjectType, ProjectStatus
from app.schemas.project import (
    ProjectListResponse,
    ProjectDetailResponse,
    PaginatedResponse,
    AISummaryResponse,
    SourceResponse,
)

router = APIRouter()


def _project_to_list_response(project: Project) -> ProjectListResponse:
    """Convert a Project model to list response, extracting lat/lng from geometry."""
    lat = None
    lng = None
    # Location will be extracted in the query via ST_X/ST_Y
    return ProjectListResponse(
        id=project.id,
        name=project.name,
        slug=project.slug,
        project_type=project.project_type,
        status=project.status,
        city=project.city,
        authority=project.authority,
        announced_date=project.announced_date,
        expected_completion=project.expected_completion,
        budget_crore=project.budget_crore,
        verification_status=project.verification_status,
        is_verified=project.is_verified,
        latitude=getattr(project, "_latitude", None),
        longitude=getattr(project, "_longitude", None),
        created_at=project.created_at,
    )


@router.get("", response_model=PaginatedResponse)
async def list_projects(
    city: Optional[str] = Query(None),
    project_type: Optional[ProjectType] = Query(None),
    status: Optional[ProjectStatus] = Query(None),
    is_verified: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List projects with optional filters and pagination."""
    # Build filter conditions
    conditions = []
    if city:
        conditions.append(Project.city.ilike(f"%{city}%"))
    if project_type:
        conditions.append(Project.project_type == project_type)
    if status:
        conditions.append(Project.status == status)
    if is_verified is not None:
        conditions.append(Project.is_verified == is_verified)

    # Count total
    count_query = select(func.count(Project.id))
    if conditions:
        count_query = count_query.where(and_(*conditions))
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Fetch projects with lat/lng extracted from geometry
    query = (
        select(
            Project,
            func.ST_Y(func.ST_Transform(Project.location, 4326)).label("latitude"),
            func.ST_X(func.ST_Transform(Project.location, 4326)).label("longitude"),
        )
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Project.created_at.desc())
    )
    if conditions:
        query = query.where(and_(*conditions))

    result = await db.execute(query)
    rows = result.all()

    items = []
    for row in rows:
        project = row[0]
        project._latitude = row[1]
        project._longitude = row[2]
        items.append(_project_to_list_response(project))

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get project details with sources and AI summary."""
    query = (
        select(
            Project,
            func.ST_Y(func.ST_Transform(Project.location, 4326)).label("latitude"),
            func.ST_X(func.ST_Transform(Project.location, 4326)).label("longitude"),
        )
        .where(Project.id == project_id)
        .options(
            selectinload(Project.sources),
            selectinload(Project.ai_summaries),
        )
    )

    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Project not found")

    project = row[0]
    lat = row[1]
    lng = row[2]

    # Get the latest AI summary
    ai_summary = None
    if project.ai_summaries:
        latest = sorted(project.ai_summaries, key=lambda s: s.generated_at, reverse=True)[0]
        ai_summary = AISummaryResponse.model_validate(latest)

    sources = [SourceResponse.model_validate(s) for s in project.sources]

    return ProjectDetailResponse(
        id=project.id,
        name=project.name,
        slug=project.slug,
        project_type=project.project_type,
        status=project.status,
        description=project.description,
        city=project.city,
        district=project.district,
        authority=project.authority,
        announced_date=project.announced_date,
        expected_completion=project.expected_completion,
        budget_crore=project.budget_crore,
        impact_radius_km=project.impact_radius_km,
        confidence_score=project.confidence_score,
        verification_status=project.verification_status,
        is_verified=project.is_verified,
        latitude=lat,
        longitude=lng,
        sources=sources,
        ai_summary=ai_summary,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


@router.get("/nearby/search")
async def get_nearby_projects(
    latitude: float = Query(..., ge=6.5, le=37.5, description="Latitude (India bounds)"),
    longitude: float = Query(..., ge=68.0, le=97.5, description="Longitude (India bounds)"),
    radius_km: float = Query(5.0, gt=0, le=100, description="Search radius in km"),
    project_type: Optional[ProjectType] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Find projects within a radius of given coordinates using PostGIS."""
    # Convert km to meters for ST_DWithin (uses geography type for accurate distance)
    radius_meters = radius_km * 1000

    point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

    conditions = [
        func.ST_DWithin(
            func.cast(Project.location, func.Geography),
            func.cast(point, func.Geography),
            radius_meters,
        )
    ]
    if project_type:
        conditions.append(Project.project_type == project_type)

    query = (
        select(
            Project,
            func.ST_Y(func.ST_Transform(Project.location, 4326)).label("latitude"),
            func.ST_X(func.ST_Transform(Project.location, 4326)).label("longitude"),
            func.ST_Distance(
                func.cast(Project.location, func.Geography),
                func.cast(point, func.Geography),
            ).label("distance_meters"),
        )
        .where(and_(*conditions))
        .order_by("distance_meters")
        .limit(50)
    )

    result = await db.execute(query)
    rows = result.all()

    items = []
    for row in rows:
        project = row[0]
        project._latitude = row[1]
        project._longitude = row[2]
        item = _project_to_list_response(project).model_dump()
        item["distance_km"] = round(row[3] / 1000, 2) if row[3] else None
        items.append(item)

    return {"items": items, "total": len(items), "center": {"latitude": latitude, "longitude": longitude, "radius_km": radius_km}}
