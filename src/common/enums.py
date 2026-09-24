"""Common enumeration types across the teleoperation platform."""
from enum import Enum


class DriverMode(str, Enum):
    SIMULATION = "simulation"
    VENDOR_ADAPTER = "vendor_adapter"
    ROS2 = "ros2"


class DeviceStatus(str, Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    ESTOP_ACTIVE = "estop_active"


class TeleopState(str, Enum):
    STANDBY = "standby"
    CALIBRATING = "calibrating"
    ENGAGED = "engaged"
    PAUSED = "paused"
    FAULT = "fault"


class ValidationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class ControlMode(str, Enum):
    JOINT_POSITION = "joint_position"
    CARTESIAN_POSE = "cartesian_pose"
    JOINT_VELOCITY = "joint_velocity"
