"""Manifest and stream completeness validator."""
import os
from typing import List, Tuple, Dict, Any
from src.common.models import EpisodeMetadata


class CompletenessValidator:
    """Verifies that all required streams and metadata components exist."""

    REQUIRED_METADATA_FIELDS = [
        "episode_id", "task_id", "operator_id", "robot_id", "start_time", "calibration_version"
    ]

    def validate_completeness(self, episode_dir: str, metadata: EpisodeMetadata) -> Tuple[bool, List[str]]:
        reasons = []

        # Check metadata fields
        meta_dict = metadata.model_dump()
        for field in self.REQUIRED_METADATA_FIELDS:
            if not meta_dict.get(field):
                reasons.append(f"Missing required metadata field: {field}")

        # Check required stream paths
        telemetry_parquet = os.path.join(episode_dir, "robot", "telemetry.parquet")
        telemetry_jsonl = os.path.join(episode_dir, "robot", "telemetry.jsonl")
        if not (os.path.exists(telemetry_parquet) or os.path.exists(telemetry_jsonl)):
            reasons.append("Robot telemetry stream file missing")

        action_parquet = os.path.join(episode_dir, "actions", "actions.parquet")
        action_jsonl = os.path.join(episode_dir, "actions", "actions.jsonl")
        if not (os.path.exists(action_parquet) or os.path.exists(action_jsonl)):
            reasons.append("Action stream file missing")

        return len(reasons) == 0, reasons
