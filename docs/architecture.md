# RoboTeleop System Architecture

## 1. Architectural Philosophy
The RoboTeleop platform is designed around **strict decoupling of real-time control, hardware abstractions, safety guardrails, and dataset curation**.
In physical robotics, mixing vendor-specific networking loops directly into recording or teleoperation business logic creates severe safety hazards, vendor lock-in, and fragile synchronization.

## 2. Core Architectural Layers

```
Layer 1: Physical / Simulator Hardware (Franka, UR, GELLO, USB Cams, V4L2)
                │
Layer 2: Hardware Adapters (RobotInterface, LeaderInterface, CameraInterface)
                │
Layer 3: Teleoperation Pipeline (Coordinate mapping, Gear scaling, Tremor deadband)
                │
Layer 4: Safety Supervisor (Workspace boundary box, Table safety floor, Velocity caps, Hardware E-stop)
                │
Layer 5: Synchronization Engine (Monotonic timestamps, sequence numbers, jitter detector)
                │
Layer 6: Demonstration Recording (Parquet tabular streams + MP4 video + manifest.json)
                │
Layer 7: 11-Point Validation Pipeline (PASS / FAIL / NEEDS_REVIEW)
                │
Layer 8: High-Level API & Operator UI (FastAPI + React 19 + Interactive Teleop Twin)
```

## 3. Why Abstraction Layers Exist
Changing the follower robot manufacturer (e.g. migrating from Franka Emika to Universal Robots UR5e or Kinova Gen3) requires updating **only** the `VendorRobotAdapter` in `src/hardware/robot/vendor/`.
The higher-level teleoperation mapping, data recording schema, operator UI, safety checking, and dataset export remain 100% untouched.
