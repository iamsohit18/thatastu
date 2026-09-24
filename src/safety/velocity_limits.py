"""Velocity rate limiter and delta clamp to prevent sudden jerks or excessive speeds."""
import math
from typing import Dict, Any, Optional
from src.common.models import CartesianPose
from src.common.exceptions import SafetyViolationError


class VelocityLimits:
    """Enforces velocity caps and computes max displacement per teleoperation cycle."""

    def __init__(self, config: Dict[str, Any]):
        vel_cfg = config.get("safety", {}).get("velocity_enforcement", {})
        self.max_linear_vel = vel_cfg.get("max_cartesian_linear_m_s", 0.30)
        self.max_angular_vel = vel_cfg.get("max_cartesian_angular_rad_s", 0.70)
        self.max_joint_scale = vel_cfg.get("max_joint_velocity_scale", 0.50)

    def clamp_velocity(
        self,
        current_pose: CartesianPose,
        target_pose: CartesianPose,
        dt_seconds: float,
    ) -> CartesianPose:
        """
        Limits step displacement between current and target poses to max allowable velocity.
        """
        if dt_seconds <= 0.0:
            return current_pose

        dx = target_pose.x - current_pose.x
        dy = target_pose.y - current_pose.y
        dz = target_pose.z - current_pose.z

        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        max_dist = self.max_linear_vel * dt_seconds

        if dist > max_dist and dist > 1e-6:
            scale = max_dist / dist
            clamped_x = current_pose.x + dx * scale
            clamped_y = current_pose.y + dy * scale
            clamped_z = current_pose.z + dz * scale
        else:
            clamped_x = target_pose.x
            clamped_y = target_pose.y
            clamped_z = target_pose.z

        return CartesianPose(
            x=clamped_x,
            y=clamped_y,
            z=clamped_z,
            roll=target_pose.roll,
            pitch=target_pose.pitch,
            yaw=target_pose.yaw,
        )
