"""
LandScope AI — Seed Script.
Populates the database with initial verified projects and areas.
"""

import asyncio
import os
import sys
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2.elements import WKTElement

from app.db.session import async_session
from app.models import Project, Area, Source, GrowthIndicator
from app.db.seed_data import SEED_PROJECTS, SEED_AREAS

async def seed_data():
    async with async_session() as session:
        print("Starting data seed...")
        
        # 1. Seed Areas
        for area_data in SEED_AREAS:
            # Check if exists
            result = await session.execute(select(Area).where(Area.slug == area_data["slug"]))
            if result.first():
                print(f"Area {area_data['name']} already exists. Skipping.")
                continue
                
            print(f"Adding Area: {area_data['name']}")
            
            # Create centroid Point
            centroid = f"SRID=4326;POINT({area_data['longitude']} {area_data['latitude']})"
            
            area = Area(
                name=area_data["name"],
                slug=area_data["slug"],
                city=area_data["city"],
                avg_price_sqft=area_data["avg_price_sqft"],
                growth_rate_pct=area_data["growth_rate_pct"],
                description=area_data["description"],
                connectivity_data=area_data["connectivity_data"],
                centroid=WKTElement(centroid, srid=4326)
            )
            session.add(area)
            await session.flush()  # To get the ID
            
            # Add Growth Indicators
            for gi_data in area_data["growth_indicators"]:
                # Parse date if it's a string
                measured_date = gi_data["measured_date"]
                if isinstance(measured_date, str):
                    measured_date = datetime.strptime(measured_date, "%Y-%m-%d").date()
                    
                gi = GrowthIndicator(
                    area_id=area.id,
                    indicator_type=gi_data["indicator_type"],
                    value=gi_data["value"],
                    unit=gi_data["unit"],
                    measured_date=measured_date
                )
                session.add(gi)
        
        # 2. Seed Projects
        for proj_data in SEED_PROJECTS:
            # Check if exists
            result = await session.execute(select(Project).where(Project.slug == proj_data["slug"]))
            if result.first():
                print(f"Project {proj_data['name']} already exists. Skipping.")
                continue
                
            print(f"Adding Project: {proj_data['name']}")
            
            # Create location Point
            location = f"SRID=4326;POINT({proj_data['longitude']} {proj_data['latitude']})"
            
            announced_date = proj_data["announced_date"]
            if isinstance(announced_date, str):
                announced_date = datetime.strptime(announced_date, "%Y-%m-%d").date() if announced_date else None
                
            expected_completion = proj_data["expected_completion"]
            if isinstance(expected_completion, str):
                expected_completion = datetime.strptime(expected_completion, "%Y-%m-%d").date() if expected_completion else None
                
            project = Project(
                name=proj_data["name"],
                slug=proj_data["slug"],
                project_type=proj_data["project_type"],
                status=proj_data["status"],
                description=proj_data["description"],
                city=proj_data["city"],
                district=proj_data["district"],
                authority=proj_data["authority"],
                announced_date=announced_date,
                expected_completion=expected_completion,
                budget_crore=proj_data["budget_crore"],
                impact_radius_km=proj_data["impact_radius_km"],
                is_verified=True,
                verification_status="verified",
                location=WKTElement(location, srid=4326)
            )
            session.add(project)
            await session.flush()
            
            # Add Sources
            for source_data in proj_data["sources"]:
                published_date = source_data["published_date"]
                if isinstance(published_date, str):
                    published_date = datetime.strptime(published_date, "%Y-%m-%d").date() if published_date else None
                    
                source = Source(
                    project_id=project.id,
                    source_type=source_data["source_type"],
                    title=source_data["title"],
                    url=source_data["url"],
                    authority_name=source_data["authority_name"],
                    published_date=published_date,
                    content_text=source_data["content_text"]
                )
                session.add(source)

        await session.commit()
        print("Seed data successfully loaded!")

if __name__ == "__main__":
    asyncio.run(seed_data())
