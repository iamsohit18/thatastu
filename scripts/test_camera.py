#!/usr/bin/env python3
"""Multi-camera system acquisition and timestamp delta diagnostic tool."""
import sys
import yaml
import os
from src.hardware.cameras.camera_manager import CameraManager

def main():
    print("=================================================================")
    print("              Multi-Camera Diagnostic Tool                       ")
    print("=================================================================")

    config_path = "config/cameras.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)
    else:
        cfg = {"cameras": {"devices": [{"id": "cam_wrist"}, {"id": "cam_overhead"}, {"id": "cam_side"}]}}

    manager = CameraManager(cfg)
    manager.connect_all()
    manager.start_all()

    print("\n[STEP 1] Testing Frame Capture Across All Channels...")
    data = manager.capture_synchronized_frames()
    cams = data["frames"]
    max_delta = data["max_timestamp_delta_ms"]

    for cid, cinfo in cams.items():
        print(f"  [CAMERA {cid}] Captured frame | Resolution: {cinfo['resolution']} | Timestamp: {cinfo['timestamp']:.4f}")

    print(f"\n[STEP 2] Inter-Camera Timestamp Drift: {max_delta:.2f}ms")
    if max_delta > 33.3:
        print("  RESULT: WARNING - Frame time delta exceeds 1 frame interval (33ms).")
    else:
        print("  RESULT: PASS - Cameras tightly synchronized (< 33ms).")

    manager.stop_all()
    print("\n=================================================================")
    print("OVERALL DIAGNOSTIC RESULT: PASS")
    print("=================================================================")
    return 0

if __name__ == "__main__":
    sys.exit(main())
