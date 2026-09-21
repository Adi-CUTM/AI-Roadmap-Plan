"""
Internal logging setup for LogSentry itself (not the logs it parses).
Supports console + rotating file output, structured JSON option for
shipping LogSentry's own operational logs to a SIEM too.
"""

import logging
import logging.handlers
import sys
import json
from pathlib import Path
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Emit log records as single-line JSON for machine ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def setup_logger(
    name: str = "logsentry",
    log_dir: str = "logs",
    level: str = "INFO",
    json_format: bool = False,
    max_bytes: int = 10 * 1024 * 1024,   # 10 MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Configure and return the root LogSentry logger.
    Call this ONCE at startup (cli.py). Every module then does:
        logger = logging.getLogger("logsentry.<module>")
    and inherits this config.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured (e.g. re-imported) — don't duplicate handlers
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = (
        JsonFormatter()
        if json_format
        else logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=Path(log_dir) / "logsentry.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger


def get_logger(module_name: str) -> logging.Logger:
    """Convenience getter for use inside any module."""
    return logging.getLogger(f"logsentry.{module_name}")