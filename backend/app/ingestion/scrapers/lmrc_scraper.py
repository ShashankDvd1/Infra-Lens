"""
Mock scraper for Lucknow Metro Rail Corporation (LMRC).
"""

import uuid

def mock_scrape_lmrc() -> list[dict]:
    """Simulates scraping new projects from the LMRC website."""
    
    return [
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Lucknow Metro East-West Corridor",
            "city": "Lucknow",
            "description": "New metro line connecting Charbagh to Vasant Kunj with 12 stations (7 underground).",
            "source_url": "https://lmrcl.com/east-west-corridor"
        }
    ]
