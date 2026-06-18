"""
LandScope AI — Post-Ingestion Hooks.
Runs auto-embed, verify, and summarize on newly ingested projects.
"""

from app.rag.embeddings import get_embedding_service
from app.agents.orchestrator import process_project_pipeline
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Project, ProjectEmbedding
import asyncio

async def run_post_ingestion_hooks(db: AsyncSession, project: Project):
    """Run all post-ingestion tasks for a new project."""
    
    # 1. Generate and store embeddings
    embedder = get_embedding_service()
    vector = embedder.embed_text(project.description)
    
    emb = ProjectEmbedding(
        project_id=project.id,
        content=project.description,
        embedding=vector
    )
    db.add(emb)
    await db.commit()
    
    # 2. Run LangGraph Orchestrator (Verify, Score)
    state = {
        "project_id": str(project.id),
        "project_name": project.name,
        "city": project.city,
        "description": project.description
    }
    
    final_state = await process_project_pipeline(state)
    
    # Update project with score and verification
    project.opportunity_score = final_state.get("opportunity_score", 50)
    project.is_verified = final_state.get("is_verified", False)
    
    await db.commit()
    
    return final_state
