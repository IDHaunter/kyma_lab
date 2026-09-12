import json
import logging
import os
import sys
from datetime import datetime, timezone


DEFAULT_LOG_LEVEL = "INFO"


class JsonFormatter(logging.Formatter):
    """Format log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


def get_log_level() -> int:
    """Read the log level from the LOG_LEVEL environment variable."""

    level_name = os.getenv(
        "LOG_LEVEL",
        DEFAULT_LOG_LEVEL,
    ).strip().upper()

    level = getattr(logging, level_name, None)

    if not isinstance(level, int):
        return logging.INFO

    return level


def get_log_level_name(level: int) -> str:
    """Convert a logging level number to its textual name."""

    return logging.getLevelName(level)


def configure_logging() -> str:
    """
    Configure application-wide logging.

    Returns:
        str: The effective log level name, e.g. "INFO", "DEBUG".
    """

    level = get_log_level()
    level_name = get_log_level_name(level)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove handlers configured by other libraries/frameworks.
    root_logger.handlers.clear()

    # Kubernetes expects applications to write logs to stdout/stderr.
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(JsonFormatter())

    root_logger.addHandler(handler)

    return level_name


def get_logger(name: str) -> logging.Logger:
    """Return a logger using the global logging configuration."""

    return logging.getLogger(name)