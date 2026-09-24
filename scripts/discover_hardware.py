#!/usr/bin/env python3
"""Hardware discovery script to probe network interfaces, USB serial ports, and cameras."""
import os
import sys
import glob

print("=================================================================")
print("           RoboTeleop Hardware Discovery Utility                ")
print("=================================================================")

# 1. Probe USB serial devices (Potential Leader arms, Grippers)
print("\n[PROBING USB/SERIAL DEVICES]")
serial_ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
if serial_ports:
    for p in serial_ports:
        print(f"  [FOUND] Serial Port: {p}")
    print("  RESULT: PASS - Detected serial devices.")
else:
    print("  [WARNING] No /dev/ttyUSB* or /dev/ttyACM* ports detected.")
    print("  RESULT: WARNING - Leader arm or Gripper may require USB connection or simulation mode.")

# 2. Probe Video Devices (Cameras)
print("\n[PROBING V4L2 VIDEO DEVICES]")
video_devices = glob.glob("/dev/video*")
if video_devices:
    for v in video_devices:
        print(f"  [FOUND] Video Device: {v}")
    print(f"  RESULT: PASS - Found {len(video_devices)} video device endpoints.")
else:
    print("  [WARNING] No /dev/video* devices found. Synthetic camera stream will be used for testing.")
    print("  RESULT: WARNING - Synthetic vision fallback active.")

# 3. Check Network Interface & Ping Robot IP
print("\n[PROBING ROBOT NETWORK INTERFACE]")
robot_ip = os.getenv("ROBOT_HOST", "192.168.1.100")
print(f"  Configured Robot IP: {robot_ip}")
ret = os.system(f"ping -c 1 -W 1 {robot_ip} > /dev/null 2>&1")
if ret == 0:
    print(f"  [FOUND] Ping response from {robot_ip}")
    print("  RESULT: PASS - Physical robot network reachable.")
else:
    print(f"  [INFO] Robot IP {robot_ip} unreachable or ping disabled.")
    print("  RESULT: WARNING - Ensure robotics isolated subnet is connected, or use simulation mode.")

print("\n=================================================================")
print("Discovery complete. For physical control, provide exact vendor specs.")
print("=================================================================")
