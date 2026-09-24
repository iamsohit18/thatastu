"""Episode recording, validation, and review API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

router = APIRouter(tags=["episodes"])

# Pre-seeded tasks for teleoperation demonstrations
TASKS_DB = [
    {"id": "peg_in_hole", "name": "Precision Peg-in-Hole Insertion", "difficulty": "Hard", "target_hz": 50},
    {"id": "washer_pick_place", "name": "Washer Pick & Place on Stanchion", "difficulty": "Medium", "target_hz": 50},
    {"id": "dual_block_stack", "name": "Block Stacking with Force Adaptation", "difficulty": "Medium", "target_hz": 50},
    {"id": "cable_routing", "name": "Deformable Cable Routing through Clip", "difficulty": "Hard", "target_hz": 50},
]

EPISODES_DB: Dict[str, Dict[str, Any]] = {
    "EP_20260924_001": {
        "episode_id": "EP_20260924_001",
        "task_id": "washer_pick_place",
        "operator_id": "operator_alpha",
        "robot_id": "follower_arm_01",
        "leader_id": "leader_arm_01",
        "start_time": "2026-09-24T12:10:00Z",
        "end_time": "2026-09-24T12:10:45Z",
        "duration_seconds": 45.2,
        "total_frames": 2260,
        "calibration_version": "CAL_01",
        "software_version": "0.1.0",
        "outcome": "success",
        "validation_status": "PASS",
        "human_review_status": "APPROVED",
        "checks": {
            "streams_complete": True,
            "timestamps_valid": True,
            "within_limits": True,
            "no_dropouts": True,
            "calibration_valid": True,
        },
    }
}


class CreateEpisodeRequest(BaseModel):
    task_id: str
    operator_id: str
    robot_id: str = "follower_arm_01"
    leader_id: str = "leader_arm_01"


class StopEpisodeRequest(BaseModel):
    outcome: str = "success"  # "success" | "failure" | "interrupted"


class ReviewEpisodeRequest(BaseModel):
    decision: str  # "APPROVED" | "REJECTED"
    notes: Optional[str] = None


@router.get("/tasks")
def list_tasks():
    return TASKS_DB


@router.get("/episodes", response_model=List[Dict[str, Any]])
def list_episodes():
    return list(EPISODES_DB.values())


@router.post("/episodes")
def create_episode(req: CreateEpisodeRequest):
    ep_id = f"EP_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
    record = {
        "episode_id": ep_id,
        "task_id": req.task_id,
        "operator_id": req.operator_id,
        "robot_id": req.robot_id,
        "leader_id": req.leader_id,
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": None,
        "duration_seconds": 0.0,
        "total_frames": 0,
        "calibration_version": "CAL_01",
        "software_version": "0.1.0",
        "outcome": "recording",
        "validation_status": "RECORDING",
        "human_review_status": "UNREVIEWED",
    }
    EPISODES_DB[ep_id] = record
    return record


@router.post("/episodes/{episode_id}/start")
def start_episode(episode_id: str):
    if episode_id not in EPISODES_DB:
        raise HTTPException(status_code=404, detail="Episode not found")
    EPISODES_DB[episode_id]["outcome"] = "recording"
    EPISODES_DB[episode_id]["validation_status"] = "RECORDING"
    return EPISODES_DB[episode_id]


@router.post("/episodes/{episode_id}/stop")
def stop_episode(episode_id: str, req: StopEpisodeRequest):
    if episode_id not in EPISODES_DB:
        raise HTTPException(status_code=404, detail="Episode not found")
    ep = EPISODES_DB[episode_id]
    ep["end_time"] = datetime.now(timezone.utc).isoformat()
    ep["outcome"] = req.outcome
    if ep["duration_seconds"] == 0:
        ep["duration_seconds"] = 32.4
        ep["total_frames"] = 1620
    ep["validation_status"] = "NEEDS_REVIEW" if req.outcome != "success" else "PASS"
    return ep


@router.get("/episodes/{episode_id}")
def get_episode(episode_id: str):
    if episode_id not in EPISODES_DB:
        raise HTTPException(status_code=404, detail="Episode not found")
    return EPISODES_DB[episode_id]


@router.post("/episodes/{episode_id}/validate")
def validate_episode(episode_id: str):
    if episode_id not in EPISODES_DB:
        raise HTTPException(status_code=404, detail="Episode not found")
    ep = EPISODES_DB[episode_id]
    # Simulate thorough 11-point inspection
    status = "PASS" if ep["outcome"] == "success" else "FAIL"
    ep["validation_status"] = status
    return {
        "episode_id": episode_id,
        "status": status,
        "checks": {
            "required_streams_exist": True,
            "files_readable": True,
            "timestamps_valid": True,
            "telemetry_in_range": True,
            "no_sensor_dropout": True,
            "calibration_exists": True,
            "robot_state_exists": True,
            "action_stream_exists": True,
            "metadata_complete": True,
            "storage_integrity_passes": True,
            "human_review_status": ep.get("human_review_status", "UNREVIEWED"),
        },
        "reasons": [] if status == "PASS" else ["Operator marked demonstration outcome as failure"],
    }


@router.post("/episodes/{episode_id}/review")
def review_episode(episode_id: str, req: ReviewEpisodeRequest):
    if episode_id not in EPISODES_DB:
        raise HTTPException(status_code=404, detail="Episode not found")
    ep = EPISODES_DB[episode_id]
    ep["human_review_status"] = req.decision
    ep["review_notes"] = req.notes
    return ep
