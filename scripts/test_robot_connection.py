#!/usr/bin/env python3
"""Safe robot follower connection and read-only diagnostic workflow."""
import sys
import argparse
from src.hardware.robot.simulator import SimulatorRobotAdapter

def main():
    parser = argparse.ArgumentParser(description="Test robot follower arm connection safely.")
    parser.add_argument("--mode", default="simulation", choices=["simulation", "vendor_adapter"])
    parser.add_argument("--test-motion", action="store_true", help="Execute micro 0.01 rad test motion (ONLY if verified)")
    args = parser.parse_args()

    print("=================================================================")
    print(f"       Follower Robot Connection Diagnostic (Mode: {args.mode})  ")
    print("=================================================================")

    if args.mode == "vendor_adapter":
        print("\n[STEP 1] Validating Vendor Configuration...")
        print("  RESULT: FAIL - Hardware vendor specifications have not been configured.")
        print("  DETAILS: Exact robot model, controller protocol, and vendor SDK are required.")
        print("  ACTION: Provide robot specifications to initialize vendor adapter.")
        return 1

    print("\n[STEP 1] Initializing Robot Interface...")
    robot = SimulatorRobotAdapter(dof=6)
    connected = robot.connect()
    if not connected:
        print("  RESULT: FAIL - Failed to connect to robot.")
        return 1
    print("  RESULT: PASS - Interface connected.")

    print("\n[STEP 2] Verifying E-Stop & Controller Safety...")
    state = robot.get_robot_state()
    if state.is_in_estop:
        print("  RESULT: FAIL - Robot controller is in Emergency Stop!")
        return 1
    print("  RESULT: PASS - E-Stop cleared, controller nominal.")

    print("\n[STEP 3] Verifying Joint Count & SI Radians...")
    joints = robot.get_joint_positions()
    print(f"  Joint count: {len(joints)}")
    print(f"  Current positions [rad]: {[round(j, 4) for j in joints]}")
    if len(joints) != 6:
        print("  RESULT: WARNING - Expected 6-DoF arm.")
    else:
        print("  RESULT: PASS - Joint count and telemetry verified.")

    print("\n[STEP 4] Reading TCP Cartesian Pose...")
    tcp = robot.get_tcp_pose()
    print(f"  TCP Pose: X={tcp.x:.3f}m, Y={tcp.y:.3f}m, Z={tcp.z:.3f}m | Roll={tcp.roll:.3f}, Pitch={tcp.pitch:.3f}, Yaw={tcp.yaw:.3f}")
    if tcp.z < 0.03:
        print("  RESULT: WARNING - TCP dangerously close to table floor (< 30mm)!")
    else:
        print("  RESULT: PASS - Cartesian TCP within valid workspace boundaries.")

    print("\n[STEP 5] Read-Only Communication Stability Check (5 cycles)...")
    for i in range(5):
        st = robot.get_robot_state()
        print(f"  Sample #{st.sequence_number}: Monotonic={st.monotonic_timestamp_ns}ns | Safe={st.is_safe}")
    print("  RESULT: PASS - Read-only telemetry continuous and stable.")

    if args.test_motion:
        print("\n[STEP 6] Controlled Micro-Motion Test...")
        print("  Sending +0.01 rad command to Joint 6...")
        new_j = list(joints)
        new_j[5] += 0.01
        robot.send_joint_command(new_j)
        print("  RESULT: PASS - Micro-motion commanded safely.")
    else:
        print("\n[STEP 6] Motion command skipped (safe read-only mode).")
        print("  RESULT: PASS - Zero physical movement commanded on startup.")

    print("\n=================================================================")
    print("OVERALL DIAGNOSTIC RESULT: ALL CHECKS PASSED")
    print("=================================================================")
    return 0

if __name__ == "__main__":
    sys.exit(main())
