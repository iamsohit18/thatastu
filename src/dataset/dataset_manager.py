"""Robotics Dataset Aggregation and Partition Management."""
import os
import json
import shutil
from typing import List, Dict, Any, Optional
from src.common.models import EpisodeMetadata


class DatasetManager:
    """Manages collections of validated episodes into structured datasets for model training."""

    def __init__(self, storage_dir: str = "./data"):
        self.storage_dir = storage_dir
        self.episodes_dir = os.path.join(storage_dir, "episodes")
        self.datasets_dir = os.path.join(storage_dir, "datasets")
        os.makedirs(self.datasets_dir, exist_ok=True)

    def list_datasets(self) -> List[Dict[str, Any]]:
        datasets = []
        if not os.path.exists(self.datasets_dir):
            return []

        for name in os.listdir(self.datasets_dir):
            ds_path = os.path.join(self.datasets_dir, name)
            info_path = os.path.join(ds_path, "dataset_info.json")
            if os.path.isfile(info_path):
                with open(info_path, "r", encoding="utf-8") as f:
                    datasets.append(json.load(f))
        return datasets

    def create_dataset(
        self,
        dataset_name: str,
        episode_ids: List[str],
        task_id: str,
        version: str = "v1.0",
    ) -> Dict[str, Any]:
        ds_dir = os.path.join(self.datasets_dir, dataset_name)
        os.makedirs(ds_dir, exist_ok=True)

        info = {
            "dataset_name": dataset_name,
            "version": version,
            "task_id": task_id,
            "total_episodes": len(episode_ids),
            "episode_ids": episode_ids,
            "export_format": "lerobot_compatible_parquet",
        }

        with open(os.path.join(ds_dir, "dataset_info.json"), "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2)

        return info
