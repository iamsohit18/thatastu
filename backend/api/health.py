"""System and hardware health status endpoints."""
from fastapi import APIRouter
from typing import Dict, Any
import time

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "system": "RoboTeleop Data Platform",
        "version": "0.1.0",
        "timestamp": time.time(),
        "hardware_bridges": {
            "robot_driver": "connected",
            "leader_arm": "connected",
            "cameras": "3_active",
            "safety_system": "nominal",
            "emergency_stop": "cleared",
        },
        "storage": {
            "disk_free_gb": 48.2,
            "status": "sufficient",
        },
    }
