"""
Centralized logging configuration for the application.

Provides two formatters:
- JSONFormatter: Structured output for production (machine-parseable, log aggregator friendly).
- TextFormatter: Human-readable output for local development.

Usage::

    from common.logging import setup_logging, get_logger

    setup_logging()  # Call once at app startup
    logger = get_logger(__name__)
    logger.info("Server started", extra={"extra_data": {"port": 8000}})
"""

import json
import logging
import sys
from datetime import datetime, timezone

from core.config import get_configs


class JSONFormatter(logging.Formatter):
    """
    Structured JSON log formatter for production environments.

    Emits one JSON object per log line, compatible with log aggregators
    such as ELK, Datadog, and CloudWatch. Automatically includes
    ``request_id`` and ``extra_data`` when attached to the log record.

    Output example::

        {
            "timestamp": "2026-04-03T12:00:00+00:00",
            "level": "ERROR",
            "message": "Connection refused",
            "logger": "app.db",
            "module": "db",
            "function": "connect",
            "line": 42,
            "request_id": "abc-123",
            "exception": {"type": "ConnectionError", "message": "..."}
        }
    """

    def format(self, record: logging.LogRecord) -> str:
        # Base structured payload — always present in every log line
        log_data = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Correlation ID for tracing requests across services.
        # Injected via middleware: extra={"request_id": "..."}
        request_id = getattr(record, "request_id", None)
        if request_id is not None:
            log_data["request_id"] = request_id

        # Arbitrary structured context (e.g. user_id, payload size).
        # Pass via: logger.info("msg", extra={"extra_data": {...}})
        extra_data = getattr(record, "extra_data", None)
        if extra_data is not None:
            log_data["data"] = extra_data

        # Capture exception type and message without full traceback
        # to keep log lines compact; full stack is in stderr by default
        if record.exc_info:
            exc_type, exc_value = (
                record.exc_info[0],
                record.exc_info[1],
            )
            if exc_type is not None and exc_value is not None:
                log_data["exception"] = {
                    "type": exc_type.__name__,
                    "message": str(exc_value),
                }

        return json.dumps(log_data)


class TextFormatter(logging.Formatter):
    """
    Human-readable formatter for local development.

    Output example::

        2026-04-03 12:00:00 | ERROR    | abc-123 | app.db:connect:42 - Connection refused
    """

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        # Falls back to "-" when no request context is available (e.g. startup logs)
        request_id = getattr(record, "request_id", "-")
        return (
            f"{timestamp} | {record.levelname:<8} | {request_id} | "
            f"{record.name}:{record.funcName}:{record.lineno} "
            f"- {record.getMessage()}"
        )


def setup_logging() -> None:
    """
    Configure application-wide logging. Call once during startup.

    Behavior is controlled by application config:
    - ``LOG_LEVEL``: Root log level (e.g. DEBUG, INFO, WARNING).
    - ``LOG_FORMAT``: ``"json"`` for production, anything else for text.
    - ``DEBUG``: When True, SQLAlchemy engine logs at INFO level.
    """
    configs = get_configs()

    # Configure root logger so all child loggers inherit the level
    root_logger = logging.getLogger()
    root_logger.setLevel(configs.LOG_LEVEL)

    # Remove any handlers added by imported libraries to avoid duplicates
    root_logger.handlers.clear()

    # Write to stdout (not stderr) so container runtimes
    # (Docker, K8s) capture logs via standard log drivers
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(configs.LOG_LEVEL)

    # JSON in production for log aggregators; text locally for readability
    if configs.LOG_FORMAT == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(TextFormatter())

    root_logger.addHandler(handler)

    # Suppress noisy third-party loggers to reduce log volume in production.
    # uvicorn.access: every HTTP request is already logged by middleware
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    # sqlalchemy.engine: only show queries in debug mode for troubleshooting
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if configs.DEBUG else logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger instance.

    Args:
        name: Logger name, typically ``__name__`` of the calling module.

    Returns:
        A configured :class:`logging.Logger` instance.
    """
    return logging.getLogger(name)
