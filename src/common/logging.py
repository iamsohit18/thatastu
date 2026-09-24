"""Structured logger for teleoperation platform events."""
import logging
import json
import sys
from datetime import datetime, timezone
from typing import Optional, Dict, Any


class StructuredJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "component": getattr(record, "component", record.name),
            "event": getattr(record, "event", "LOG"),
            "device": getattr(record, "device", None),
            "episode_id": getattr(record, "episode_id", None),
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_entry.update(record.extra_data)
        return json.dumps({k: v for k, v in log_entry.items() if v is not None})


def get_logger(name: str = "roboteleop") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredJsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log_event(
    logger: logging.Logger,
    level: int,
    component: str,
    event: str,
    message: str,
    device: Optional[str] = None,
    episode_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
):
    """Utility to emit structured teleop telemetry log messages."""
    record_extra = {
        "component": component,
        "event": event,
        "device": device,
        "episode_id": episode_id,
        "extra_data": extra or {},
    }
    logger.log(level, message, extra=record_extra)
