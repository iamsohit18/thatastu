# Troubleshooting & Diagnostics

## Common Hardware & Diagnostic Issues

### 1. "Robot adapter: HARDWARE SPECIFICATION REQUIRED"
- **Cause**: Application is attempting to run physical mode before vendor SDK has been configured.
- **Remedy**: Switch to `driver_mode: "simulation"` in `config/robot.yaml` or provide vendor SDK documentation to implement the vendor adapter.

### 2. "Timestamp gap exceeded threshold (>80ms)"
- **Cause**: Network packet delay or USB hub bandwidth saturation.
- **Remedy**: Ensure USB 3.0 cameras are connected to independent host controllers rather than an unpowered hub.

### 3. "Emergency Stop Latched"
- **Cause**: Software or physical E-Stop triggered.
- **Remedy**: Verify workcell clearance, confirm physical E-stop button is released, then click Reset E-Stop in the operator dashboard.
