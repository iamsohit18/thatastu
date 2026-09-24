"""Episode stream recorder coordinating video, telemetry, and action writers."""
import os
import time
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from src.recording.writers.telemetry_writer import TelemetryWriter
from src.recording.writers.action_writer import ActionWriter
from src.recording.writers.video_writer import VideoWriter
from src.recording.manifest import EpisodeManifest
from src.common.models import EpisodeMetadata, RobotTelemetry, LeaderState, TeleopAction
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("recorder")


class EpisodeRecorder:
    """Synchronous writer coordinator for an active demonstration episode."""

    def __init__(self, episode_dir: str, metadata: EpisodeMetadata):
        self.episode_dir = episode_dir
        self.metadata = metadata

        self.telemetry_path = os.path.join(episode_dir, "robot", "telemetry.parquet")
        self.action_path = os.path.join(episode_dir, "actions", "actions.parquet")
        self.telemetry_writer = TelemetryWriter(self.telemetry_path)
        self.action_writer = ActionWriter(self.action_path)

        self.video_writers: Dict[str, VideoWriter] = {}
        self._is_recording = False
        self._frame_count = 0
        self._start_mono_ns = 0

    def start(self, camera_meta: Dict[str, Any]) -> None:
        self._is_recording = True
        self._start_mono_ns = time.monotonic_ns()
        self.metadata.start_time = datetime.now(timezone.utc).isoformat()

        # Initialize video writers for each camera
        for cam_id, meta in camera_meta.items():
            res = meta.get("resolution", (640, 480))
            fps = meta.get("fps", 30)
            vid_path = os.path.join(self.episode_dir, "cameras", f"{cam_id}.mp4")
            writer = VideoWriter(vid_path, resolution=res, fps=fps)
            writer.open()
            self.video_writers[cam_id] = writer

        log_event(logger, logging.INFO, "recorder", "RECORDING_STARTED", f"Recording episode {self.metadata.episode_id}")

    def record_step(
        self,
        telemetry: RobotTelemetry,
        action: Optional[TeleopAction],
        camera_frames: Dict[str, Any],
    ) -> None:
        if not self._is_recording:
            return

        self.telemetry_writer.write_sample(telemetry)
        if action:
            self.action_writer.write_action(action)

        for cam_id, cam_info in camera_frames.items():
            frame = cam_info.get("frame")
            if frame is not None and cam_id in self.video_writers:
                self.video_writers[cam_id].write_frame(frame)

        self._frame_count += 1

    def stop(self, outcome: str = "success") -> EpisodeMetadata:
        self._is_recording = False
        duration_s = (time.monotonic_ns() - self._start_mono_ns) / 1e9

        self.telemetry_writer.close()
        self.action_writer.close()
        for writer in self.video_writers.values():
            writer.close()

        self.metadata.end_time = datetime.now(timezone.utc).isoformat()
        self.metadata.duration_seconds = duration_s
        self.metadata.total_frames = self._frame_count
        self.metadata.outcome = outcome

        # Write manifest.json
        manifest = EpisodeManifest(self.episode_dir, self.metadata)
        manifest.save()

        log_event(
            logger,
            logging.INFO,
            "recorder",
            "RECORDING_STOPPED",
            f"Completed episode {self.metadata.episode_id} ({duration_s:.1f}s, {self._frame_count} frames)",
            episode_id=self.metadata.episode_id,
        )

        return self.metadata
