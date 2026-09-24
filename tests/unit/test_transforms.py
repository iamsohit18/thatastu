"""Unit tests for coordinate transformation and scaling."""
from src.common.models import CartesianPose
from src.teleoperation.motion_scaling import MotionScaler
from src.teleoperation.coordinate_transform import CoordinateTransformer

def test_motion_scaler_deadband():
    scaler = MotionScaler(position_ratio=1.0, deadband_m=0.005)
    # Below 5mm deadband
    tiny_delta = CartesianPose(x=0.002, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0)
    scaled = scaler.apply_scale(tiny_delta)
    assert scaled.x == 0.0

    # Above deadband
    significant_delta = CartesianPose(x=0.02, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0)
    scaled_sig = scaler.apply_scale(significant_delta)
    assert scaled_sig.x == 0.02

def test_motion_scaling_ratio():
    scaler = MotionScaler(position_ratio=0.5, deadband_m=0.001)
    delta = CartesianPose(x=0.04, y=0.02, z=0.06, roll=0.0, pitch=0.0, yaw=0.0)
    scaled = scaler.apply_scale(delta)
    assert abs(scaled.x - 0.02) < 1e-4
    assert abs(scaled.y - 0.01) < 1e-4
    assert abs(scaled.z - 0.03) < 1e-4
