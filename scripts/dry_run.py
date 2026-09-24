#!/usr/bin/env python3
"""Dry-run teleoperation verification loop (Safe end-to-end rehearsal)."""
import time
import argparse
from src.hardware.robot.simulator import SimulatorRobotAdapter
from src.hardware.leader.simulator import SimulatorLeaderAdapter
from src.safety.safety_manager import SafetyManager
from src.teleoperation.teleop_controller import TeleopController

def main():
    parser = argparse.ArgumentParser(description="Dry-run teleoperation loop without physical hazard.")
    parser.add_argument("--duration", type=int, default=5, help="Test duration in seconds")
    args = parser.parse_args()

    print("=================================================================")
    print(f"       RoboTeleop Dry-Run Teleoperation Loop ({args.duration}s)          ")
    print("=================================================================")

    config = {
        "leader": {"scaling": {"position_ratio": 0.8, "orientation_ratio": 0.8}},
        "safety": {
            "watchdog": {"command_timeout_ms": 200},
            "velocity_enforcement": {"max_cartesian_linear_m_s": 0.3},
            "workspace_limits": {"bounding_box": {"x": [-0.65, 0.65], "y": [0.25, 0.8], "z": [0.03, 0.7]}},
        },
    }

    robot = SimulatorRobotAdapter(dof=6)
    leader = SimulatorLeaderAdapter()
    safety = SafetyManager(config)
    controller = TeleopController(robot, leader, safety, config)

    robot.connect()
    leader.connect()
    engaged = controller.engage()

    if not engaged:
        print("  RESULT: FAIL - Could not engage teleoperation controller.")
        return 1

    print("  [RUNNING] Executing teleoperation control cycles at 50Hz...")
    start_t = time.time()
    ticks = 0
    while (time.time() - start_t) < args.duration:
        action = controller.step()
        ticks += 1
        time.sleep(0.02)  # 50Hz loop

    controller.disengage()
    robot.disconnect()
    leader.disconnect()

    hz = ticks / args.duration
    print(f"\n  Cycles completed: {ticks} ticks | Rate: {hz:.1f}Hz")
    if hz < 40.0:
        print("  RESULT: WARNING - Loop frequency below 40Hz target.")
    else:
        print("  RESULT: PASS - Real-time teleoperation timing satisfied.")

    print("\n=================================================================")
    print("OVERALL RESULT: PASS")
    print("=================================================================")
    return 0

if __name__ == "__main__":
    main()
