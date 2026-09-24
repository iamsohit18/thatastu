# Data Format & Schema Specification

## Episode Directory Structure

```
data/episodes/EP_20260924_120000_a1b2c3/
├── manifest.json              # Episode metadata, versions, duration, outcome
├── validation.json            # 11-point inspection results & human review sign-off
├── robot/
│   └── telemetry.parquet      # High-rate joint angles, velocities, torques, TCP pose
├── actions/
│   └── actions.parquet        # Commanded targets and gripper apertures
└── cameras/
    ├── cam_wrist.mp4          # Wrist camera video stream
    ├── cam_overhead.mp4       # Overhead top-down workspace camera
    └── cam_side.mp4           # Third-person perspective camera
```

## Schema Details

### Manifest (`manifest.json`)
```json
{
  "episode_id": "EP_20260924_120000_a1b2c3",
  "task_id": "washer_pick_place",
  "robot_id": "follower_arm_01",
  "operator_id": "operator_alpha",
  "start_time": "2026-09-24T12:00:00Z",
  "end_time": "2026-09-24T12:00:45Z",
  "duration_seconds": 45.2,
  "total_frames": 2260,
  "calibration_version": "CAL_01",
  "software_version": "0.1.0",
  "outcome": "success"
}
```
