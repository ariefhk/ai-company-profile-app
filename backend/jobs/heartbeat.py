"""Heartbeat job — periodic health check log to confirm the scheduler is alive."""

from common.logging import get_logger

logger = get_logger(__name__)


async def heartbeat() -> None:
    """Log a heartbeat message. Runs every 60 seconds by default."""
    logger.info("Heartbeat: scheduler is alive")
