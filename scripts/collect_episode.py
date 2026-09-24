#!/usr/bin/env python3
"""CLI demonstration collection and validation runner."""
import time
import argparse
from src.hardware.robot.simulator import SimulatorRobotAdapter
from src.hardware.leader.simulator import SimulatorLeaderAdapter
from src.hardware.cameras.camera_manager import CameraManager
from src.safety.safety_manager import SafetyManager
from src.teleoperation.teleop_controller import TeleopController
from src.recording.episode_manager import EpisodeManager
from src.validation.validator import EpisodeValidator

def main():
    parser = argparse.ArgumentParser(description="Collect and validate a human demonstration episode.")
    parser.add_argument("--task", default="washer_pick_place", help="Task ID")
    parser.add_argument("--operator", default="operator_01", help="Operator ID")
    parser.add_argument("--duration", type=int, default=4, help="Duration in seconds")
    args = parser.parse_args()

    print("=================================================================")
    print(f"  Collecting Demonstration Episode: {args.task} ({args.duration}s)")
    print("=================================================================")

    config = {
        "leader": {"scaling": {"position_ratio": 0.8, "orientation_ratio": 0.8}},
        "safety": {
            "watchdog": {"command_timeout_ms": 200},
            "velocity_enforcement": {"max_cartesian_linear_m_s": 0.3},
            "workspace_limits": {"bounding_box": {"x": [-0.65, 0.65], "y": [0.25, 0.8], "z": [0.03, 0.7]}},
        },
        "recording": {"output_base_dir": "./data/episodes"},
        "cameras": {"devices": [{"id": "cam_wrist"}, {"id": "cam_overhead"}, {"id": "cam_side"}]},
    }

    robot = SimulatorRobotAdapter(dof=6)
    leader = SimulatorLeaderAdapter()
    safety = SafetyManager(config)
    controller = TeleopController(robot, leader, safety, config)
    camera_mgr = CameraManager(config)
    episode_mgr = EpisodeManager(config)
    validator = EpisodeValidator()

    robot.connect()
    leader.connect()
    camera_mgr.connect_all()
    camera_mgr.start_all()

    recorder = episode_mgr.create_episode(
        task_id=args.task,
        operator_id=args.operator,
        robot_id="sim_robot",
        leader_id="sim_leader",
    )

    recorder.start({cid: {"resolution": (640, 480), "fps": 30} for cid in camera_mgr.get_camera_ids()})
    controller.engage()

    print("  [RECORDING] Streaming telemetry, actions, and camera frames...")
    start_t = time.time()
    while (time.time() - start_t) < args.duration:
        action = controller.step()
        telemetry = robot.get_robot_state()
        cams = camera_mgr.capture_synchronized_frames()
        recorder.record_step(telemetry=telemetry, action=action, camera_frames=cams["frames"])
        time.sleep(0.02)

    controller.disengage()
    metadata = episode_mgr.stop_current_episode(outcome="success")
    camera_mgr.stop_all()
    robot.disconnect()
    leader.disconnect()

    print(f"\n  Episode {metadata.episode_id} finished:")
    print(f"  Duration: {metadata.duration_seconds:.2f}s | Total Frames: {metadata.total_frames}")

    print("\n[VALIDATING EPISODE]")
    ep_dir = f"./data/episodes/{metadata.episode_id}"
    val_result = validator.validate_episode(ep_dir)
    print(f"  Validation Status: {val_result['status']}")
    print(f"  Checks: {val_result['checks']}")
    if val_result["reasons"]:
        print(f"  Reasons: {val_result['reasons']}")

    print("\n=================================================================")
    print(f"OVERALL RESULT: {val_result['status']}")
    print("=================================================================")
    return 0

if __name__ == "__main__":
    main()
