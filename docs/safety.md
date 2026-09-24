# Safety Architecture & Risk Mitigation

## Critical Notice
> **SOFTWARE SAFETY IS NOT A REPLACEMENT FOR HARDWARE SAFETY.**
> Software checks are a secondary supervision layer. All physical workcells must be equipped with physical dual-channel hardware Emergency Stop pushbuttons, light curtains, or collaborative torque/speed safety limits certified under ISO 10218-1/2 and ISO/TS 15066.

## Multi-Layer Safety Guardrails

### 1. Watchdog & Communication Loss
- High-rate heartbeat (10Hz-50Hz).
- If no command is received within `command_timeout_ms` (default: 150ms), the follower arm automatically decelerates to a complete stop.

### 2. Workspace Bounding Envelopes
- Soft and hard Cartesian bounding limits:
  - $X \in [-0.65m, +0.65m]$
  - $Y \in [+0.25m, +0.80m]$
  - $Z \in [+0.03m, +0.70m]$
- Floor clearance of $\ge 30\text{mm}$ is enforced to protect workbenches and fixturing.

### 3. Velocity & Acceleration Clamping
- Max linear Cartesian velocity capped at $0.30\text{m/s}$.
- Max angular rotation rate capped at $0.70\text{rad/s}$.
- Joint velocity limited to $50\%$ of manufacturer nominal ratings during teleoperation.

### 4. Deadman Switch
- The leader device or operator dashboard requires active deadman engagement. Releasing the switch immediately freezes follower motion without resetting the master reference origin.
