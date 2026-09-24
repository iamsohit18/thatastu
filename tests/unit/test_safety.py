"""Unit tests for workspace and velocity safety limits."""
import pytest
from src.common.models import CartesianPose
from src.common.exceptions import SafetyViolationError, EmergencyStopActiveError
from src.safety.workspace_limits import WorkspaceLimits
from src.safety.velocity_limits import VelocityLimits
from src.safety.emergency_stop import EmergencyStopManager

def test_workspace_table_floor_violation():
    cfg = {"safety": {"workspace_limits": {"bounding_box": {"x": [-0.6, 0.6], "y": [0.2, 0.8], "z": [0.03, 0.7]}, "table_safety_margin_m": 0.03}}}
    ws = WorkspaceLimits(cfg)

    # Pose below table margin (0.03 + 0.03 = 0.06m)
    dangerous_pose = CartesianPose(x=0.0, y=0.4, z=0.02, roll=0.0, pitch=0.0, yaw=0.0)
    with pytest.raises(SafetyViolationError):
        ws.validate_pose(dangerous_pose)

def test_velocity_limit_clamping():
    cfg = {"safety": {"velocity_enforcement": {"max_cartesian_linear_m_s": 0.20}}}
    vl = VelocityLimits(cfg)
    curr = CartesianPose(x=0.0, y=0.0, z=0.3, roll=0.0, pitch=0.0, yaw=0.0)
    # Huge jump of 0.5m in 0.02s
    jump = CartesianPose(x=0.5, y=0.0, z=0.3, roll=0.0, pitch=0.0, yaw=0.0)
    clamped = vl.clamp_velocity(curr, jump, dt_seconds=0.02)
    # Max displacement = 0.20 * 0.02 = 0.004m
    assert abs(clamped.x - 0.004) < 1e-4

def test_emergency_stop_latched():
    estop = EmergencyStopManager()
    assert not estop.is_triggered
    estop.trigger("Testing E-Stop")
    assert estop.is_triggered

    with pytest.raises(EmergencyStopActiveError):
        estop.assert_safe()

    estop.reset()
    assert not estop.is_triggered
