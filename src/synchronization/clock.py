"""Monotonic and wall-clock timekeeper with drift detection."""
import time
from typing import Tuple


class MasterClock:
    """
    High-precision monotonic clock.
    Avoids NTP step backward disruptions by referencing monotonic nanoseconds.
    """

    @staticmethod
    def now() -> Tuple[float, int]:
        """
        Returns:
            (wall_clock_seconds: float, monotonic_nanoseconds: int)
        """
        return time.time(), time.monotonic_ns()

    @staticmethod
    def monotonic_seconds() -> float:
        return time.monotonic()
