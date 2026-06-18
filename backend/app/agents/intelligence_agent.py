"""
LandScope AI — Intelligence Agent.
Generates comprehensive AI summaries for infrastructure projects.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from app.models import Project, AISummary, Source
from app.rag.pipeline import get_llm

SUMMARY_PROMPT = """
You are an expert infrastructure analyst. Based on the provided project details and source documents, 
generate a comprehensive summary of the project.

Project Name: {project_name}
Project Type: {project_type}
City: {city}
Description: {description}

Source Documents:
{source_texts}

Your response must be a valid JSON object with the following keys exactly:
- what_is_being_built: A clear 2-3 sentence description of the physical infrastructure being constructed.
- why_it_matters: The strategic importance and primary goals of the project.
- expected_impact: Economic, social, or connectivity impact once completed.
- nearby_benefiting_areas: Names of specific localities or areas that will benefit most.

Return only JSON. Do not include markdown formatting or extra text.
"""

async def generate_project_summary(db: AsyncSession, project: Project) -> AISummary:
    """Generate and save an AI summary for a project using its sources."""
    
    # Gather sources
    source_texts = ""
    for idx, source in enumerate(project.sources):
        if source.content_text:
            source_texts += f"Source {idx+1} ({source.title}):\n{source.content_text}\n\n"
            
    if not source_texts:
        source_texts = "No detailed source documents available."
        
    prompt = PromptTemplate(
        template=SUMMARY_PROMPT,
        input_variables=["project_name", "project_type", "city", "description", "source_texts"]
    )
    
    llm = get_llm(fallback=False) # Use primary Llama 3.3 70B
    parser = JsonOutputParser()
    
    chain = prompt | llm | parser
    
    print(f"Generating summary for {project.name}...")
    try:
        result = await chain.ainvoke({
            "project_name": project.name,
            "project_type": project.project_type.value,
            "city": project.city,
            "description": project.description or "N/A",
            "source_texts": source_texts
        })
        
        # Save to DB
        summary = AISummary(
            project_id=project.id,
            what_is_being_built=result.get("what_is_being_built", ""),
            why_it_matters=result.get("why_it_matters", ""),
            expected_impact=result.get("expected_impact", ""),
            nearby_benefiting_areas=result.get("nearby_benefiting_areas", ""),
            model_used=llm.model_name
        )
        
        db.add(summary)
        await db.commit()
        return summary
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        raise

async def summarise_all_projects():
    from app.db.session import async_session
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    async with async_session() as session:
        # Load projects with their sources
        stmt = select(Project).options(selectinload(Project.sources))
        projects = (await session.execute(stmt)).scalars().all()
        
        for p in projects:
            # Skip if summary already exists
            summ_stmt = select(AISummary).where(AISummary.project_id == p.id)
            existing_summ = (await session.execute(summ_stmt)).scalar_one_or_none()
            if existing_summ:
                print(f"Summary for {p.name} already exists. Skipping.")
                continue
                
            try:
                await generate_project_summary(session, p)
                print(f"✅ Generated summary for {p.name}")
            except Exception as e:
                print(f"❌ Failed to generate summary for {p.name}: {e}")

if __name__ == "__main__":
    import asyncio
    import sys
    
    if "--summarise-all" in sys.argv:
        asyncio.run(summarise_all_projects())
