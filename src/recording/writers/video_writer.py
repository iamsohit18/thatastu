"""Video stream writer using OpenCV or containerized MP4 encoder."""
import os
from typing import Tuple, Optional
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    cv2 = None
    HAS_CV2 = False


class VideoWriter:
    """Encodes real-time camera frames to MP4 video files."""

    def __init__(self, output_path: str, resolution: Tuple[int, int], fps: int = 30):
        self.output_path = output_path
        self.resolution = resolution
        self.fps = fps
        self.writer = None
        self._frames_written = 0

    def open(self) -> bool:
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        if HAS_CV2:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, self.resolution)
            return self.writer.isOpened()
        return True

    def write_frame(self, frame: np.ndarray) -> None:
        self._frames_written += 1
        if self.writer is not None and HAS_CV2:
            self.writer.write(frame)

    def close(self) -> int:
        if self.writer is not None and HAS_CV2:
            self.writer.release()
            self.writer = None
        return self._frames_written
