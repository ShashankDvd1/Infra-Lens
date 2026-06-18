"""
LandScope AI — Recommendation Agent.
Determines opportunity scores and recommends areas based on the project.
"""

from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.rag.pipeline import get_llm

RECOMMENDATION_PROMPT = """
You are the LandScope AI Recommendation Agent.
Based on the verified project details and research, suggest 2-3 specific real estate investment strategies or areas that will benefit.

Project Name: {project_name}
City: {city}
Verified Notes: {verification_notes}

Return a JSON object with:
- opportunity_score: integer from 1 to 100 indicating investment potential.
- recommended_areas: list of strings (e.g., ["Area 1", "Area 2"])
- investment_strategy: brief paragraph explaining why these areas are good.
"""

async def run_recommendation_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"--- [Recommendation Agent] Scoring: {state['project_name']} ---")
    
    if not state.get("is_verified", False):
        return {
            "opportunity_score": 0,
            "recommended_areas": [],
            "investment_strategy": "Project could not be verified. Investment not recommended."
        }
        
    prompt = PromptTemplate(
        template=RECOMMENDATION_PROMPT,
        input_variables=["project_name", "city", "verification_notes"]
    )
    
    llm = get_llm(fallback=False) # Use 70B for reasoning
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    
    try:
        response = await chain.ainvoke({
            "project_name": state.get("project_name", ""),
            "city": state.get("city", "Lucknow"),
            "verification_notes": state.get("verification_notes", "")
        })
        
        return {
            "opportunity_score": response.get("opportunity_score", 50),
            "recommended_areas": response.get("recommended_areas", []),
            "investment_strategy": response.get("investment_strategy", "")
        }
    except Exception as e:
        print(f"Recommendation parsing error: {e}")
        return {
            "opportunity_score": 50,
            "recommended_areas": [],
            "investment_strategy": "Failed to generate strategy."
        }
