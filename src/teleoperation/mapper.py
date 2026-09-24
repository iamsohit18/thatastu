"""Teleoperation mapping layer: transforms raw leader inputs into normalized commands."""
from typing import Dict, Any, Optional
from src.common.models import LeaderState, CartesianPose, TeleopAction
from src.teleoperation.coordinate_transform import CoordinateTransformer
from src.teleoperation.motion_scaling import MotionScaler


class TeleopMapper:
    """
    Translates raw master input (Cartesian pose or joint angles, analog trigger)
    into normalized follower action candidates.
    """

    def __init__(self, config: Dict[str, Any]):
        leader_cfg = config.get("leader", {})
        scaling_cfg = leader_cfg.get("scaling", {})

        self.scaler = MotionScaler(
            position_ratio=scaling_cfg.get("position_ratio", 0.8),
            orientation_ratio=scaling_cfg.get("orientation_ratio", 0.8),
            deadband_m=scaling_cfg.get("deadband_translation_m", 0.003),
            deadband_rad=scaling_cfg.get("deadband_rotation_rad", 0.03),
        )
        self.transformer = CoordinateTransformer()
        self._initial_leader_pose: Optional[CartesianPose] = None
        self._initial_follower_pose: Optional[CartesianPose] = None

    def reset_origin(self, leader_pose: CartesianPose, follower_pose: CartesianPose) -> None:
        """Calibrates initial relative reference poses upon teleop engagement."""
        self._initial_leader_pose = leader_pose
        self._initial_follower_pose = follower_pose

    def map_leader_state(self, leader_state: LeaderState, current_follower_pose: CartesianPose) -> CartesianPose:
        """
        Maps leader state to a candidate follower pose.
        If initial reference poses are recorded, computes relative scaled trajectory.
        """
        if leader_state.cartesian_pose is None:
            return current_follower_pose

        if self._initial_leader_pose is None or self._initial_follower_pose is None:
            self.reset_origin(leader_state.cartesian_pose, current_follower_pose)
            return current_follower_pose

        # Compute delta from start
        dx = leader_state.cartesian_pose.x - self._initial_leader_pose.x
        dy = leader_state.cartesian_pose.y - self._initial_leader_pose.y
        dz = leader_state.cartesian_pose.z - self._initial_leader_pose.z

        d_roll = leader_state.cartesian_pose.roll - self._initial_leader_pose.roll
        d_pitch = leader_state.cartesian_pose.pitch - self._initial_leader_pose.pitch
        d_yaw = leader_state.cartesian_pose.yaw - self._initial_leader_pose.yaw

        delta = CartesianPose(x=dx, y=dy, z=dz, roll=d_roll, pitch=d_pitch, yaw=d_yaw)
        scaled_delta = self.scaler.apply_scale(delta)

        candidate_pose = CartesianPose(
            x=self._initial_follower_pose.x + scaled_delta.x,
            y=self._initial_follower_pose.y + scaled_delta.y,
            z=self._initial_follower_pose.z + scaled_delta.z,
            roll=self._initial_follower_pose.roll + scaled_delta.roll,
            pitch=self._initial_follower_pose.pitch + scaled_delta.pitch,
            yaw=self._initial_follower_pose.yaw + scaled_delta.yaw,
        )

        return candidate_pose
