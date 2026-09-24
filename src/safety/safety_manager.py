"""Composite Safety Manager combining workspace, velocity, watchdog, and E-Stop checks."""
import time
from typing import Dict, Any, Optional
from src.safety.workspace_limits import WorkspaceLimits
from src.safety.velocity_limits import VelocityLimits
from src.safety.emergency_stop import EmergencyStopManager
from src.common.models import CartesianPose, TeleopAction, RobotTelemetry
from src.common.exceptions import SafetyViolationError, EmergencyStopActiveError
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("safety_manager")


class SafetyManager:
    """
    Central safety arbiter. Every command passing from leader to follower
    MUST be validated here before transmission to low-level hardware.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.workspace = WorkspaceLimits(config)
        self.velocity = VelocityLimits(config)
        self.estop = EmergencyStopManager()

        safety_cfg = config.get("safety", {})
        watchdog_cfg = safety_cfg.get("watchdog", {})
        self.command_timeout_s = watchdog_cfg.get("command_timeout_ms", 150) / 1000.0

        self._last_command_time = time.time()
        self._deadman_pressed = True

    def set_deadman_state(self, pressed: bool) -> None:
        self._deadman_pressed = pressed

    def is_safe(self) -> bool:
        return not self.estop.is_triggered and self._deadman_pressed

    def validate_action(
        self,
        current_telemetry: RobotTelemetry,
        candidate_pose: CartesianPose,
        dt_seconds: float = 0.02,
    ) -> CartesianPose:
        """
        Validates target pose against all active safety rules:
        1. E-Stop state
        2. Deadman switch engagement
        3. Watchdog timeout
        4. Workspace boundaries
        5. Velocity limits
        """
        # 1. E-Stop check
        self.estop.assert_safe()

        # 2. Deadman switch
        if not self._deadman_pressed:
            log_event(logger, logging.DEBUG, "safety_manager", "DEADMAN_RELEASED", "Deadman switch not held; holding current position")
            return current_telemetry.tcp_pose

        # 3. Watchdog check
        now = time.time()
        if (now - self._last_command_time) > self.command_timeout_s:
            log_event(logger, logging.WARNING, "safety_manager", "WATCHDOG_WARN", "Command heartbeat interval exceeded")
        self._last_command_time = now

        # 4. Workspace boundary clamp
        safe_bounded_pose = self.workspace.clamp_pose(candidate_pose)

        # 5. Velocity rate clamp
        safe_rate_pose = self.velocity.clamp_velocity(
            current_pose=current_telemetry.tcp_pose,
            target_pose=safe_bounded_pose,
            dt_seconds=dt_seconds,
        )

        return safe_rate_pose
