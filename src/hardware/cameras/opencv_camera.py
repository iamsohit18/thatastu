"""OpenCV / USB camera implementation with fallback synthetic frame generation for testing."""
import time
from typing import Tuple, Optional
import numpy as np
from src.hardware.cameras.interface import CameraInterface
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("opencv_camera")

# Optional cv2 import
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    cv2 = None
    HAS_CV2 = False


class OpenCVCamera(CameraInterface):
    """
    Standard OpenCV video capture driver.
    Supports USB UVC cameras, V4L2 devices, or generates a synthetic test pattern
    if device index cannot be opened.
    """

    def __init__(
        self,
        camera_id: str,
        device_index: int = 0,
        resolution: Tuple[int, int] = (640, 480),
        fps: int = 30,
        synthetic_fallback: bool = True,
    ):
        self._camera_id = camera_id
        self._device_index = device_index
        self._resolution = resolution
        self._fps = fps
        self._synthetic = synthetic_fallback
        self._cap = None
        self._connected = False
        self._streaming = False
        self._last_timestamp = 0.0
        self._frame_count = 0

    @property
    def camera_id(self) -> str:
        return self._camera_id

    @property
    def resolution(self) -> Tuple[int, int]:
        return self._resolution

    @property
    def fps(self) -> int:
        return self._fps

    @property
    def is_connected(self) -> bool:
        return self._connected

    def connect(self) -> bool:
        if HAS_CV2 and not self._synthetic:
            try:
                self._cap = cv2.VideoCapture(self._device_index)
                if self._cap.isOpened():
                    self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._resolution[0])
                    self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._resolution[1])
                    self._cap.set(cv2.CAP_PROP_FPS, self._fps)
                    self._connected = True
                    log_event(logger, logging.INFO, "opencv_camera", "CONNECTED", f"Opened hardware camera {self._camera_id} at /dev/video{self._device_index}")
                    return True
            except Exception as e:
                log_event(logger, logging.WARNING, "opencv_camera", "HARDWARE_FAILED", f"Could not open physical camera: {e}")

        # Fallback to simulation/synthetic mode
        self._synthetic = True
        self._connected = True
        log_event(logger, logging.INFO, "opencv_camera", "SYNTHETIC_MODE", f"Using synthetic test camera for {self._camera_id}")
        return True

    def start(self) -> bool:
        if not self._connected:
            return False
        self._streaming = True
        return True

    def stop(self) -> None:
        self._streaming = False
        if self._cap is not None and HAS_CV2:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None
        self._connected = False

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray], float]:
        if not self._connected or not self._streaming:
            return False, None, 0.0

        ts = time.time()
        self._last_timestamp = ts
        self._frame_count += 1

        if not self._synthetic and self._cap is not None and HAS_CV2:
            ret, frame = self._cap.read()
            if ret:
                return True, frame, ts

        # Generate synthetic robotics test pattern
        w, h = self._resolution
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        # Background gradient
        frame[:, :, 0] = np.linspace(20, 50, h)[:, None]
        frame[:, :, 1] = np.linspace(30, 60, w)[None, :]
        frame[:, :, 2] = 40

        # Draw reticle / workspace visual
        cx, cy = w // 2, h // 2
        frame[cy - 10 : cy + 10, cx - 1 : cx + 2] = [0, 255, 128]
        frame[cy - 1 : cy + 2, cx - 10 : cx + 10] = [0, 255, 128]

        return True, frame, ts

    def get_timestamp(self) -> float:
        return self._last_timestamp
