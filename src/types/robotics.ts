export interface CartesianPose {
  x: number;
  y: number;
  z: number;
  roll: number;
  pitch: number;
  yaw: number;
}

export interface JointState {
  positions: number[];
  velocities?: number[];
  torques?: number[];
}

export interface GripperState {
  position: number; // mm
  is_closed: boolean;
  effort: number;   // N
  is_moving: boolean;
}

export interface RobotTelemetry {
  timestamp: number;
  monotonic_ns: number;
  sequence_number: number;
  joint_state: JointState;
  tcp_pose: CartesianPose;
  gripper_state: GripperState;
  is_in_estop: boolean;
  is_safe: boolean;
  controller_status: string;
}

export interface LeaderState {
  timestamp: number;
  sequence_number: number;
  cartesian_pose: CartesianPose;
  gripper_trigger: number; // 0.0 to 1.0
  deadman_pressed: boolean;
  clutch_pressed: boolean;
}

export interface TeleopAction {
  timestamp: number;
  sequence_number: number;
  target_tcp_pose: CartesianPose;
  target_gripper_position: number;
}

export interface EpisodeRecord {
  episode_id: string;
  task_id: string;
  operator_id: string;
  robot_id: string;
  leader_id: string;
  start_time: string;
  end_time?: string;
  duration_seconds: number;
  total_frames: number;
  calibration_version: string;
  software_version: string;
  outcome: 'success' | 'failure' | 'recording';
  validation_status: 'PASS' | 'FAIL' | 'NEEDS_REVIEW' | 'RECORDING';
  human_review_status: 'APPROVED' | 'REJECTED' | 'UNREVIEWED';
  checks?: Record<string, boolean>;
  reasons?: string[];
}

export interface HardwareSpecForm {
  manufacturer: string;
  model: string;
  controller: string;
  numJoints: number;
  gripper: string;
  leaderModel: string;
  followerModel: string;
  cameraModels: string;
  computer: string;
  os: string;
  cpu: string;
  gpu: string;
  ram: string;
  networkInterface: string;
  robotIp: string;
  robotPort: number;
  communicationProtocol: string;
  sdkVersion: string;
  ros2Version: string;
  ros2Driver: string;
  firmware: string;
  estopArchitecture: string;
}
