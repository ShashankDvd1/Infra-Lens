from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.distress import DistressProperty
from app.models import Project
from app.schemas.distress import DistressPropertyResponse
from app.services.search_service import perform_search_and_verify_flow
from typing import List, Optional

router = APIRouter()

@router.get("", response_model=List[DistressPropertyResponse])
async def list_distress_properties(
    city: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List distress properties/auctions with optional city filter."""
    query = select(DistressProperty)
    if city:
        query = query.where(DistressProperty.city.ilike(f"%{city}%"))
    result = await db.execute(query)
    properties = result.scalars().all()
    return properties

@router.post("/scan", response_model=List[DistressPropertyResponse])
async def scan_and_verify_properties(
    city: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Perform live search, verify listings using LLM, match with projects, and save to DB."""
    # 1. Run live search and verification flow
    verified_listings = await perform_search_and_verify_flow("bank auction distress properties", city)
    
    # 2. Fetch projects in the city for matching
    proj_stmt = select(Project).where(Project.city.ilike(f"%{city}%"))
    projects_res = await db.execute(proj_stmt)
    db_projects = projects_res.scalars().all()
    
    # Stop words for location-based matching
    stop_words = {"metro", "phase", "line", "road", "outer", "ring", "expressway", "link", "extension", "project", "the", "and", "for", "city"}
    
    for item in verified_listings:
        # Check if already exists in DB
        existing_stmt = select(DistressProperty).where(DistressProperty.title == item["title"])
        existing_res = await db.execute(existing_stmt)
        if existing_res.first():
            continue
            
        # Match project
        matched_project_id = None
        for proj in db_projects:
            clean_loc = item.get("location", "").lower()
            clean_title = item.get("title", "").lower()
            proj_name_words = set(proj.name.lower().split())
            keywords = {w for w in proj_name_words if len(w) > 3 and w not in stop_words}
            if any(kw in clean_loc or kw in clean_title for kw in keywords):
                matched_project_id = proj.id
                break
                
        # Insert new distress property
        new_prop = DistressProperty(
            title=item["title"],
            location=item["location"],
            city=item["city"],
            property_type=item["property_type"],
            market_value=item["market_value"],
            reserve_price=item["reserve_price"],
            discount=item["discount"],
            auction_date=item["auction_date"],
            backing_authority=item.get("backing_authority", "Public Bank"),
            project_id=matched_project_id
        )
        db.add(new_prop)
        
    await db.commit()
    
    # Return updated list
    query = select(DistressProperty).where(DistressProperty.city.ilike(f"%{city}%"))
    result = await db.execute(query)
    properties = result.scalars().all()
    return properties


