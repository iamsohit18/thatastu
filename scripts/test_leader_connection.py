#!/usr/bin/env python3
"""Safe leader/master arm connection and telemetry verification script."""
import sys
import argparse
from src.hardware.leader.simulator import SimulatorLeaderAdapter

def main():
    parser = argparse.ArgumentParser(description="Test master/leader arm connection safely.")
    parser.add_argument("--mode", default="simulation", choices=["simulation", "vendor_adapter"])
    args = parser.parse_args()

    print("=================================================================")
    print(f"        Leader Arm Diagnostic Tool (Mode: {args.mode})           ")
    print("=================================================================")

    if args.mode == "vendor_adapter":
        print("\n[STEP 1] Validating Leader Vendor Configuration...")
        print("  RESULT: FAIL - Master hardware model and serial protocol not configured.")
        print("  ACTION: Provide leader arm hardware specs.")
        return 1

    leader = SimulatorLeaderAdapter()
    if not leader.connect():
        print("  RESULT: FAIL - Could not connect to leader device.")
        return 1
    print("  RESULT: PASS - Leader interface connected.")

    print("\n[STEP 2] Inspecting Master Telemetry Sample...")
    state = leader.read_state()
    print(f"  Sample sequence: {state.sequence_number}")
    print(f"  Gripper trigger: {state.gripper_trigger:.2f} (0.0=open, 1.0=closed)")
    print(f"  Deadman pressed: {state.deadman_pressed}")
    if state.cartesian_pose:
        print(f"  Pose: X={state.cartesian_pose.x:.3f}, Y={state.cartesian_pose.y:.3f}, Z={state.cartesian_pose.z:.3f}")
    print("  RESULT: PASS - Master telemetry read successfully.")

    print("\n=================================================================")
    print("OVERALL DIAGNOSTIC RESULT: PASS")
    print("=================================================================")
    return 0

if __name__ == "__main__":
    sys.exit(main())
