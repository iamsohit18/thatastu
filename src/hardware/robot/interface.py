"""Abstract interface definition for robot follower arms."""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.common.models import RobotTelemetry, CartesianPose, JointState


class RobotInterface(ABC):
    """
    Abstract Robot Interface.
    Decouples higher-level teleoperation, safety, and recording logic from vendor-specific drivers.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection with the robot controller. Returns True if successful."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Safely terminate communication and release controller resources."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if active, healthy communication exists."""
        pass

    @abstractmethod
    def get_joint_positions(self) -> List[float]:
        """Return current joint angles in radians."""
        pass

    @abstractmethod
    def get_joint_velocities(self) -> Optional[List[float]]:
        """Return current joint velocities in rad/s, or None if unsupported."""
        pass

    @abstractmethod
    def get_joint_torques(self) -> Optional[List[float]]:
        """Return measured joint torques/effort in Nm, or None if unsupported."""
        pass

    @abstractmethod
    def get_tcp_pose(self) -> CartesianPose:
        """Return current Tool Center Point pose in base coordinates."""
        pass

    @abstractmethod
    def send_joint_command(self, positions: List[float]) -> bool:
        """Send target joint positions to low-level controller."""
        pass

    @abstractmethod
    def send_cartesian_command(self, pose: CartesianPose) -> bool:
        """Send target Cartesian pose to low-level controller."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Command an immediate, controlled deceleration stop."""
        pass

    @abstractmethod
    def get_robot_state(self) -> RobotTelemetry:
        """Return full telemetry snapshot."""
        pass
