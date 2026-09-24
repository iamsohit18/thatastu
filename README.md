# RoboTeleop Data Platform

A production-oriented modular robotics platform for human teleoperation, safe follower arm control, and synchronized demonstration data collection for imitation learning (Behavioral Cloning, Diffusion Policy, ACT) and robotics foundation models.

---

## System Overview

```
Human Operator
     │
     ▼
[Leader / Master Robotic Arm] (Joints, Pose, Gripper)
     │
     ▼
[Teleoperation Mapping Layer] (Workspace calibration, coordinate transform, scaling, deadzone)
     │
     ▼
[Safety Layer] (Workspace bounds, joint limits, velocity caps, watchdog, E-Stop)
     │
     ▼
[Follower Robotic Arm] (Hardware adapter or High-fidelity Simulator)
     │
     ├── Telemetry Acquisition (Positions, Velocities, Torques, TCP, Gripper)
     ├── Multi-Camera System (Wrist, Overhead, Side - time-stamped)
     └── Action Logging (Target joints / TCP commands)
     │
     ▼
[Time Synchronization & Episode Recording] (Monotonic clocks, software sync, manifest.json)
     │
     ▼
[Data Validation Pipeline] (11-point inspection: PASS / FAIL / NEEDS_REVIEW)
     │
     ▼
[Training-Ready Robotics Dataset] (Parquet telemetry + actions, MP4 video streams, manifest)
```

---

## Hardware Configuration Requirement

> ⚠️ **CRITICAL SAFETY NOTICE:**
> Real hardware requires exact vendor SDKs, communication protocols, controller register maps, and safety hardware loops. 
> The platform includes:
> 1. `RobotInterface` & `LeaderInterface` (Pure abstraction)
> 2. `SimulatorRobotAdapter` & `SimulatorLeaderAdapter` (Simulation & testing)
> 3. `VendorRobotAdapter` & `VendorLeaderAdapter` (Structured stubs clearly marked with `TODO: CONFIGURATION REQUIRED`)
>
> **Never operate real physical robotics without verifying physical E-stop, deadman switches, and workspace boundaries.**

---

## Directory Layout

```
roboteleop/
├── README.md
├── LICENSE
├── .env.example
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── config/
│   ├── robot.yaml
│   ├── leader.yaml
│   ├── cameras.yaml
│   ├── safety.yaml
│   ├── recording.yaml
│   └── system.yaml
├── src/
│   ├── hardware/
│   ├── teleoperation/
│   ├── safety/
│   ├── synchronization/
│   ├── recording/
│   ├── validation/
│   ├── dataset/
│   ├── monitoring/
│   └── common/
├── backend/
│   ├── main.py
│   ├── api/
│   └── database/
├── scripts/
│   ├── discover_hardware.py
│   ├── test_robot_connection.py
│   ├── test_leader_connection.py
│   ├── test_camera.py
│   ├── calibrate.py
│   ├── dry_run.py
│   └── collect_episode.py
├── tests/
├── ros2_ws/
└── docs/
```

---

## Quick Start (Simulation Mode)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Hardware Discovery & Configuration Check
python scripts/discover_hardware.py

# 3. Test Leader Connection (Simulation / Read-only)
python scripts/test_leader_connection.py --mode simulation

# 4. Test Robot Connection (Simulation / Read-only)
python scripts/test_robot_connection.py --mode simulation

# 5. Run Dry-Run Teleoperation Loop (No physical movement commanded)
python scripts/dry_run.py --duration 10

# 6. Launch Backend API Server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 7. Launch Operator Web Dashboard
npm run dev
```

---

## License

Apache-2.0 License.
