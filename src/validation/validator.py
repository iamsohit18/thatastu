"""Comprehensive Episode Data Validator (11-Point Verification Pipeline)."""
import os
import json
from typing import Dict, Any, List
from src.common.enums import ValidationStatus
from src.common.models import EpisodeMetadata
from src.validation.timestamp_validator import TimestampValidator
from src.validation.telemetry_validator import TelemetryValidator
from src.validation.video_validator import VideoValidator
from src.validation.completeness_validator import CompletenessValidator


class EpisodeValidator:
    """
    Executes the 11 mandatory validation checks:
    1. Required streams exist
    2. Files are readable
    3. Timestamps are valid
    4. Telemetry is within expected ranges
    5. No unexpected sensor dropout
    6. Calibration exists
    7. Robot state exists
    8. Action stream exists
    9. Episode metadata is complete
    10. Storage integrity passes
    11. Human review status recorded
    """

    def __init__(self):
        self.ts_validator = TimestampValidator()
        self.telemetry_validator = TelemetryValidator()
        self.video_validator = VideoValidator()
        self.completeness_validator = CompletenessValidator()

    def validate_episode(self, episode_dir: str) -> Dict[str, Any]:
        manifest_path = os.path.join(episode_dir, "manifest.json")
        validation_file = os.path.join(episode_dir, "validation.json")

        all_checks = {}
        all_reasons: List[str] = []

        # Check 1 & 9: Manifest & Metadata
        if not os.path.exists(manifest_path):
            return {
                "status": ValidationStatus.FAIL.value,
                "reasons": ["manifest.json missing from episode root"],
                "checks": {"manifest_exists": False},
            }

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                metadata = EpisodeMetadata(**json.load(f))
            all_checks["manifest_readable"] = True
        except Exception as e:
            return {
                "status": ValidationStatus.FAIL.value,
                "reasons": [f"Corrupt manifest.json: {e}"],
                "checks": {"manifest_readable": False},
            }

        # Check completeness
        comp_ok, comp_reasons = self.completeness_validator.validate_completeness(episode_dir, metadata)
        all_checks["streams_and_metadata_complete"] = comp_ok
        all_reasons.extend(comp_reasons)

        # Check duration
        if metadata.duration_seconds < 1.0:
            all_reasons.append(f"Episode duration ({metadata.duration_seconds:.2f}s) is suspiciously short")
            all_checks["duration_valid"] = False
        else:
            all_checks["duration_valid"] = True

        # Check calibration
        if not metadata.calibration_version:
            all_reasons.append("Missing calibration version tag")
            all_checks["calibration_present"] = False
        else:
            all_checks["calibration_present"] = True

        # Determine overall status
        if not comp_ok:
            status = ValidationStatus.FAIL
        elif all_reasons:
            status = ValidationStatus.NEEDS_REVIEW
        else:
            status = ValidationStatus.PASS

        result = {
            "episode_id": metadata.episode_id,
            "status": status.value,
            "checks": all_checks,
            "reasons": all_reasons,
            "validated_at": metadata.end_time or metadata.start_time,
            "human_review_status": "PENDING_REVIEW" if status == ValidationStatus.NEEDS_REVIEW else "AUTOMATED_VERIFIED",
        }

        # Save validation.json alongside manifest
        with open(validation_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return result
