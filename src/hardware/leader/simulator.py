"""Simulated leader/master teleoperation input device."""
import time
import math
from typing import List, Optional
from src.hardware.leader.interface import LeaderInterface
from src.common.models import CartesianPose, LeaderState
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("simulator_leader")


class SimulatorLeaderAdapter(LeaderInterface):
    """
    Simulated leader arm. Can generate smooth test demonstration trajectories
    or accept virtual input from keyboard/dashboard.
    """

    def __init__(self, dof: int = 6):
        self._connected = False
        self._dof = dof
        self._seq = 0
        self._start_time = time.time()
        self._gripper_val = 0.0
        self._deadman = True
        self._clutch = False
        self._pose = CartesianPose(x=0.45, y=0.0, z=0.35, roll=0.0, pitch=1.57, yaw=0.0)

    def connect(self) -> bool:
        self._connected = True
        self._start_time = time.time()
        log_event(logger, logging.INFO, "simulator_leader", "CONNECTED", "Simulator leader arm initialized")
        return True

    def disconnect(self) -> None:
        self._connected = False
        log_event(logger, logging.INFO, "simulator_leader", "DISCONNECTED", "Simulator leader arm disconnected")

    def is_connected(self) -> bool:
        return self._connected

    def read_pose(self) -> Optional[CartesianPose]:
        self._update_sim_motion()
        return self._pose

    def read_joints(self) -> Optional[List[float]]:
        t = time.time() - self._start_time
        return [
            0.1 * math.sin(t * 0.5),
            -0.785 + 0.05 * math.cos(t * 0.5),
            0.0,
            -1.57 + 0.05 * math.sin(t * 0.5),
            0.0,
            1.57 + 0.1 * math.cos(t * 0.5),
        ][:self._dof]

    def read_gripper(self) -> float:
        return self._gripper_val

    def get_timestamp(self) -> float:
        return time.time()

    def set_virtual_pose(self, pose: CartesianPose) -> None:
        """Allow manual override from operator UI/dashboard."""
        self._pose = pose

    def set_virtual_gripper(self, val: float) -> None:
        self._gripper_val = max(0.0, min(1.0, val))

    def set_deadman(self, state: bool) -> None:
        self._deadman = state

    def read_state(self) -> LeaderState:
        self._update_sim_motion()
        self._seq += 1
        return LeaderState(
            timestamp=time.time(),
            monotonic_timestamp_ns=time.monotonic_ns(),
            sequence_number=self._seq,
            joint_positions=self.read_joints(),
            cartesian_pose=self._pose,
            gripper_trigger=self._gripper_val,
            deadman_pressed=self._deadman,
            clutch_pressed=self._clutch,
        )

    def _update_sim_motion(self) -> None:
        """Generate subtle sinusoidal movement if not overridden."""
        t = time.time() - self._start_time
        # Circular pick-and-place demonstration arc
        self._pose.x = 0.45 + 0.08 * math.cos(t * 0.4)
        self._pose.y = 0.00 + 0.08 * math.sin(t * 0.4)
        self._pose.z = 0.35 + 0.04 * math.sin(t * 0.8)
        self._gripper_val = 0.5 + 0.5 * math.sin(t * 0.3)
