# Testing & Validation Strategy

## Test Hierarchy

1. **Unit Testing (`pytest tests/unit`)**:
   - Coordinate transforms and mathematical frame operations
   - Motion deadband filtering and scale factor arithmetic
   - Workspace limit bounding box clamp and table floor clearance
   - Velocity rate clamping
   - Monotonic timestamp anomaly detection (duplicate timestamps, time reversal, excessive jitter)

2. **Integration Testing (`pytest tests/integration`)**:
   - Full simulator teleoperation loop with simulated leader, follower arm, and recorder
   - Episode file serialization (manifest, Parquet tables, validation JSON)

3. **Hardware-in-the-Loop (HIL) Testing**:
   - Run `python scripts/test_robot_connection.py --mode vendor_adapter` (Read-only, zero physical motion)
   - Inspect continuous joint telemetry stream at 50Hz without packet drop
   - Verify hardware E-Stop latching and unlatching response
   - Micro-motion test (0.01 rad) with manual deadman switch held

4. **Fault Injection Testing**:
   - Disconnecting leader USB during teleoperation -> Immediate standstill
   - Network latency spikes -> Watchdog timeout stops robot in <150ms
   - Sensor frame drop -> Validator flags episode as `NEEDS_REVIEW`
