"""
Mock scraper for Hyderabad Metropolitan Development Authority (HMDA).
"""

import uuid

def mock_scrape_hmda() -> list[dict]:
    """Simulates scraping new projects from the HMDA website."""
    
    return [
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Hyderabad Airport Express Metro",
            "city": "Hyderabad",
            "description": "31 km metro line connecting Mindspace Junction to Rajiv Gandhi International Airport.",
            "source_url": "https://hmrl.co.in/airport-express"
        },
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Regional Ring Road (RRR)",
            "city": "Hyderabad",
            "description": "340 km long, 4-lane access-controlled expressway encircling the city beyond the ORR.",
            "source_url": "https://hmda.gov.in/rrr"
        }
    ]
