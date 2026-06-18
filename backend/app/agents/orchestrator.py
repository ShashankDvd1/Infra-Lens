"""
LandScope AI — LangGraph Orchestrator.
Coordinates the multi-agent workflow for processing new infrastructure projects.
"""

from typing import Dict, Any, TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END

from app.agents.research_agent import run_research_agent
from app.agents.verification_agent import run_verification_agent
from app.agents.recommendation_agent import run_recommendation_agent

# Define the State for LangGraph
class AgentState(TypedDict):
    project_id: str
    project_name: str
    city: str
    description: str
    
    # Populated by Research Agent
    research_dossier: str
    
    # Populated by Verification Agent
    is_verified: bool
    verification_notes: str
    
    # Populated by Recommendation Agent
    opportunity_score: int
    recommended_areas: list[str]
    investment_strategy: str

# Define conditional routing
def verification_router(state: AgentState) -> str:
    if state.get("is_verified", False):
        return "recommend"
    else:
        return "end"

# Build the Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("research", run_research_agent)
workflow.add_node("verify", run_verification_agent)
workflow.add_node("recommend", run_recommendation_agent)

# Add Edges
workflow.set_entry_point("research")
workflow.add_edge("research", "verify")

# Conditional Edge from Verify
workflow.add_conditional_edges(
    "verify",
    verification_router,
    {
        "recommend": "recommend",
        "end": END
    }
)

workflow.add_edge("recommend", END)

# Compile
app = workflow.compile()

async def process_project_pipeline(initial_state: dict) -> dict:
    """Entry point to run the full LangGraph pipeline."""
    final_state = await app.ainvoke(initial_state)
    
    # Calculate simple opportunity score based on keywords in description
    score = 50
    desc = final_state.get("description", "").lower()
    if "expressway" in desc or "highway" in desc: score += 15
    if "airport" in desc or "aerocity" in desc: score += 20
    if "metro" in desc or "transit" in desc: score += 15
    if "it city" in desc or "tech" in desc: score += 10
    
    final_state["opportunity_score"] = min(100, score)
    return final_state
