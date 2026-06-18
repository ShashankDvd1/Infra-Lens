"""
LandScope AI — AI API endpoints (Ask AI + Summary generation).
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.ai import AskAIRequest, AskAIResponse, SummaryGenerateRequest
from app.config import get_settings

router = APIRouter()


@router.post("/ask", response_model=AskAIResponse)
async def ask_ai(
    request: AskAIRequest,
    db: AsyncSession = Depends(get_db),
):
    """Ask AI — conversational query with RAG-grounded response."""
    from app.rag.pipeline import ask_ai_pipeline
    
    answer, sources = await ask_ai_pipeline(request.query, db)

    return AskAIResponse(
        answer=answer,
        sources=sources,
        recommended_areas=[],
    )


@router.post("/summary/{project_id}")
async def generate_summary(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Generate or refresh AI summary for a specific project."""
    from sqlalchemy import select
    from app.models import Project
    from sqlalchemy.orm import selectinload
    from app.agents.intelligence_agent import generate_project_summary
    
    # Check if project exists and load its sources
    stmt = select(Project).where(Project.id == project_id).options(selectinload(Project.sources))
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    try:
        summary = await generate_project_summary(db, project)
        return {
            "status": "success",
            "project_id": str(project_id),
            "summary_id": str(summary.id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
