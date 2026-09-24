"""Multi-camera system orchestrator with software timestamp alignment."""
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from src.hardware.cameras.interface import CameraInterface
from src.hardware.cameras.opencv_camera import OpenCVCamera
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("camera_manager")


class CameraManager:
    """Coordinates multiple synchronized cameras (e.g. wrist, overhead, side)."""

    def __init__(self, config: Dict[str, Any]):
        self._cameras: Dict[str, CameraInterface] = {}
        self._config = config
        self._initialize_from_config()

    def _initialize_from_config(self) -> None:
        cam_cfg = self._config.get("cameras", {})
        devices = cam_cfg.get("devices", [])

        for dev in devices:
            cam_id = dev.get("id")
            res = tuple(dev.get("resolution", [640, 480]))
            fps = dev.get("fps", 30)
            dev_idx = dev.get("device_index", 0)

            cam = OpenCVCamera(
                camera_id=cam_id,
                device_index=dev_idx,
                resolution=res,
                fps=fps,
            )
            self._cameras[cam_id] = cam

    def connect_all(self) -> bool:
        all_ok = True
        for cam_id, cam in self._cameras.items():
            if not cam.connect():
                all_ok = False
        return all_ok

    def start_all(self) -> bool:
        all_ok = True
        for cam_id, cam in self._cameras.items():
            if not cam.start():
                all_ok = False
        return all_ok

    def stop_all(self) -> None:
        for cam in self._cameras.values():
            cam.stop()

    def capture_synchronized_frames(self) -> Dict[str, Dict[str, Any]]:
        """
        Capture frames from all cameras near simultaneously.
        Computes inter-frame timestamp deltas to monitor sync health.
        """
        results = {}
        timestamps = []

        for cam_id, cam in self._cameras.items():
            success, frame, ts = cam.read_frame()
            if success and frame is not None:
                results[cam_id] = {
                    "frame": frame,
                    "timestamp": ts,
                    "resolution": cam.resolution,
                }
                timestamps.append(ts)

        max_delta_ms = (max(timestamps) - min(timestamps)) * 1000.0 if len(timestamps) > 1 else 0.0

        return {
            "frames": results,
            "max_timestamp_delta_ms": max_delta_ms,
            "num_cameras_captured": len(results),
        }

    def get_camera_ids(self) -> List[str]:
        return list(self._cameras.keys())

    def get_camera(self, cam_id: str) -> Optional[CameraInterface]:
        return self._cameras.get(cam_id)
