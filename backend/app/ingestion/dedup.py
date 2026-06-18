"""
LandScope AI — Deduplication Logic.
Ensures we don't insert duplicate projects from different sources.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Project

async def is_duplicate(db: AsyncSession, project_name: str, city: str) -> bool:
    """Check if a project with a very similar name already exists in the same city."""
    # Simple check for MVP: exact name match (case-insensitive) in the same city
    stmt = select(Project).where(
        Project.name.ilike(project_name),
        Project.city.ilike(city)
    )
    result = await db.execute(stmt)
    existing = result.scalars().first()
    
    return existing is not None
