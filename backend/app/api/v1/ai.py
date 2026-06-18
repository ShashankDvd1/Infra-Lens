"""
LandScope AI — AI API endpoints (Ask AI + Summary generation).
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.ai import (
    AskAIRequest, AskAIResponse, SummaryGenerateRequest,
    InvestRecommendationRequest, InvestRecommendationResponse
)
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


@router.post("/recommend", response_model=InvestRecommendationResponse)
async def get_recommendation(
    request: InvestRecommendationRequest,
    db: AsyncSession = Depends(get_db),
):
    """Get personalized investment strategy backed by verified projects."""
    from sqlalchemy import select
    from app.models import Project
    from sqlalchemy.orm import selectinload
    from app.rag.pipeline import get_llm
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    
    # 1. Fetch all verified projects and their sources
    stmt = select(Project).where(Project.is_verified == True).options(selectinload(Project.sources))
    result = await db.execute(stmt)
    projects = result.scalars().all()
    
    if not projects:
        return InvestRecommendationResponse(
            strategy="No verified projects available to base recommendations on.",
            target_areas=[],
            expected_roi="N/A",
            rationale="No verified infrastructure projects are currently in our database.",
            backed_projects=[]
        )
        
    # 2. Build projects context
    context_parts = []
    for p in projects:
        sources_list = []
        for s in p.sources:
            sources_list.append(f"'{s.title}' ({s.url or 'no URL'})")
        sources_str = ", ".join(sources_list) if sources_list else "No official sources found"
        
        context_parts.append(
            f"Project ID: {p.id}\n"
            f"Project Name: {p.name}\n"
            f"Type: {p.project_type.value}\n"
            f"Status: {p.status.value}\n"
            f"Budget: {p.budget_crore or 'Unknown'} Crore\n"
            f"Description: {p.description or 'No description'}\n"
            f"Sources: {sources_str}"
        )
    context_str = "\n\n".join(context_parts)
    
    # 3. Create the prompt
    system_prompt = f"""
You are the LandScope AI Investment Advisor.
Analyze the following list of real, verified infrastructure projects in Lucknow:

{context_str}

A user is seeking investment advice. Here is their profile:
- Budget: {request.budget} Lakhs (Note: 100 Lakhs = 1 Crore)
- Risk Tolerance: {request.risk}

Recommend a customized investment strategy backed strictly by one or more of the real projects listed above.
You must include the actual project ID(s) and project name(s) that support your recommendation.
Your recommendation must be fully grounded in the provided projects. Do not invent projects.

Return a valid JSON object with the following fields:
- strategy: A direct recommendation of what asset types and areas to focus on (e.g. residential land, commercial space, logistics, etc.).
- target_areas: A list of 1 to 3 specific, real areas in Lucknow that are near the projects and would benefit (e.g., Gomti Nagar, Shaheed Path, Kanpur Road, etc. based on the projects).
- expected_roi: A realistic estimated annual return range (e.g., "12-15% p.a." or "15-18% p.a.") based on the projects.
- rationale: A detailed paragraph explaining why this strategy fits their budget and risk level, referencing the specific project name(s) and source(s) (name of authority or article title) that back it up.
- backed_projects: An array of objects, each representing a project that supports this recommendation:
  - id: The project's ID (UUID string).
  - name: The project's name.
  - source_title: The title of the main source document backing the project.
  - source_url: The URL of the main source document (if any).

Ensure the response is valid JSON. Return ONLY the JSON object.
"""
    
    prompt_template = PromptTemplate(
        template="{prompt_text}",
        input_variables=["prompt_text"]
    )
    
    # Use Llama 3.3 70B for high-quality recommendations
    llm = get_llm(fallback=False)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser
    
    try:
        response = await chain.ainvoke({"prompt_text": system_prompt})
        
        # Validate that the returned backed projects actually exist
        project_ids = {str(p.id) for p in projects}
        validated_backed_projects = []
        for bp in response.get("backed_projects", []):
            if bp.get("id") in project_ids:
                validated_backed_projects.append(bp)
                
        return InvestRecommendationResponse(
            strategy=response.get("strategy", ""),
            target_areas=response.get("target_areas", []),
            expected_roi=response.get("expected_roi", ""),
            rationale=response.get("rationale", ""),
            backed_projects=validated_backed_projects
        )
    except Exception as e:
        print(f"Recommendation generation failed: {e}")
        # Return fallback response using one of the projects directly
        default_proj = projects[0]
        default_source = default_proj.sources[0] if default_proj.sources else None
        return InvestRecommendationResponse(
            strategy=f"Focus on residential opportunities near the {default_proj.name}.",
            target_areas=[default_proj.city],
            expected_roi="12-15% p.a.",
            rationale=f"This recommendation is backed by the verified project {default_proj.name}.",
            backed_projects=[{
                "id": str(default_proj.id),
                "name": default_proj.name,
                "source_title": default_source.title if default_source else "Official Announcement",
                "source_url": default_source.url if default_source else None
            }]
        )
