# Calibration Guide

## Purpose
Demonstration data collection requires accurate mapping between the leader's spatial motion and the follower's workspace.

## Procedures

### 1. Master Zero-Point Calibration
1. Place the master handle into the mechanical home jig.
2. Run `python scripts/calibrate.py`.
3. Verify encoder readings match reference zero rad $\pm 0.005\text{rad}$.

### 2. Gripper Stroke Calibration
1. Command open stroke until hardware endstop is reached ($85.0\text{mm}$).
2. Command complete closure ($0.0\text{mm}$).
3. Map analog trigger min/max ADC values to normalized $[0.0, 1.0]$.

### 3. Eye-in-Hand & Eye-to-Hand Camera Extrinsics
- Use an ArUco or checkerboard target mounted at a known offset from the robot base.
- Save transformation matrices in `config/calibration/extrinsics.yaml`.
