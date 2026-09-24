"""Explicit Teleoperation Control Loop Orchestrator."""
import time
from typing import Dict, Any, Optional
from src.hardware.robot.interface import RobotInterface
from src.hardware.leader.interface import LeaderInterface
from src.teleoperation.mapper import TeleopMapper
from src.safety.safety_manager import SafetyManager
from src.common.models import LeaderState, RobotTelemetry, TeleopAction, CartesianPose
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("teleop_controller")


class TeleopController:
    """
    Central loop coordinator executing:
    Leader -> Normalized Command -> Coordinate Transform -> Scaling -> Safety Check -> Follower Execution
    """

    def __init__(
        self,
        robot: RobotInterface,
        leader: LeaderInterface,
        safety: SafetyManager,
        config: Dict[str, Any],
    ):
        self.robot = robot
        self.leader = leader
        self.safety = safety
        self.config = config
        self.mapper = TeleopMapper(config)

        self._active = False
        self._seq = 0
        self._last_cycle_time = time.time()

    @property
    def is_active(self) -> bool:
        return self._active

    def engage(self) -> bool:
        """Start teleoperation after checking preconditions."""
        if not self.robot.is_connected() or not self.leader.is_connected():
            log_event(logger, logging.ERROR, "teleop_controller", "ENGAGE_FAILED", "Robot or Leader arm not connected")
            return False

        if not self.safety.is_safe():
            log_event(logger, logging.ERROR, "teleop_controller", "ENGAGE_FAILED", "Safety system in E-Stop or not cleared")
            return False

        current_telemetry = self.robot.get_robot_state()
        leader_state = self.leader.read_state()

        if leader_state.cartesian_pose:
            self.mapper.reset_origin(leader_state.cartesian_pose, current_telemetry.tcp_pose)

        self._active = True
        self._last_cycle_time = time.time()
        log_event(logger, logging.INFO, "teleop_controller", "ENGAGED", "Teleoperation loop engaged successfully")
        return True

    def disengage(self) -> None:
        """Safely disengage teleoperation and stop follower motion."""
        self._active = False
        self.robot.stop()
        log_event(logger, logging.INFO, "teleop_controller", "DISENGAGED", "Teleoperation loop disengaged; follower stopped")

    def step(self) -> Optional[TeleopAction]:
        """
        Executes a single synchronized control tick.
        Returns the commanded safe TeleopAction, or None if inactive/aborted.
        """
        if not self._active:
            return None

        now = time.time()
        dt = max(1e-4, now - self._last_cycle_time)
        self._last_cycle_time = now
        self._seq += 1

        # 1. Read leader input
        leader_state = self.leader.read_state()

        # Update deadman switch status from master input
        self.safety.set_deadman_state(leader_state.deadman_pressed)

        # 2. Read follower current state
        follower_telemetry = self.robot.get_robot_state()

        # 3. Mapping: leader state -> candidate pose
        candidate_pose = self.mapper.map_leader_state(leader_state, follower_telemetry.tcp_pose)

        # 4. Safety validation (workspace limits, velocity clamp, E-Stop assertion)
        safe_target_pose = self.safety.validate_action(
            current_telemetry=follower_telemetry,
            candidate_pose=candidate_pose,
            dt_seconds=dt,
        )

        # 5. Send command to follower
        self.robot.send_cartesian_command(safe_target_pose)

        # 6. Construct action snapshot for recorder
        action = TeleopAction(
            timestamp=now,
            sequence_number=self._seq,
            target_tcp_pose=safe_target_pose,
            target_gripper_position=leader_state.gripper_trigger * 85.0,
            command_mode="cartesian_pose",
        )

        return action
