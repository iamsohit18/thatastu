# Teleoperation Pipeline

## Concept
The teleoperation loop translates human intent into safe robot actuator commands at 50Hz:

```python
while teleoperation_enabled:
    leader_state = leader.read_state()
    target = mapper.map_leader_state(leader_state, current_follower_pose)
    target = safety.validate_action(current_telemetry, target)
    follower.send_cartesian_command(target)
    recorder.record_step(telemetry, action, camera_frames)
```

## Motion Scaling & Tremor Rejection
- Hand tremors smaller than $3\text{mm}$ translation or $0.03\text{rad}$ rotation are filtered out by the deadband.
- Scale ratio $0.8\times$ allows human operators to perform delicate insertions without overshooting.
