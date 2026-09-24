"""Performance metrics counter (teleoperation loop frequency, dropped frames, latencies)."""
import time
from typing import Dict, Any


class MetricsCollector:
    def __init__(self):
        self.loop_count = 0
        self.last_time = time.time()
        self.hz = 0.0

    def tick(self) -> None:
        self.loop_count += 1
        now = time.time()
        elapsed = now - self.last_time
        if elapsed >= 1.0:
            self.hz = self.loop_count / elapsed
            self.loop_count = 0
            self.last_time = now

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "current_frequency_hz": round(self.hz, 1),
        }
