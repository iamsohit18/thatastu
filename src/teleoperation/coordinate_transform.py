"""Coordinate frame transformations between leader reference frame and robot base frame."""
import math
from typing import Tuple
from src.common.models import CartesianPose


class CoordinateTransformer:
    """
    Transforms 3D position and orientation offsets from master coordinate frame
    into the follower robot base coordinate frame.
    """

    def __init__(self, rotation_rpy: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        self.roll_offset = rotation_rpy[0]
        self.pitch_offset = rotation_rpy[1]
        self.yaw_offset = rotation_rpy[2]

    def transform_pose(self, leader_pose: CartesianPose, reference_origin: CartesianPose) -> CartesianPose:
        """
        Computes delta from origin and maps to robot frame.
        """
        # Apply orientation transformation
        transformed_roll = leader_pose.roll + self.roll_offset
        transformed_pitch = leader_pose.pitch + self.pitch_offset
        transformed_yaw = leader_pose.yaw + self.yaw_offset

        # Standard Euclidean translation mapping
        return CartesianPose(
            x=leader_pose.x,
            y=leader_pose.y,
            z=leader_pose.z,
            roll=transformed_roll,
            pitch=transformed_pitch,
            yaw=transformed_yaw,
        )
