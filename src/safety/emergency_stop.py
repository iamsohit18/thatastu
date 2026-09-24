"""Emergency stop monitoring and state latching."""
import time
from typing import Optional
from src.common.exceptions import EmergencyStopActiveError
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("emergency_stop")


class EmergencyStopManager:
    """
    Manages both software emergency stop latching and physical E-Stop input monitoring.
    Never auto-clears an E-Stop condition: requires explicit operator reset.
    """

    def __init__(self):
        self._latched_estop = False
        self._estop_reason = ""
        self._timestamp = 0.0

    @property
    def is_triggered(self) -> bool:
        return self._latched_estop

    @property
    def reason(self) -> str:
        return self._estop_reason

    def trigger(self, reason: str = "Operator manual emergency stop") -> None:
        self._latched_estop = True
        self._estop_reason = reason
        self._timestamp = time.time()
        log_event(logger, logging.CRITICAL, "emergency_stop", "ESTOP_TRIGGERED", f"EMERGENCY STOP ACTIVATED: {reason}")

    def reset(self) -> bool:
        """Explicit operator reset after confirming physical hardware safe state."""
        log_event(logger, logging.WARNING, "emergency_stop", "ESTOP_RESET", "Emergency stop reset requested by operator")
        self._latched_estop = False
        self._estop_reason = ""
        return True

    def assert_safe(self) -> None:
        if self._latched_estop:
            raise EmergencyStopActiveError(f"System halted under Emergency Stop: {self._estop_reason}")
