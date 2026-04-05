"""
APScheduler configuration and singleton instance.

Provides a single AsyncIOScheduler that is started/stopped
via the FastAPI lifespan. Jobs are registered in jobs/registry.py.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(
    job_defaults={
        "coalesce": True,  # Combine multiple missed runs into one
        "max_instances": 1,  # Prevent overlapping runs of the same job
        "misfire_grace_time": 60,  # Allow 60s late execution before skipping
    },
)
