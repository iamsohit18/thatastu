"""Episode manifest generator and metadata serialization."""
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from src.common.models import EpisodeMetadata


class EpisodeManifest:
    """Manages the lifecycle and serialization of manifest.json for an episode."""

    def __init__(self, output_dir: str, metadata: EpisodeMetadata):
        self.output_dir = output_dir
        self.metadata = metadata
        self.manifest_path = os.path.join(output_dir, "manifest.json")

    def save(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata.model_dump(), f, indent=2)

    @classmethod
    def load(cls, manifest_path: str) -> "EpisodeManifest":
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        meta = EpisodeMetadata(**data)
        return cls(output_dir=os.path.dirname(manifest_path), metadata=meta)
