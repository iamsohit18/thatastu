import React, { useState } from 'react';
import { X, Code, FileText, Check, Copy } from 'lucide-react';

interface YamlViewerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const YamlViewerModal: React.FC<YamlViewerModalProps> = ({ isOpen, onClose }) => {
  const [activeConfig, setActiveConfig] = useState<'robot' | 'leader' | 'safety' | 'cameras'>('robot');
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const configs = {
    robot: `# config/robot.yaml
robot:
  id: "follower_arm_01"
  name: "Follower Manipulator Arm"
  driver_mode: "simulation" # "simulation" | "vendor_adapter" | "ros2"

  hardware_spec:
    manufacturer: "TODO: CONFIGURATION REQUIRED (e.g. Franka, UR, Kinova)"
    model: "TODO: CONFIGURATION REQUIRED (e.g. FR3, UR5e)"
    controller_model: "TODO: CONFIGURATION REQUIRED"
    num_joints: 6
    communication_protocol: "TODO: CONFIGURATION REQUIRED"
    network:
      ip_address: "192.168.1.100"
      port: 30003

  joint_limits:
    position_lower: [-3.14159, -1.5708, -3.14159, -3.14159, -2.0944, -6.28318]
    position_upper: [3.14159, 1.5708, 3.14159, 3.14159, 2.0944, 6.28318]
    velocity_max: [1.5, 1.5, 1.5, 2.0, 2.0, 2.5]
    torque_max: [87.0, 87.0, 87.0, 45.0, 12.0, 12.0]

  cartesian_limits:
    x_min: -0.70
    x_max: 0.70
    y_min: 0.20
    y_max: 0.85
    z_min: 0.05
    z_max: 0.75
    linear_velocity_max: 0.35
    angular_velocity_max: 0.8`,

    leader: `# config/leader.yaml
leader:
  id: "leader_arm_01"
  name: "Master Teleoperation Arm"
  driver_mode: "simulation"

  hardware_spec:
    manufacturer: "TODO: CONFIGURATION REQUIRED (e.g. GELLO / Aloha Master)"
    model: "TODO: CONFIGURATION REQUIRED"
    serial_port: "/dev/ttyUSB_LEADER"
    baud_rate: 1000000

  scaling:
    position_ratio: 0.8
    orientation_ratio: 0.8
    deadband_translation_m: 0.003
    deadband_rotation_rad: 0.03

  gripper:
    input_type: "analog_trigger"
    trigger_min_raw: 200
    trigger_max_raw: 3900`,

    safety: `# config/safety.yaml
safety:
  watchdog:
    heartbeat_interval_ms: 50
    command_timeout_ms: 150

  emergency_stop:
    software_estop_enabled: true
    hardware_estop_monitoring: true

  velocity_enforcement:
    max_cartesian_linear_m_s: 0.30
    max_cartesian_angular_rad_s: 0.70
    max_joint_velocity_scale: 0.50

  workspace_limits:
    table_safety_margin_m: 0.03
    enforce_bounding_box: true
    bounding_box:
      x: [-0.65, 0.65]
      y: [0.25, 0.80]
      z: [0.03, 0.70]`,

    cameras: `# config/cameras.yaml
cameras:
  synchronization_mode: "software_monotonic"
  max_acceptable_frame_delta_ms: 33.3

  devices:
    - id: "cam_wrist"
      name: "End-Effector Wrist Camera"
      role: "wrist"
      resolution: [640, 480]
      fps: 30

    - id: "cam_overhead"
      name: "Top-Down Workspace Camera"
      role: "overhead"
      resolution: [1280, 720]
      fps: 30

    - id: "cam_side"
      name: "Third-Person Perspective Camera"
      role: "perspective"
      resolution: [640, 480]
      fps: 30`,
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(configs[activeConfig]);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-3xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <Code className="w-5 h-5 text-sky-400" />
            <h2 className="text-base font-bold text-white">System YAML Configurations</h2>
          </div>
          <button onClick={onClose} className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab selection */}
        <div className="flex border-b border-slate-800 bg-slate-950/50 px-6 gap-2 pt-2">
          {(['robot', 'leader', 'safety', 'cameras'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveConfig(tab)}
              className={`px-3 py-1.5 text-xs font-mono rounded-t-lg transition-colors capitalize ${
                activeConfig === tab
                  ? 'bg-slate-900 text-sky-400 border-t border-x border-slate-700 font-semibold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab}.yaml
            </button>
          ))}
        </div>

        {/* YAML Display */}
        <div className="p-4 bg-slate-950 flex-1 overflow-y-auto">
          <pre className="font-mono text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-4 rounded-xl border border-slate-800/80">
            {configs[activeConfig]}
          </pre>
        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 bg-slate-950 border-t border-slate-800 flex items-center justify-between">
          <span className="text-xs text-slate-400">Path: /config/{activeConfig}.yaml</span>
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium border border-slate-700 transition-colors"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            {copied ? 'Copied' : 'Copy YAML'}
          </button>
        </div>
      </div>
    </div>
  );
};
