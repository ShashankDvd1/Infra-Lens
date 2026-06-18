from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.distress import DistressProperty
from app.schemas.distress import DistressPropertyResponse
from typing import List

router = APIRouter()

@router.get("", response_model=List[DistressPropertyResponse])
async def list_distress_properties(
    db: AsyncSession = Depends(get_db)
):
    """List all distress properties/auctions."""
    result = await db.execute(select(DistressProperty))
    properties = result.scalars().all()
    return properties
