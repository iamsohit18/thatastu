"""Robots management API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/robots", tags=["robots"])

# In-memory robot status registry
ROBOTS_DB = {
    "follower_arm_01": {
        "id": "follower_arm_01",
        "name": "Follower Manipulator Arm",
        "dof": 6,
        "mode": "simulation",
        "status": "connected",
        "is_safe": True,
        "estop": False,
        "ip": "192.168.1.100",
        "joint_positions": [0.0, -0.785, 0.0, -1.57, 0.0, 1.57],
        "tcp_pose": {"x": 0.45, "y": 0.0, "z": 0.35, "roll": 0.0, "pitch": 1.57, "yaw": 0.0},
    }
}


@router.get("", response_model=List[Dict[str, Any]])
def list_robots():
    return list(ROBOTS_DB.values())


@router.get("/{robot_id}")
def get_robot(robot_id: str):
    if robot_id not in ROBOTS_DB:
        raise HTTPException(status_code=404, detail="Robot ID not found")
    return ROBOTS_DB[robot_id]


@router.post("/{robot_id}/connect")
def connect_robot(robot_id: str):
    if robot_id not in ROBOTS_DB:
        raise HTTPException(status_code=404, detail="Robot ID not found")
    ROBOTS_DB[robot_id]["status"] = "connected"
    return {"status": "connected", "robot_id": robot_id}


@router.post("/{robot_id}/disconnect")
def disconnect_robot(robot_id: str):
    if robot_id not in ROBOTS_DB:
        raise HTTPException(status_code=404, detail="Robot ID not found")
    ROBOTS_DB[robot_id]["status"] = "disconnected"
    return {"status": "disconnected", "robot_id": robot_id}
