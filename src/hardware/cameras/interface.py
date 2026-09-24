"""Abstract interface definition for vision cameras."""
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Any
import numpy as np


class CameraInterface(ABC):
    """
    Abstract Vision Sensor Interface.
    Exposes frame capture, camera metadata, and hardware/software timestamps.
    """

    @property
    @abstractmethod
    def camera_id(self) -> str:
        """Unique string identifier (e.g. 'cam_wrist')."""
        pass

    @property
    @abstractmethod
    def resolution(self) -> Tuple[int, int]:
        """(width, height) in pixels."""
        pass

    @property
    @abstractmethod
    def fps(self) -> int:
        """Target acquisition framerate."""
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Status of camera link."""
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Initialize connection to device driver/bus."""
        pass

    @abstractmethod
    def start(self) -> bool:
        """Start streaming frame buffer."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop streaming and release image buffers."""
        pass

    @abstractmethod
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray], float]:
        """
        Capture latest frame.
        Returns:
            (success: bool, frame: Optional[np.ndarray], timestamp: float)
        """
        pass

    @abstractmethod
    def get_timestamp(self) -> float:
        """Return latest captured frame timestamp."""
        pass
