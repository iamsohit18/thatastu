"""Timestamp continuity and monotonic sanity validator."""
from typing import List, Tuple, Dict, Any


class TimestampValidator:
    """Validates timestamp monotonic ordering, absence of reversals, and gap limits."""

    def __init__(self, max_gap_ms: float = 80.0):
        self.max_gap_ms = max_gap_ms

    def validate_timestamps(self, timestamps: List[float]) -> Tuple[bool, List[str]]:
        reasons = []
        if not timestamps:
            return False, ["Timestamp list is empty"]

        if len(timestamps) < 10:
            reasons.append("Episode has fewer than 10 recorded samples (too short)")

        # Reversal check
        reversals = 0
        gaps = 0
        for i in range(1, len(timestamps)):
            dt = timestamps[i] - timestamps[i - 1]
            if dt < 0:
                reversals += 1
            elif dt * 1000.0 > self.max_gap_ms:
                gaps += 1

        if reversals > 0:
            reasons.append(f"Detected {reversals} timestamp reversals (clock went backward)")

        if gaps > 0:
            reasons.append(f"Detected {gaps} excessive timestamp gaps exceeding {self.max_gap_ms}ms")

        is_valid = (reversals == 0) and (gaps <= 2)
        return is_valid, reasons
