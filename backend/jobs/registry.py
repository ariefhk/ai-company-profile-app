"""
Job registry — central place to register all scheduled jobs.

Add new jobs here so they are picked up automatically on startup.
"""

from jobs.heartbeat import heartbeat
from jobs.scheduler import scheduler


def register_jobs() -> None:
    """Register all scheduled jobs with the scheduler.

    Call this once before ``scheduler.start()``.
    To add a new job, append an ``scheduler.add_job(...)`` call below.
    """

    scheduler.add_job(
        heartbeat,
        trigger="interval",
        seconds=60,
        id="heartbeat",
        replace_existing=True,
    )

    # --- Add more jobs below ---
    # scheduler.add_job(
    #     your_task_function,
    #     trigger="cron",
    #     hour=2,
    #     minute=0,
    #     id="nightly_cleanup",
    #     replace_existing=True,
    # )
