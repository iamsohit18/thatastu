"""Timestamp container and validation helpers."""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SyncTimestamp:
    """
    Immutable timestamp packet binding wall time, monotonic time, source ID, and sequence.
    """
    wall_time_s: float
    monotonic_ns: int
    sequence_id: int
    source_id: str


class TimestampAnomalyDetector:
    """
    Inspects incoming stream timestamps for:
    - Duplicates
    - Time reversals (clock going backwards)
    - Excessive gaps
    - Missing sequence numbers
    """

    def __init__(self, source_id: str, max_gap_seconds: float = 0.100):
        self.source_id = source_id
        self.max_gap_seconds = max_gap_seconds
        self.last_timestamp: Optional[SyncTimestamp] = None
        self.anomalies_detected = 0

    def check_sample(self, sample: SyncTimestamp) -> Tuple[bool, Optional[str]]:
        if self.last_timestamp is None:
            self.last_timestamp = sample
            return True, None

        # 1. Reversal check
        if sample.monotonic_ns < self.last_timestamp.monotonic_ns:
            self.anomalies_detected += 1
            return False, f"Timestamp reversal detected: {sample.monotonic_ns} < {self.last_timestamp.monotonic_ns}"

        # 2. Duplicate check
        if sample.monotonic_ns == self.last_timestamp.monotonic_ns:
            self.anomalies_detected += 1
            return False, f"Duplicate timestamp detected at {sample.monotonic_ns}ns"

        # 3. Gap check
        delta_s = (sample.monotonic_ns - self.last_timestamp.monotonic_ns) / 1e9
        if delta_s > self.max_gap_seconds:
            self.anomalies_detected += 1
            return False, f"Excessive timestamp gap of {delta_s*1000:.1f}ms (threshold: {self.max_gap_seconds*1000:.1f}ms)"

        # 4. Sequence discontinuity
        expected_seq = self.last_timestamp.sequence_id + 1
        if sample.sequence_id != expected_seq:
            self.anomalies_detected += 1
            return False, f"Sequence gap: expected {expected_seq}, received {sample.sequence_id}"

        self.last_timestamp = sample
        return True, None
