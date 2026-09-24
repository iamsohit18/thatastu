"""Episode lifecycle and directory manager."""
import os
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from src.recording.recorder import EpisodeRecorder
from src.recording.manifest import EpisodeManifest
from src.common.models import EpisodeMetadata
from src.common.exceptions import EpisodeRecordingError


class EpisodeManager:
    """Manages episode sessions, directory provisioning, and list enumeration."""

    def __init__(self, config: Dict[str, Any]):
        rec_cfg = config.get("recording", {})
        self.base_dir = rec_cfg.get("output_base_dir", "./data/episodes")
        self.active_recorder: Optional[EpisodeRecorder] = None

    def create_episode(
        self,
        task_id: str,
        operator_id: str,
        robot_id: str = "robot_01",
        leader_id: str = "leader_01",
        driver_mode: str = "simulation",
    ) -> EpisodeRecorder:
        if self.active_recorder is not None:
            raise EpisodeRecordingError("An episode recording session is already active.")

        ep_id = f"EP_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        ep_dir = os.path.join(self.base_dir, ep_id)
        os.makedirs(ep_dir, exist_ok=True)

        metadata = EpisodeMetadata(
            episode_id=ep_id,
            task_id=task_id,
            operator_id=operator_id,
            robot_id=robot_id,
            leader_id=leader_id,
            start_time=datetime.now(timezone.utc).isoformat(),
            driver_mode=driver_mode,
        )

        recorder = EpisodeRecorder(episode_dir=ep_dir, metadata=metadata)
        self.active_recorder = recorder
        return recorder

    def stop_current_episode(self, outcome: str = "success") -> EpisodeMetadata:
        if self.active_recorder is None:
            raise EpisodeRecordingError("No active episode is currently recording.")

        meta = self.active_recorder.stop(outcome=outcome)
        self.active_recorder = None
        return meta

    def list_episodes(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.base_dir):
            return []

        episodes = []
        for name in sorted(os.listdir(self.base_dir), reverse=True):
            ep_dir = os.path.join(self.base_dir, name)
            manifest_file = os.path.join(ep_dir, "manifest.json")
            if os.path.isdir(ep_dir) and os.path.exists(manifest_file):
                try:
                    manifest = EpisodeManifest.load(manifest_file)
                    episodes.append(manifest.metadata.model_dump())
                except Exception:
                    pass
        return episodes
