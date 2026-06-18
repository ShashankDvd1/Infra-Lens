"""
LandScope AI — Areas API endpoints.
"""

from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from geoalchemy2.functions import ST_DWithin, ST_MakePoint, ST_SetSRID

from app.db.session import get_db
from app.models import Area, GrowthIndicator, Project
from app.schemas.area import AreaListResponse, AreaDetailResponse, GrowthIndicatorResponse

router = APIRouter()


@router.get("")
async def list_areas(
    city: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List areas with growth data."""
    conditions = []
    if city:
        conditions.append(Area.city.ilike(f"%{city}%"))

    query = (
        select(
            Area,
            func.ST_Y(func.ST_Transform(Area.centroid, 4326)).label("latitude"),
            func.ST_X(func.ST_Transform(Area.centroid, 4326)).label("longitude"),
        )
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Area.name)
    )
    if conditions:
        query = query.where(and_(*conditions))

    result = await db.execute(query)
    rows = result.all()

    items = []
    for row in rows:
        area = row[0]
        items.append(AreaListResponse(
            id=area.id,
            name=area.name,
            slug=area.slug,
            city=area.city,
            avg_price_sqft=area.avg_price_sqft,
            growth_rate_pct=area.growth_rate_pct,
            latitude=row[1],
            longitude=row[2],
        ))

    return {"items": items, "total": len(items)}


@router.get("/{slug}", response_model=AreaDetailResponse)
async def get_area(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get area intelligence with nearby projects and growth indicators."""
    query = (
        select(
            Area,
            func.ST_Y(func.ST_Transform(Area.centroid, 4326)).label("latitude"),
            func.ST_X(func.ST_Transform(Area.centroid, 4326)).label("longitude"),
        )
        .where(Area.slug == slug)
        .options(selectinload(Area.growth_indicators))
    )

    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Area not found")

    area = row[0]
    lat = row[1]
    lng = row[2]

    # Find nearby projects (within 5km of area centroid)
    nearby_projects = []
    if area.centroid:
        nearby_query = (
            select(
                Project,
                func.ST_Y(func.ST_Transform(Project.location, 4326)).label("latitude"),
                func.ST_X(func.ST_Transform(Project.location, 4326)).label("longitude"),
            )
            .where(
                func.ST_DWithin(
                    func.cast(Project.location, func.Geography),
                    func.cast(area.centroid, func.Geography),
                    5000,  # 5km in meters
                )
            )
            .limit(20)
        )
        nearby_result = await db.execute(nearby_query)
        for proj_row in nearby_result.all():
            proj = proj_row[0]
            nearby_projects.append({
                "id": str(proj.id),
                "name": proj.name,
                "slug": proj.slug,
                "project_type": proj.project_type.value,
                "status": proj.status.value,
                "latitude": proj_row[1],
                "longitude": proj_row[2],
            })

    indicators = [GrowthIndicatorResponse.model_validate(gi) for gi in area.growth_indicators]

    return AreaDetailResponse(
        id=area.id,
        name=area.name,
        slug=area.slug,
        city=area.city,
        avg_price_sqft=area.avg_price_sqft,
        growth_rate_pct=area.growth_rate_pct,
        latitude=lat,
        longitude=lng,
        description=area.description,
        connectivity_data=area.connectivity_data,
        growth_indicators=indicators,
        nearby_projects=nearby_projects,
        created_at=area.created_at,
        updated_at=area.updated_at,
    )
