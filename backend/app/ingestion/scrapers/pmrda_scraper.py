"""
Mock scraper for Pune Metropolitan Region Development Authority (PMRDA).
"""

import uuid

def mock_scrape_pmrda() -> list[dict]:
    """Simulates scraping new projects from the PMRDA website."""
    
    return [
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Pune Ring Road (Eastern Alignment)",
            "city": "Pune",
            "description": "A proposed 128-km circular road to divert heavy traffic outside the city.",
            "source_url": "https://pmrda.gov.in/ring-road"
        },
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Hinjawadi to Shivajinagar Metro Line 3",
            "city": "Pune",
            "description": "23.3 km elevated metro line connecting IT hub Hinjawadi to central Pune.",
            "source_url": "https://punemetrorail.org/line-3"
        }
    ]
