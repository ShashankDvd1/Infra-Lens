"""
LandScope AI — Celery Tasks.
Defines background jobs for scraping and processing data.
"""

from app.ingestion.celery_app import celery_app
from app.ingestion.scrapers.lda_scraper import mock_scrape_lda
from app.ingestion.scrapers.lmrc_scraper import mock_scrape_lmrc
from app.ingestion.scrapers.private_scraper import mock_scrape_private_lucknow
from app.agents.orchestrator import process_project_pipeline
from app.services.notification_service import send_alert_email
from app.models.alert import AlertSubscription
from app.db.session import async_session
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import asyncio

def run_async(coro):
    """Helper to run async code in Celery sync context."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

@celery_app.task(name="app.ingestion.tasks.scrape_lda")
def scrape_lda():
    print("Starting LDA scraping job...")
    projects = mock_scrape_lda()
    print(f"Scraped {len(projects)} projects from LDA.")
    
    for proj in projects:
        # Pass to LangGraph Orchestrator
        final_state = run_async(process_project_pipeline(proj))
        print(f"Processed project: {final_state['project_name']} | Verified: {final_state['is_verified']}")
        # Check alerts
        run_async(check_alerts_for_project(final_state))
        
    return f"Processed {len(projects)} LDA projects."

@celery_app.task(name="app.ingestion.tasks.scrape_lmrc")
def scrape_lmrc():
    print("Starting LMRC scraping job...")
    projects = mock_scrape_lmrc()
    print(f"Scraped {len(projects)} projects from LMRC.")
    
    for proj in projects:
        final_state = run_async(process_project_pipeline(proj))
        print(f"Processed project: {final_state['project_name']} | Verified: {final_state['is_verified']}")
        run_async(check_alerts_for_project(final_state))
        
    return f"Processed {len(projects)} LMRC projects."

@celery_app.task
def scrape_private():
    """Scrape private real estate developments."""
    projects = mock_scrape_private_lucknow()
    print(f"Found {len(projects)} new private projects. Triggering AI pipeline...")
    
    for proj in projects:
        final_state = run_async(process_project_pipeline(proj))
        print(f"Processed private project: {final_state['project_name']} | Verified: {final_state['is_verified']}")
        run_async(check_alerts_for_project(final_state))
        
    return f"Processed {len(projects)} private projects."

@celery_app.task(name="app.ingestion.tasks.scrape_all")
def scrape_all():
    from app.ingestion.scrapers.generic_scraper import run_universal_scraper
    import uuid
    
    print("Starting Universal Scraping Job...")
    projects = run_async(run_universal_scraper())
    print(f"Extracted {len(projects)} total projects from web.")
    
    for proj in projects:
        if "project_id" not in proj:
            proj["project_id"] = str(uuid.uuid4())
            
        final_state = run_async(process_project_pipeline(proj))
        print(f"Processed project: {final_state.get('project_name')} | Verified: {final_state.get('is_verified')}")
        run_async(check_alerts_for_project(final_state))
        
    return f"Processed {len(projects)} projects."

async def check_alerts_for_project(project_data: dict):
    """Check if the newly scraped project matches any user alert subscriptions."""
    if not project_data.get("is_verified"):
        return
        
    async with async_session() as db:
        result = await db.execute(select(AlertSubscription).options(selectinload(AlertSubscription.user)))
        alerts = result.scalars().all()
        
        for alert in alerts:
            if alert.user and alert.user.email:
                send_alert_email(
                    email=alert.user.email,
                    subject=f"New Infrastructure Alert: {project_data.get('project_name')}",
                    message=f"A new project was just announced in {project_data.get('city')}:\n{project_data.get('description')}\n\nOpportunity Score: {project_data.get('opportunity_score')}"
                )
