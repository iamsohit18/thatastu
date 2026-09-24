"""Motion scaling and deadband filtering for fine teleoperation control."""
import math
from src.common.models import CartesianPose


class MotionScaler:
    """
    Applies configurable gear ratios and tremor deadbands.
    Prevents jerky movements and allows micrometric assembly demonstrations.
    """

    def __init__(
        self,
        position_ratio: float = 0.8,
        orientation_ratio: float = 0.8,
        deadband_m: float = 0.003,
        deadband_rad: float = 0.03,
    ):
        self.position_ratio = position_ratio
        self.orientation_ratio = orientation_ratio
        self.deadband_m = deadband_m
        self.deadband_rad = deadband_rad

    def apply_scale(self, delta_pose: CartesianPose) -> CartesianPose:
        """Scales displacement deltas while filtering out vibrations below deadband."""
        trans_mag = math.sqrt(delta_pose.x**2 + delta_pose.y**2 + delta_pose.z**2)
        if trans_mag < self.deadband_m:
            sx, sy, sz = 0.0, 0.0, 0.0
        else:
            sx = delta_pose.x * self.position_ratio
            sy = delta_pose.y * self.position_ratio
            sz = delta_pose.z * self.position_ratio

        # Orientation filtering
        s_roll = 0.0 if abs(delta_pose.roll) < self.deadband_rad else delta_pose.roll * self.orientation_ratio
        s_pitch = 0.0 if abs(delta_pose.pitch) < self.deadband_rad else delta_pose.pitch * self.orientation_ratio
        s_yaw = 0.0 if abs(delta_pose.yaw) < self.deadband_rad else delta_pose.yaw * self.orientation_ratio

        return CartesianPose(x=sx, y=sy, z=sz, roll=s_roll, pitch=s_pitch, yaw=s_yaw)
