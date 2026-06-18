"""
LandScope AI — Opportunity Scoring Service.
Evaluates projects based on multiple dimensions to generate an Opportunity Score.
"""

from typing import Dict, Any

def calculate_opportunity_score(project_data: Dict[str, Any], area_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Calculate an opportunity score based on 5 dimensions:
    1. Infrastructure Proximity (Metro, Highway, Airport)
    2. Area Growth Rate (if available)
    3. Project Status (Completed vs Under Construction)
    4. Type of Project (Commercial vs Residential impact)
    5. Distress/Value factor (Placeholder for Phase 3)
    """
    
    score_breakdown = {
        "infrastructure": 0,
        "growth": 0,
        "status": 0,
        "type": 0,
        "value": 0
    }
    
    desc = project_data.get("description", "").lower()
    
    # 1. Infrastructure Proximity (Max 30)
    if "expressway" in desc or "highway" in desc: score_breakdown["infrastructure"] += 10
    if "airport" in desc or "aerocity" in desc: score_breakdown["infrastructure"] += 10
    if "metro" in desc or "transit" in desc: score_breakdown["infrastructure"] += 10
    
    # 2. Area Growth Rate (Max 25)
    if area_data and "growth_rate_pct" in area_data:
        growth = area_data["growth_rate_pct"]
        if growth > 15:
            score_breakdown["growth"] = 25
        elif growth > 10:
            score_breakdown["growth"] = 15
        elif growth > 5:
            score_breakdown["growth"] = 10
        else:
            score_breakdown["growth"] = 5
    else:
        # Default average growth
        score_breakdown["growth"] = 10
        
    # 3. Project Status (Max 15)
    status = project_data.get("status", "").lower()
    if status == "completed":
        score_breakdown["status"] = 15
    elif status == "under_construction":
        score_breakdown["status"] = 10
    elif status == "planned":
        score_breakdown["status"] = 5
        
    # 4. Project Type (Max 15)
    p_type = project_data.get("project_type", "").lower()
    if p_type in ["commercial", "industrial"]:
        score_breakdown["type"] = 15
    elif p_type == "residential":
        score_breakdown["type"] = 10
    else:
        score_breakdown["type"] = 5
        
    # 5. Value/Distress Factor (Max 15)
    # Placeholder for Phase 3 logic
    if "distress" in desc or "auction" in desc:
        score_breakdown["value"] = 15
    elif "affordable" in desc:
        score_breakdown["value"] = 10
    else:
        score_breakdown["value"] = 5
        
    total_score = sum(score_breakdown.values())
    
    # Cap at 100
    total_score = min(100, total_score)
    
    return {
        "total_score": total_score,
        "breakdown": score_breakdown,
        "grade": get_score_grade(total_score)
    }
    
def get_score_grade(score: int) -> str:
    """Return letter grade for score."""
    if score >= 85: return "A+"
    if score >= 75: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    return "D"
