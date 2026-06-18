"""
LandScope AI — RAG Retriever.
Searches pgvector embeddings and reranks results.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict

from app.models import ProjectEmbedding, Project
from app.rag.embeddings import get_embedding_service
from app.config import get_settings

settings = get_settings()

async def search_projects(db: AsyncSession, query: str, limit: int = 5) -> List[Dict]:
    """Retrieve similar projects based on vector search."""
    # 1. Embed query
    embedder = get_embedding_service()
    query_vector = embedder.embed_text(query)
    
    # 2. Vector search via pgvector (cosine distance)
    # distance operator is <=>. We order by distance ascending.
    stmt = (
        select(Project, ProjectEmbedding.content, ProjectEmbedding.embedding.cosine_distance(query_vector).label("distance"))
        .join(Project, Project.id == ProjectEmbedding.project_id)
        .order_by("distance")
        .limit(settings.RAG_TOP_K)
    )
    
    result = await db.execute(stmt)
    rows = result.all()
    
    # Simple thresholding
    matches = []
    for row in rows:
        project, content, distance = row[0], row[1], row[2]
        similarity = 1.0 - distance
        if similarity >= settings.RAG_SIMILARITY_THRESHOLD:
            matches.append({
                "project": project,
                "content": content,
                "score": similarity
            })
            
    # In a full implementation, we would add the cross-encoder reranker here
    # For MVP, we'll just return the top K based on vector similarity
    
    # Sort descending by score just in case, and take top limit
    matches = sorted(matches, key=lambda x: x["score"], reverse=True)[:limit]
    
    return matches
