"""Dataset aggregation and export API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/datasets", tags=["datasets"])

DATASETS_DB = [
    {
        "id": "ds_precision_insertion_v1",
        "name": "Precision Insertion Dataset v1",
        "task_id": "peg_in_hole",
        "version": "1.0.0",
        "total_episodes": 42,
        "format": "LeRobot (Parquet + MP4)",
        "created_at": "2026-09-24T08:00:00Z",
    }
]


class ExportDatasetRequest(BaseModel):
    dataset_name: str
    episode_ids: List[str]
    target_format: str = "lerobot"


@router.get("", response_model=List[Dict[str, Any]])
def list_datasets():
    return DATASETS_DB


@router.post("/export")
def export_dataset(req: ExportDatasetRequest):
    new_ds = {
        "id": f"ds_{req.dataset_name.lower().replace(' ', '_')}",
        "name": req.dataset_name,
        "task_id": "washer_pick_place",
        "version": "1.0.0",
        "total_episodes": len(req.episode_ids),
        "format": req.target_format,
        "created_at": "2026-09-24T12:15:00Z",
    }
    DATASETS_DB.append(new_ds)
    return {"status": "success", "dataset": new_ds}
