"""Factory module for creating master/leader adapters."""
from typing import Dict, Any
from src.hardware.leader.interface import LeaderInterface
from src.hardware.leader.simulator import SimulatorLeaderAdapter
from src.hardware.leader.vendor.leader_adapter import VendorLeaderAdapter
from src.common.exceptions import ConfigurationError
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("leader_factory")


class LeaderFactory:
    @staticmethod
    def create(config: Dict[str, Any]) -> LeaderInterface:
        leader_cfg = config.get("leader", {})
        driver_mode = leader_cfg.get("driver_mode", "simulation").lower()

        if driver_mode == "simulation":
            log_event(logger, logging.INFO, "leader_factory", "CREATED", "Creating SimulatorLeaderAdapter")
            return SimulatorLeaderAdapter()

        elif driver_mode == "vendor_adapter":
            hw_spec = leader_cfg.get("hardware_spec", {})
            port = hw_spec.get("serial_port", "/dev/ttyUSB_LEADER")
            baud = hw_spec.get("baud_rate", 1000000)
            log_event(logger, logging.INFO, "leader_factory", "CREATED", f"Creating VendorLeaderAdapter on {port}@{baud}")
            return VendorLeaderAdapter(serial_port=port, baud_rate=baud)

        else:
            raise ConfigurationError(f"Unsupported leader driver mode: {driver_mode}")
