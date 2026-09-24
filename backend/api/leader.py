"""Master/Leader input arm API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/leaders", tags=["leaders"])

LEADERS_DB = {
    "leader_arm_01": {
        "id": "leader_arm_01",
        "name": "Master Teleoperation Arm",
        "mode": "simulation",
        "status": "connected",
        "deadman_pressed": True,
        "gripper_trigger": 0.0,
        "pose": {"x": 0.45, "y": 0.0, "z": 0.35, "roll": 0.0, "pitch": 1.57, "yaw": 0.0},
    }
}


@router.get("", response_model=List[Dict[str, Any]])
def list_leaders():
    return list(LEADERS_DB.values())


@router.post("/{leader_id}/connect")
def connect_leader(leader_id: str):
    if leader_id not in LEADERS_DB:
        raise HTTPException(status_code=404, detail="Leader ID not found")
    LEADERS_DB[leader_id]["status"] = "connected"
    return {"status": "connected", "leader_id": leader_id}
