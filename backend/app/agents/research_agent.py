"""
LandScope AI — Research Agent.
Simulates fetching context, master plans, and public records for a project.
"""

from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from app.rag.pipeline import get_llm

RESEARCH_PROMPT = """
You are the LandScope AI Research Agent.
You are given initial details about an infrastructure project.
Your job is to generate a comprehensive "research dossier" containing:
1. Likely contractors or authorities involved.
2. Potential related nearby infrastructure (e.g., feeder roads for an expressway).
3. Any typical regulatory hurdles for this type of project.

Project Name: {project_name}
City: {city}
Description: {description}

Generate the dossier as a detailed plain text report.
"""

async def run_research_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"--- [Research Agent] Researching: {state['project_name']} ---")
    
    prompt = PromptTemplate(
        template=RESEARCH_PROMPT,
        input_variables=["project_name", "city", "description"]
    )
    
    llm = get_llm(fallback=True) # Use faster fallback model for basic research
    chain = prompt | llm
    
    response = await chain.ainvoke({
        "project_name": state.get("project_name", ""),
        "city": state.get("city", "Lucknow"),
        "description": state.get("description", "")
    })
    
    # Update state with research dossier
    return {"research_dossier": response.content}
