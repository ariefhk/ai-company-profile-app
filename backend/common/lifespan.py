"""
Application lifespan management for FastAPI.

Handles startup initialization (logging, config) and graceful shutdown
using FastAPI's lifespan context manager protocol.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.logging import get_logger, setup_logging
from core.config import get_configs
from jobs.registry import register_jobs
from jobs.scheduler import scheduler

configs = get_configs()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Manage application startup and shutdown lifecycle.

    This async context manager is passed to the FastAPI app constructor
    and controls resource initialization and cleanup. Everything before
    ``yield`` runs on startup; everything after runs on shutdown.

    Args:
        app: The FastAPI application instance.

    Yields:
        None: Control is handed to the application to serve requests.
    """
    # --- Startup ---
    setup_logging()
    logger.info(
        "Starting %s v%s [%s]",
        configs.APP_NAME,
        configs.APP_VERSION,
        configs.APP_ENV,
    )

    if configs.SCHEDULER_ENABLED:
        register_jobs()
        scheduler.start()
        logger.info(
            "Scheduler started with %d job(s)", len(scheduler.get_jobs())
        )

    yield

    # --- Shutdown ---
    if configs.SCHEDULER_ENABLED and scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
    logger.info("Shutting down %s", configs.APP_NAME)
