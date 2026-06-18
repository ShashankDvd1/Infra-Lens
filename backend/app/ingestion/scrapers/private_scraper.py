"""
Mock scraper for Private Real Estate portals (e.g., RERA listings, Builder sites).
"""

import uuid

def mock_scrape_private_lucknow() -> list[dict]:
    """Simulates scraping top private real estate projects in Lucknow."""
    
    return [
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Shalimar One World",
            "city": "Lucknow",
            "description": "A massive integrated township located on Shaheed Path, offering premium residential and commercial spaces.",
            "source_url": "https://shalimarcorp.com/oneworld"
        },
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Omaxe Metro City",
            "city": "Lucknow",
            "description": "A large integrated township offering a mix of plots, villas, and apartments along Raebareli Road.",
            "source_url": "https://omaxe.com/metro-city"
        },
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Rishita Mulberry Heights",
            "city": "Lucknow",
            "description": "A highly sought-after luxury gated community project located in Sushant Golf City.",
            "source_url": "https://rishita.in/mulberry-heights"
        },
        {
            "project_id": str(uuid.uuid4()),
            "project_name": "Oro Constella",
            "city": "Lucknow",
            "description": "A premium luxury living high-rise development on the Shaheed Path corridor.",
            "source_url": "https://orogroup.in/oro-constella"
        }
    ]
