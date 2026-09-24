"""
Vendor-Specific Gripper Adapter Stub.

=============================================================================
HARDWARE SPECIFICATION ARCHITECTURAL DOCUMENTATION:
=============================================================================
WHAT IT DOES:
  Communicates with the robotic end-effector (e.g. Robotiq 2F-85/140, OnRobot RG2,
  Schunk, or custom servo gripper) over Modbus RTU / RS485 / TCP / CAN.

WHY IT EXISTS:
  To encapsulate vendor command words, registers, activations, and force feedback
  into a simple millimeter/Newton standard interface.

HOW IT COMMUNICATES:
  [TODO: CONFIGURATION REQUIRED]
  Awaiting gripper hardware specifications (e.g. Modbus RTU over RS-485 or USB).

WHAT INPUT IT RECEIVES:
  - Target position (0.0 to max opening in mm), gripping effort limit (Newtons).

WHAT OUTPUT IT PRODUCES:
  - GripperState: Current position, object detected status, active force.

WHAT CAN GO WRONG:
  - Gripper fault / emergency stall.
  - Serial bus timeout or baudrate mismatch.

HOW IT IS TESTED:
  - Calibration stroke test: Cycle open/close without load, confirm end stops.
=============================================================================
"""
from typing import Optional
from src.hardware.gripper.interface import GripperInterface
from src.common.models import GripperState
from src.common.exceptions import ConfigurationError


class VendorGripperAdapter(GripperInterface):
    def __init__(self, port: str = "/dev/ttyUSB_GRIPPER", baud_rate: int = 115200):
        self._port = port
        self._baud = baud_rate
        self._connected = False

    def connect(self) -> bool:
        """TODO: CONFIGURATION REQUIRED - Send activation sequence to physical gripper."""
        raise ConfigurationError(
            "Gripper hardware connection requires gripper model and communication specs. "
            "Please configure gripper vendor specifications."
        )

    def disconnect(self) -> None:
        self._connected = False

    def open(self) -> bool:
        raise NotImplementedError("Vendor gripper open command not configured.")

    def close(self) -> bool:
        raise NotImplementedError("Vendor gripper close command not configured.")

    def set_position(self, position_mm: float, effort_n: Optional[float] = None) -> bool:
        raise NotImplementedError("Vendor gripper position command not configured.")

    def get_state(self) -> GripperState:
        raise NotImplementedError("Vendor gripper state query not configured.")
