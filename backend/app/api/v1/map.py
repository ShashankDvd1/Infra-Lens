"""
LandScope AI — Map API endpoints (GeoJSON markers and clusters).
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models import Project, ProjectType, ProjectStatus
from app.core.cache import cache_response

router = APIRouter()


# Color mapping for project types
PROJECT_TYPE_COLORS = {
    ProjectType.METRO: "#3B82F6",           # Blue
    ProjectType.EXPRESSWAY: "#10B981",       # Green
    ProjectType.RING_ROAD: "#8B5CF6",        # Purple
    ProjectType.IT_CITY: "#F59E0B",          # Amber
    ProjectType.IT_PARK: "#F59E0B",          # Amber
    ProjectType.WELLNESS_CITY: "#EC4899",    # Pink
    ProjectType.TOWNSHIP: "#F97316",         # Orange
    ProjectType.LOGISTICS_PARK: "#6366F1",   # Indigo
    ProjectType.GOVT_HOUSING: "#14B8A6",     # Teal
    ProjectType.LDA: "#14B8A6",              # Teal
    ProjectType.AWAS_VIKAS: "#14B8A6",       # Teal
    ProjectType.FLYOVER: "#64748B",          # Slate
    ProjectType.BRIDGE: "#64748B",           # Slate
    ProjectType.OTHER: "#6B7280",            # Gray
}

PROJECT_TYPE_ICONS = {
    ProjectType.METRO: "🚇",
    ProjectType.EXPRESSWAY: "🛣️",
    ProjectType.RING_ROAD: "🔄",
    ProjectType.IT_CITY: "🏙️",
    ProjectType.IT_PARK: "💻",
    ProjectType.WELLNESS_CITY: "🏥",
    ProjectType.TOWNSHIP: "🏘️",
    ProjectType.LOGISTICS_PARK: "🏭",
    ProjectType.GOVT_HOUSING: "🏠",
    ProjectType.LDA: "🏗️",
    ProjectType.AWAS_VIKAS: "🏠",
    ProjectType.FLYOVER: "🌉",
    ProjectType.BRIDGE: "🌉",
    ProjectType.OTHER: "📍",
}


@router.get("/markers")
@cache_response(expire_seconds=300)
async def get_map_markers(
    request: Request,
    city: Optional[str] = Query(None),
    project_type: Optional[ProjectType] = Query(None),
    status: Optional[ProjectStatus] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Return GeoJSON FeatureCollection for map rendering."""
    query = select(
        Project.id,
        Project.name,
        Project.slug,
        Project.project_type,
        Project.status,
        Project.authority,
        Project.budget_crore,
        Project.is_verified,
        Project.verification_status,
        Project.expected_completion,
        func.ST_Y(func.ST_Transform(Project.location, 4326)).label("latitude"),
        func.ST_X(func.ST_Transform(Project.location, 4326)).label("longitude"),
    ).where(Project.location.isnot(None))

    if city:
        query = query.where(Project.city.ilike(f"%{city}%"))
    if project_type:
        query = query.where(Project.project_type == project_type)
    if status:
        query = query.where(Project.status == status)

    result = await db.execute(query)
    rows = result.all()

    features = []
    for row in rows:
        if row.latitude is None or row.longitude is None:
            continue

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row.longitude, row.latitude],
            },
            "properties": {
                "id": str(row.id),
                "name": row.name,
                "slug": row.slug,
                "project_type": row.project_type.value,
                "status": row.status.value,
                "authority": row.authority,
                "budget_crore": row.budget_crore,
                "is_verified": row.is_verified,
                "verification_status": row.verification_status.value,
                "expected_completion": str(row.expected_completion) if row.expected_completion else None,
                "color": PROJECT_TYPE_COLORS.get(row.project_type, "#6B7280"),
                "icon": PROJECT_TYPE_ICONS.get(row.project_type, "📍"),
            },
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "total": len(features),
            "center": [80.9462, 26.8467],  # Lucknow center
            "zoom": 11,
        },
    }


@router.get("/clusters")
async def get_map_clusters(
    zoom: int = Query(11, ge=1, le=20),
    city: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Return clustered markers based on zoom level.

    At lower zoom levels, nearby markers are grouped into clusters.
    At higher zoom levels, individual markers are returned.
    """
    # For MVP, we return all markers and let the frontend handle clustering
    # (Leaflet.markercluster). Server-side clustering can be added in Phase 2.
    return await get_map_markers(city=city, db=db)
