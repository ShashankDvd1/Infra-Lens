"""
Mock scraper for Lucknow Development Authority (LDA).
"""

import uuid

def mock_scrape_lda() -> list[dict]:
    """Simulates scraping new projects from the LDA website."""
    
    return [
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Lucknow IT City",
            "city": "Lucknow",
            "description": "An expansive 1,696 to 2,858 acres project along Sultanpur Road to build a dedicated technology and industrial zone.",
            "source_url": "https://lda.up.gov.in/it-city-sultanpur-road"
        },
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Udyog Nagar Expansion",
            "city": "Lucknow",
            "description": "A 5,610-acre industrial and urban expansion project located along the Agra Expressway under the Mukhyamantri Shahri Vistarikaran Yojana.",
            "source_url": "https://lda.up.gov.in/udyog-nagar"
        },
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Lucknow Aerocity",
            "city": "Lucknow",
            "description": "A 1,500-acre development project featuring commercial offices, convention centers, parks, and hotels.",
            "source_url": "https://lda.up.gov.in/aerocity"
        }
    ]
