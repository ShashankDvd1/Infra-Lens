"""
LandScope AI — Verification Agent.
Validates facts against the source context to prevent hallucination.
"""

from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.rag.pipeline import get_llm

VERIFICATION_PROMPT = """
You are the LandScope AI Verification Agent.
Review the following research dossier and initial project details.
Identify any claims that seem highly speculative or contradict standard infrastructure norms in India.

Project Name: {project_name}
Dossier:
{research_dossier}

Return a JSON object with:
- is_verified: boolean (true if claims seem reasonable, false if highly speculative)
- verification_notes: string explaining your reasoning
"""

async def run_verification_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"--- [Verification Agent] Verifying: {state['project_name']} ---")
    
    prompt = PromptTemplate(
        template=VERIFICATION_PROMPT,
        input_variables=["project_name", "research_dossier"]
    )
    
    llm = get_llm(fallback=True)
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    
    try:
        response = await chain.ainvoke({
            "project_name": state.get("project_name", ""),
            "research_dossier": state.get("research_dossier", "No dossier provided.")
        })
        
        return {
            "is_verified": response.get("is_verified", False),
            "verification_notes": response.get("verification_notes", "")
        }
    except Exception as e:
        print(f"Verification parsing error: {e}")
        return {"is_verified": False, "verification_notes": "Failed to parse verification."}
