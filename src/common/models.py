"""Data models for telemetry, commands, kinematics, and state tracking."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time


class CartesianPose(BaseModel):
    """Cartesian pose in 3D workspace (positions in meters, orientation in roll-pitch-yaw radians)."""
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float


class JointState(BaseModel):
    """Joint space state representation."""
    positions: List[float] = Field(..., description="Joint angles in radians")
    velocities: Optional[List[float]] = Field(default=None, description="Joint velocities in rad/s")
    torques: Optional[List[float]] = Field(default=None, description="Joint torques in Nm")


class GripperState(BaseModel):
    """End-effector gripper status."""
    position: float = Field(..., description="Opening distance in mm or normalized [0.0, 1.0]")
    is_closed: bool = False
    effort: Optional[float] = Field(default=None, description="Grip force in Newtons")
    is_moving: bool = False


class RobotTelemetry(BaseModel):
    """Synchronized snapshot of robot status."""
    timestamp: float = Field(default_factory=time.time)
    monotonic_timestamp_ns: int = 0
    sequence_number: int = 0
    joint_state: JointState
    tcp_pose: CartesianPose
    gripper_state: GripperState
    is_in_estop: bool = False
    is_safe: bool = True
    controller_status: str = "nominal"


class LeaderState(BaseModel):
    """State sample from the master/leader arm or input device."""
    timestamp: float = Field(default_factory=time.time)
    monotonic_timestamp_ns: int = 0
    sequence_number: int = 0
    joint_positions: Optional[List[float]] = None
    cartesian_pose: Optional[CartesianPose] = None
    gripper_trigger: float = 0.0  # Normalized [0.0=open, 1.0=closed]
    deadman_pressed: bool = True
    clutch_pressed: bool = False


class TeleopAction(BaseModel):
    """Normalized safe action command issued to the follower arm."""
    timestamp: float = Field(default_factory=time.time)
    sequence_number: int = 0
    target_joint_positions: Optional[List[float]] = None
    target_tcp_pose: Optional[CartesianPose] = None
    target_gripper_position: float = 0.0
    command_mode: str = "cartesian_pose"


class EpisodeMetadata(BaseModel):
    """Standard demonstration episode metadata."""
    episode_id: str
    task_id: str
    operator_id: str
    robot_id: str
    leader_id: str
    environment_id: str = "bench_01"
    start_time: str
    end_time: Optional[str] = None
    duration_seconds: float = 0.0
    total_frames: int = 0
    calibration_version: str = "CAL_01"
    software_version: str = "0.1.0"
    driver_mode: str = "simulation"
    outcome: str = "success"  # "success" | "failure" | "interrupted"
    extra: Dict[str, Any] = Field(default_factory=dict)
