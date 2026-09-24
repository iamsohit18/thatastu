"""Factory module for instantiating robot driver adapters based on configuration."""
from typing import Dict, Any
from src.hardware.robot.interface import RobotInterface
from src.hardware.robot.simulator import SimulatorRobotAdapter
from src.hardware.robot.vendor.robot_adapter import VendorRobotAdapter
from src.common.exceptions import ConfigurationError
from src.common.logging import get_logger, log_event
import logging

logger = get_logger("robot_factory")


class RobotFactory:
    @staticmethod
    def create(config: Dict[str, Any]) -> RobotInterface:
        """
        Instantiate robot adapter based on configuration dictionary.
        """
        robot_cfg = config.get("robot", {})
        driver_mode = robot_cfg.get("driver_mode", "simulation").lower()
        num_joints = robot_cfg.get("hardware_spec", {}).get("num_joints", 6)

        if driver_mode == "simulation":
            log_event(logger, logging.INFO, "robot_factory", "CREATED", f"Creating SimulatorRobotAdapter with {num_joints} DoF")
            return SimulatorRobotAdapter(dof=num_joints)

        elif driver_mode == "vendor_adapter":
            net_cfg = robot_cfg.get("hardware_spec", {}).get("network", {})
            ip = net_cfg.get("ip_address", "127.0.0.1")
            port = net_cfg.get("port", 30003)
            log_event(logger, logging.INFO, "robot_factory", "CREATED", f"Creating VendorRobotAdapter for {ip}:{port}")
            return VendorRobotAdapter(ip_address=ip, port=port, num_joints=num_joints)

        elif driver_mode == "ros2":
            # ROS 2 driver adapter fallback / bridge
            raise NotImplementedError("ROS 2 package not loaded. Configure ros2_ws driver first.")

        else:
            raise ConfigurationError(f"Unsupported robot driver mode: {driver_mode}")
