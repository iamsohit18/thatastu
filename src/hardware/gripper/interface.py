"""Abstract interface definition for end-effector grippers."""
from abc import ABC, abstractmethod
from typing import Optional
from src.common.models import GripperState


class GripperInterface(ABC):
    """
    Abstract Gripper Interface.
    Controls electric or pneumatic end-effector grippers.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Establish communication with gripper controller."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Release gripper connection."""
        pass

    @abstractmethod
    def open(self) -> bool:
        """Fully open gripper jaws."""
        pass

    @abstractmethod
    def close(self) -> bool:
        """Close gripper jaws until contact or limit reached."""
        pass

    @abstractmethod
    def set_position(self, position_mm: float, effort_n: Optional[float] = None) -> bool:
        """Command specific jaw opening aperture (mm)."""
        pass

    @abstractmethod
    def get_state(self) -> GripperState:
        """Return current position, effort, and moving status."""
        pass
