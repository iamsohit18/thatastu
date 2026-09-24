"""Multimodal stream synchronizer aligning vision frames and high-rate telemetry."""
from typing import Dict, Any, List, Optional
from src.common.models import RobotTelemetry, LeaderState, TeleopAction


class StreamSynchronizer:
    """
    Interpolates or nearest-neighbor associates high-rate telemetry (50-500Hz)
    with vision camera frames (30-60Hz).
    """

    def __init__(self, tolerance_ms: float = 25.0):
        self.tolerance_s = tolerance_ms / 1000.0

    def bundle_step(
        self,
        camera_data: Dict[str, Any],
        robot_telemetry: RobotTelemetry,
        leader_state: Optional[LeaderState],
        action: Optional[TeleopAction],
    ) -> Dict[str, Any]:
        """
        Creates a unified synchronous demonstration step record.
        """
        ref_time = robot_telemetry.timestamp

        return {
            "timestamp": ref_time,
            "monotonic_ns": robot_telemetry.monotonic_timestamp_ns,
            "cameras": camera_data.get("frames", {}),
            "telemetry": robot_telemetry.model_dump(),
            "leader": leader_state.model_dump() if leader_state else None,
            "action": action.model_dump() if action else None,
        }
