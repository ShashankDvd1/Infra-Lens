"""
LandScope AI — Generic LLM-powered Scraper.
Scrapes URLs from scraped_sites.json and uses LangChain/Groq to extract infrastructure projects.
"""

import json
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.rag.pipeline import get_llm
from app.config import get_settings

EXTRACTION_PROMPT = """
You are an expert infrastructure data extractor. 
Analyze the following text scraped from a government or developer website ({url}).
Extract any real estate, infrastructure, or development projects mentioned.

Text:
{text}

Return a valid JSON array of objects, where each object has:
- project_name (string)
- city (string)
- description (string)
- project_type (string, e.g. "Residential", "Commercial", "Expressway", "Metro")

Return ONLY the JSON array.
"""

async def scrape_site_content(url: str) -> str:
    """Fetch and parse text from a URL."""
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer"]):
                script.extract()
                
            text = soup.get_text(separator=' ', strip=True)
            # Truncate text if it's too long for the LLM
            return text[:15000] 
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""

async def extract_projects_from_text(text: str, url: str) -> List[Dict[str, Any]]:
    """Use LLM to extract project details from raw text."""
    if len(text) < 100:
        return []
        
    prompt = PromptTemplate(
        template=EXTRACTION_PROMPT,
        input_variables=["text", "url"]
    )
    
    llm = get_llm(fallback=True) # Use faster model for extraction
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    
    try:
        results = await chain.ainvoke({"text": text, "url": url})
        if isinstance(results, list):
            for r in results:
                r["source_url"] = url
            return results
        return []
    except Exception as e:
        print(f"Extraction failed for {url}: {e}")
        return []

async def run_universal_scraper() -> List[Dict[str, Any]]:
    """Run scraper on all sites in scraped_sites.json."""
    sites_path = Path(__file__).parent.parent.parent.parent / "scraped_sites.json"
    
    if not sites_path.exists():
        print("scraped_sites.json not found!")
        return []
        
    with open(sites_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    all_extracted_projects = []
    
    # Just sample a few URLs to prevent massive LLM usage in one go
    limit = 3
    count = 0
    
    for site_group in data.get("scraped_sites", []):
        for url in site_group.get("urls", []):
            if count >= limit:
                break
                
            print(f"Scraping: {url}")
            text = await scrape_site_content(url)
            projects = await extract_projects_from_text(text, url)
            
            if projects:
                all_extracted_projects.extend(projects)
                print(f"Extracted {len(projects)} projects from {url}")
                
            count += 1
            
    return all_extracted_projects

if __name__ == "__main__":
    import asyncio
    projects = asyncio.run(run_universal_scraper())
    print(f"Total projects extracted: {len(projects)}")
