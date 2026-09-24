"""Abstract interface definition for master/leader teleoperation input devices."""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.common.models import CartesianPose, LeaderState


class LeaderInterface(ABC):
    """
    Abstract Leader/Master Interface.
    Reads operator motion, joint angles, and gripper triggers.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Connect to master arm or input controller."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect and release device resources."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Return True if device is actively transmitting packets."""
        pass

    @abstractmethod
    def read_pose(self) -> Optional[CartesianPose]:
        """Read 6-DoF Cartesian pose of operator's hand/handle."""
        pass

    @abstractmethod
    def read_joints(self) -> Optional[List[float]]:
        """Read master joint angles in radians."""
        pass

    @abstractmethod
    def read_gripper(self) -> float:
        """Read gripper input (normalized 0.0=open, 1.0=fully closed)."""
        pass

    @abstractmethod
    def get_timestamp(self) -> float:
        """Return timestamp of the latest sample."""
        pass

    @abstractmethod
    def read_state(self) -> LeaderState:
        """Return complete snapshot of leader state."""
        pass
