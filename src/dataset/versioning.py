"""Semantic versioning and schema migration for robotics demonstration datasets."""
from typing import Dict, Any


class DatasetVersioner:
    @staticmethod
    def get_current_schema_version() -> str:
        return "1.1.0"

    @staticmethod
    def is_compatible(dataset_version: str) -> bool:
        major = dataset_version.split(".")[0]
        return major == "1"
