"""Camera system API endpoints."""
from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/cameras", tags=["cameras"])

CAMERAS_DB = [
    {
        "id": "cam_wrist",
        "name": "End-Effector Wrist Camera",
        "role": "wrist",
        "resolution": [640, 480],
        "fps": 30,
        "status": "active",
        "sync_delta_ms": 1.2,
    },
    {
        "id": "cam_overhead",
        "name": "Top-Down Workspace Camera",
        "role": "overhead",
        "resolution": [1280, 720],
        "fps": 30,
        "status": "active",
        "sync_delta_ms": 1.5,
    },
    {
        "id": "cam_side",
        "name": "Third-Person Perspective Camera",
        "role": "perspective",
        "resolution": [640, 480],
        "fps": 30,
        "status": "active",
        "sync_delta_ms": 2.1,
    },
]


@router.get("", response_model=List[Dict[str, Any]])
def list_cameras():
    return CAMERAS_DB
