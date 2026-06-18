"""
LandScope AI — Search API endpoint.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, text

from app.db.session import get_db
from app.models import Project, Area, ProjectType, ProjectStatus

router = APIRouter()


@router.get("")
async def search(
    q: str = Query(..., min_length=1, max_length=500, description="Search query"),
    mode: str = Query("fulltext", description="Search mode: fulltext or semantic"),
    project_type: Optional[ProjectType] = Query(None),
    status: Optional[ProjectStatus] = Query(None),
    city: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Full-text and semantic search across projects and areas."""
    
    if mode == "semantic":
        from app.rag.retriever import search_projects
        matches = await search_projects(db, q, limit=limit)
        
        projects = []
        for match in matches:
            row = match["project"]
            # Apply filters manually for semantic search since retriever doesn't filter yet
            if project_type and row.project_type != project_type: continue
            if status and row.status != status: continue
            if city and city.lower() not in row.city.lower(): continue
            
            projects.append({
                "type": "project",
                "id": str(row.id),
                "name": row.name,
                "slug": row.slug,
                "project_type": row.project_type.value,
                "status": row.status.value,
                "city": row.city,
                "authority": row.authority,
                "latitude": row.location.y if row.location else None,
                "longitude": row.location.x if row.location else None,
                "similarity_score": match["score"]
            })
            
        return {
            "query": q,
            "mode": mode,
            "results": projects,
            "total_projects": len(projects),
            "total_areas": 0,
            "total": len(projects),
        }
    
    # Fallback to full-text search
    search_pattern = f"%{q}%"

    # Search projects
    project_query = (
        select(
            Project.id,
            Project.name,
            Project.slug,
            Project.project_type,
            Project.status,
            Project.city,
            Project.authority,
            Project.description,
            func.ST_Y(func.ST_Transform(Project.location, 4326)).label("latitude"),
            func.ST_X(func.ST_Transform(Project.location, 4326)).label("longitude"),
        )
        .where(
            or_(
                Project.name.ilike(search_pattern),
                Project.description.ilike(search_pattern),
                Project.authority.ilike(search_pattern),
                Project.district.ilike(search_pattern),
            )
        )
    )

    if project_type:
        project_query = project_query.where(Project.project_type == project_type)
    if status:
        project_query = project_query.where(Project.status == status)
    if city:
        project_query = project_query.where(Project.city.ilike(f"%{city}%"))

    project_query = project_query.limit(limit)
    project_result = await db.execute(project_query)
    project_rows = project_result.all()

    # Search areas
    area_query = (
        select(
            Area.id,
            Area.name,
            Area.slug,
            Area.city,
            Area.avg_price_sqft,
            Area.growth_rate_pct,
        )
        .where(
            or_(
                Area.name.ilike(search_pattern),
                Area.description.ilike(search_pattern),
            )
        )
        .limit(limit)
    )
    area_result = await db.execute(area_query)
    area_rows = area_result.all()

    # Format results
    projects = [
        {
            "type": "project",
            "id": str(row.id),
            "name": row.name,
            "slug": row.slug,
            "project_type": row.project_type.value,
            "status": row.status.value,
            "city": row.city,
            "authority": row.authority,
            "latitude": row.latitude,
            "longitude": row.longitude,
        }
        for row in project_rows
    ]

    areas = [
        {
            "type": "area",
            "id": str(row.id),
            "name": row.name,
            "slug": row.slug,
            "city": row.city,
            "avg_price_sqft": row.avg_price_sqft,
            "growth_rate_pct": row.growth_rate_pct,
        }
        for row in area_rows
    ]

    return {
        "query": q,
        "mode": mode,
        "results": projects + areas,
        "total_projects": len(projects),
        "total_areas": len(areas),
        "total": len(projects) + len(areas),
    }
