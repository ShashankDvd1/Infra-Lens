"""
LandScope AI — Celery App Configuration.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Celery Configuration
redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "landscope_ingestion",
    broker=redis_url,
    backend=redis_url,
    include=["app.ingestion.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)

# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    "scrape-lda-daily": {
        "task": "app.ingestion.tasks.scrape_lda",
        "schedule": crontab(hour=2, minute=0), # 2:00 AM daily
    },
    "scrape-lmrc-daily": {
        "task": "app.ingestion.tasks.scrape_lmrc",
        "schedule": crontab(hour=2, minute=30), # 2:30 AM daily
    },
    "scrape-universal-daily": {
        "task": "app.ingestion.tasks.scrape_all",
        "schedule": crontab(hour=3, minute=0), # 3:00 AM daily
    },
}
