"""Workspace boundary checking and virtual fixtures."""
from typing import Tuple, Dict, Any
from src.common.models import CartesianPose
from src.common.exceptions import SafetyViolationError


class WorkspaceLimits:
    """Enforces spatial safety envelopes to prevent table collisions or out-of-reach singularity."""

    def __init__(self, config: Dict[str, Any]):
        limits = config.get("safety", {}).get("workspace_limits", {})
        bb = limits.get("bounding_box", {})
        self.x_bounds: Tuple[float, float] = tuple(bb.get("x", [-0.70, 0.70]))
        self.y_bounds: Tuple[float, float] = tuple(bb.get("y", [0.20, 0.85]))
        self.z_bounds: Tuple[float, float] = tuple(bb.get("z", [0.03, 0.75]))
        self.table_margin_m: float = limits.get("table_safety_margin_m", 0.03)

    def validate_pose(self, pose: CartesianPose) -> CartesianPose:
        """
        Validates and clamps or raises if target pose breaches workspace boundaries.
        Returns clamped safe CartesianPose.
        """
        # Table collision floor check
        min_safe_z = self.z_bounds[0] + self.table_margin_m
        if pose.z < min_safe_z:
            raise SafetyViolationError(
                f"TCP Z-coordinate {pose.z:.3f}m violates table protection minimum {min_safe_z:.3f}m."
            )

        if not (self.x_bounds[0] <= pose.x <= self.x_bounds[1]):
            raise SafetyViolationError(
                f"TCP X-coordinate {pose.x:.3f}m outside allowed bounds {self.x_bounds}."
            )

        if not (self.y_bounds[0] <= pose.y <= self.y_bounds[1]):
            raise SafetyViolationError(
                f"TCP Y-coordinate {pose.y:.3f}m outside allowed bounds {self.y_bounds}."
            )

        if pose.z > self.z_bounds[1]:
            raise SafetyViolationError(
                f"TCP Z-coordinate {pose.z:.3f}m exceeds ceiling bound {self.z_bounds[1]}m."
            )

        return pose

    def clamp_pose(self, pose: CartesianPose) -> CartesianPose:
        """Soft clamps the pose within the bounding box for continuous teleop operation."""
        min_safe_z = self.z_bounds[0] + self.table_margin_m
        clamped_x = max(self.x_bounds[0], min(self.x_bounds[1], pose.x))
        clamped_y = max(self.y_bounds[0], min(self.y_bounds[1], pose.y))
        clamped_z = max(min_safe_z, min(self.z_bounds[1], pose.z))

        return CartesianPose(
            x=clamped_x,
            y=clamped_y,
            z=clamped_z,
            roll=pose.roll,
            pitch=pose.pitch,
            yaw=pose.yaw,
        )
