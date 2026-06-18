from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel

from app.db.session import get_db
from app.models.alert import AlertSubscription
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

class AlertCreate(BaseModel):
    area_slug: str | None = None
    project_type: str | None = None
    min_opportunity_score: int | None = None

class AlertResponse(BaseModel):
    id: str
    area_slug: str | None
    project_type: str | None
    min_opportunity_score: int | None
    is_active: bool

    class Config:
        from_attributes = True

@router.post("/", response_model=AlertResponse)
async def create_alert(
    alert_in: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    alert = AlertSubscription(
        user_id=current_user.id,
        area_slug=alert_in.area_slug,
        project_type=alert_in.project_type,
        min_opportunity_score=alert_in.min_opportunity_score
    )
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(AlertSubscription).where(AlertSubscription.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()

@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(AlertSubscription).where(
        AlertSubscription.id == alert_id,
        AlertSubscription.user_id == current_user.id
    )
    result = await db.execute(query)
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
        
    await db.delete(alert)
    await db.commit()
    return {"status": "success"}
