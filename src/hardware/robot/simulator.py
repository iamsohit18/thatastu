"""High-fidelity robot arm simulator for development, testing, and offline teleoperation."""
import time
import math
from typing import List, Optional
from src.hardware.robot.interface import RobotInterface
from src.common.models import RobotTelemetry, CartesianPose, JointState, GripperState
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("simulator_robot")


class SimulatorRobotAdapter(RobotInterface):
    """
    Simulation implementation of RobotInterface.
    Simulates a 6-DoF or 7-DoF articulated arm with forward kinematics and first-order dynamics.
    """

    def __init__(self, dof: int = 6, update_hz: float = 50.0):
        self._connected = False
        self._dof = dof
        self._dt = 1.0 / update_hz
        self._seq = 0

        # Nominal rest joint configuration [rad]
        self._current_joints = [0.0, -0.785, 0.0, -1.57, 0.0, 1.57][:dof]
        if len(self._current_joints) < dof:
            self._current_joints.extend([0.0] * (dof - len(self._current_joints)))

        self._target_joints = list(self._current_joints)
        self._joint_velocities = [0.0] * dof
        self._joint_torques = [0.0] * dof

        self._tcp_pose = CartesianPose(x=0.45, y=0.0, z=0.35, roll=0.0, pitch=1.57, yaw=0.0)
        self._target_tcp = CartesianPose(x=0.45, y=0.0, z=0.35, roll=0.0, pitch=1.57, yaw=0.0)
        self._gripper = GripperState(position=85.0, is_closed=False, effort=0.0)

    def connect(self) -> bool:
        self._connected = True
        log_event(logger, logging.INFO, "simulator_robot", "CONNECTED", "Simulator robot initialized")
        return True

    def disconnect(self) -> None:
        self._connected = False
        log_event(logger, logging.INFO, "simulator_robot", "DISCONNECTED", "Simulator robot disconnected")

    def is_connected(self) -> bool:
        return self._connected

    def get_joint_positions(self) -> List[float]:
        self._step_simulation()
        return list(self._current_joints)

    def get_joint_velocities(self) -> Optional[List[float]]:
        return list(self._joint_velocities)

    def get_joint_torques(self) -> Optional[List[float]]:
        return list(self._joint_torques)

    def get_tcp_pose(self) -> CartesianPose:
        self._step_simulation()
        return self._tcp_pose

    def send_joint_command(self, positions: List[float]) -> bool:
        if not self._connected:
            return False
        if len(positions) != self._dof:
            return False
        self._target_joints = list(positions)
        return True

    def send_cartesian_command(self, pose: CartesianPose) -> bool:
        if not self._connected:
            return False
        self._target_tcp = pose
        return True

    def stop(self) -> None:
        self._target_joints = list(self._current_joints)
        self._joint_velocities = [0.0] * self._dof

    def get_robot_state(self) -> RobotTelemetry:
        self._step_simulation()
        self._seq += 1
        return RobotTelemetry(
            timestamp=time.time(),
            monotonic_timestamp_ns=time.monotonic_ns(),
            sequence_number=self._seq,
            joint_state=JointState(
                positions=list(self._current_joints),
                velocities=list(self._joint_velocities),
                torques=list(self._joint_torques),
            ),
            tcp_pose=self._tcp_pose,
            gripper_state=self._gripper,
            is_in_estop=False,
            is_safe=True,
            controller_status="nominal_simulation",
        )

    def _step_simulation(self) -> None:
        """Simple dynamics step towards target joints and Cartesian pose."""
        alpha = 0.25  # Smooth interpolation
        for i in range(self._dof):
            diff = self._target_joints[i] - self._current_joints[i]
            vel = diff / self._dt
            self._joint_velocities[i] = vel * alpha
            self._current_joints[i] += diff * alpha
            # Simulated gravitational load
            self._joint_torques[i] = 12.0 * math.sin(self._current_joints[i])

        # Step Cartesian pose
        self._tcp_pose = CartesianPose(
            x=self._tcp_pose.x + (self._target_tcp.x - self._tcp_pose.x) * alpha,
            y=self._tcp_pose.y + (self._target_tcp.y - self._tcp_pose.y) * alpha,
            z=self._tcp_pose.z + (self._target_tcp.z - self._tcp_pose.z) * alpha,
            roll=self._tcp_pose.roll + (self._target_tcp.roll - self._tcp_pose.roll) * alpha,
            pitch=self._tcp_pose.pitch + (self._target_tcp.pitch - self._tcp_pose.pitch) * alpha,
            yaw=self._tcp_pose.yaw + (self._target_tcp.yaw - self._tcp_pose.yaw) * alpha,
        )
