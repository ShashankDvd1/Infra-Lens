from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.db.session import get_db
from app.models.user import User, SavedOpportunity
from app.models.project import Project
from app.schemas.user import UserResponse, SavedOpportunityCreate, SavedOpportunityResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/saved", response_model=SavedOpportunityResponse)
async def save_opportunity(
    saved_in: SavedOpportunityCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify project exists
    project = await db.get(Project, saved_in.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Check if already saved
    query = select(SavedOpportunity).where(
        SavedOpportunity.user_id == current_user.id,
        SavedOpportunity.project_id == saved_in.project_id
    )
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Opportunity already saved")
        
    saved = SavedOpportunity(
        user_id=current_user.id,
        project_id=saved_in.project_id,
        notes=saved_in.notes
    )
    db.add(saved)
    await db.commit()
    await db.refresh(saved)
    
    # Reload with project eager loaded to return full response
    stmt = select(SavedOpportunity).options(selectinload(SavedOpportunity.project)).where(SavedOpportunity.id == saved.id)
    res = await db.execute(stmt)
    return res.scalar_one()

@router.get("/saved", response_model=List[SavedOpportunityResponse])
async def list_saved_opportunities(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(SavedOpportunity).options(selectinload(SavedOpportunity.project)).where(
        SavedOpportunity.user_id == current_user.id
    ).order_by(SavedOpportunity.created_at.desc())
    
    result = await db.execute(query)
    return result.scalars().all()

@router.delete("/saved/{project_id}")
async def unsave_opportunity(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(SavedOpportunity).where(
        SavedOpportunity.user_id == current_user.id,
        SavedOpportunity.project_id == project_id
    )
    result = await db.execute(query)
    saved = result.scalar_one_or_none()
    
    if not saved:
        raise HTTPException(status_code=404, detail="Saved opportunity not found")
        
    await db.delete(saved)
    await db.commit()
    return {"status": "success"}
