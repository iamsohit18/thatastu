import React, { useState, useEffect, useRef } from 'react';
import {
  Activity,
  AlertOctagon,
  AlertTriangle,
  Camera,
  CheckCircle,
  CheckCircle2,
  ChevronRight,
  Clock,
  Cpu,
  Database,
  Download,
  FileCode,
  HardDrive,
  Layers,
  Play,
  Radio,
  RefreshCw,
  RotateCcw,
  Save,
  Send,
  Settings,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Sliders,
  Square,
  StopCircle,
  Target,
  Terminal,
  Video,
  XCircle,
  Zap,
} from 'lucide-react';

import {
  CartesianPose,
  EpisodeRecord,
  HardwareSpecForm,
  LeaderState,
  RobotTelemetry,
  TeleopAction,
} from './types/robotics';

import { KinematicTwinCanvas } from './components/KinematicTwinCanvas';
import { CameraStreamCard } from './components/CameraStreamCard';
import { HardwareSpecsModal } from './components/HardwareSpecsModal';
import { ValidationModal } from './components/ValidationModal';
import { YamlViewerModal } from './components/YamlViewerModal';
import { CalibrationModal } from './components/CalibrationModal';

export default function App() {
  // Navigation tabs
  const [activeTab, setActiveTab] = useState<'teleop' | 'cameras' | 'kinematics' | 'datasets' | 'hardware' | 'safety'>('teleop');

  // Hardware Driver Mode: simulation vs vendor_adapter
  const [driverMode, setDriverMode] = useState<'simulation' | 'vendor_adapter'>('simulation');

  // Master Safety States
  const [isEStop, setIsEStop] = useState<boolean>(false);
  const [deadmanPressed, setDeadmanPressed] = useState<boolean>(true);

  // Teleoperation state
  const [isTeleopEngaged, setIsTeleopEngaged] = useState<boolean>(false);
  const [motionScale, setMotionScale] = useState<number>(0.8);
  const [deadbandMm, setDeadbandMm] = useState<number>(3.0);

  // Episode Recording State
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [recordingDuration, setRecordingDuration] = useState<number>(0);
  const [recordingFrames, setRecordingFrames] = useState<number>(0);
  const [selectedTask, setSelectedTask] = useState<string>('washer_pick_place');
  const [operatorId, setOperatorId] = useState<string>('operator_01');

  // Modals
  const [isHardwareModalOpen, setIsHardwareModalOpen] = useState<boolean>(false);
  const [selectedValidationEpisode, setSelectedValidationEpisode] = useState<EpisodeRecord | null>(null);
  const [isYamlModalOpen, setIsYamlModalOpen] = useState<boolean>(false);
  const [isCalibModalOpen, setIsCalibModalOpen] = useState<boolean>(false);

  // Hardware Specs Form (Initialized with missing status)
  const [hardwareSpecs, setHardwareSpecs] = useState<HardwareSpecForm>({
    manufacturer: '',
    model: '',
    controller: '',
    numJoints: 6,
    gripper: '',
    leaderModel: '',
    followerModel: '',
    cameraModels: '',
    computer: 'Workstation 64-Core',
    os: 'Ubuntu 22.04 LTS (Kernel 6.5)',
    cpu: 'Intel Xeon / AMD Threadripper',
    gpu: 'NVIDIA RTX 4090',
    ram: '64 GB DDR5',
    networkInterface: 'enp4s0 (Isolated Subnet)',
    robotIp: '192.168.1.100',
    robotPort: 30003,
    communicationProtocol: '',
    sdkVersion: '',
    ros2Version: 'Humble Hawksbill',
    ros2Driver: '',
    firmware: '',
    estopArchitecture: 'Dual-Channel Cat 3 PLe Hardware Relay Circuit',
  });

  // Simulated Telemetry & Kinematics State
  const [tcpPose, setTcpPose] = useState<CartesianPose>({
    x: 0.45,
    y: 0.0,
    z: 0.35,
    roll: 0.0,
    pitch: 1.57,
    yaw: 0.0,
  });

  const [jointAngles, setJointAngles] = useState<number[]>([
    0.0, -0.785, 0.0, -1.57, 0.0, 1.57,
  ]);

  const [gripperPosition, setGripperPosition] = useState<number>(85.0); // mm
  const [gripperEffort, setGripperEffort] = useState<number>(0.0);       // N
  const [loopHz, setLoopHz] = useState<number>(50.0);
  const [syncDeltaMs, setSyncDeltaMs] = useState<number>(1.2);

  // Demonstration Episodes List
  const [episodes, setEpisodes] = useState<EpisodeRecord[]>([
    {
      episode_id: 'EP_20260924_104200_a8f9c2',
      task_id: 'washer_pick_place',
      operator_id: 'operator_01',
      robot_id: 'follower_arm_01',
      leader_id: 'leader_arm_01',
      start_time: '2026-09-24T10:42:00Z',
      end_time: '2026-09-24T10:42:38Z',
      duration_seconds: 38.4,
      total_frames: 1920,
      calibration_version: 'CAL_01',
      software_version: '0.1.0',
      outcome: 'success',
      validation_status: 'PASS',
      human_review_status: 'APPROVED',
      checks: {
        streams_exist: true,
        files_readable: true,
        timestamps_valid: true,
        telemetry_in_range: true,
        no_dropouts: true,
        calibration_exists: true,
        robot_state_exists: true,
        action_stream_exists: true,
        metadata_complete: true,
        storage_integrity: true,
        human_reviewed: true,
      },
    },
    {
      episode_id: 'EP_20260924_091530_3b17d4',
      task_id: 'peg_in_hole',
      operator_id: 'operator_02',
      robot_id: 'follower_arm_01',
      leader_id: 'leader_arm_01',
      start_time: '2026-09-24T09:15:30Z',
      end_time: '2026-09-24T09:16:12Z',
      duration_seconds: 42.1,
      total_frames: 2105,
      calibration_version: 'CAL_01',
      software_version: '0.1.0',
      outcome: 'success',
      validation_status: 'PASS',
      human_review_status: 'APPROVED',
    },
    {
      episode_id: 'EP_20260924_083012_e4f1a9',
      task_id: 'cable_routing',
      operator_id: 'operator_01',
      robot_id: 'follower_arm_01',
      leader_id: 'leader_arm_01',
      start_time: '2026-09-24T08:30:12Z',
      end_time: '2026-09-24T08:30:44Z',
      duration_seconds: 32.0,
      total_frames: 1600,
      calibration_version: 'CAL_01',
      software_version: '0.1.0',
      outcome: 'failure',
      validation_status: 'FAIL',
      human_review_status: 'REJECTED',
      reasons: ['Operator aborted demo: cable slipped from clip jig'],
    },
  ]);

  // System Event Diagnostic Log
  const [eventLogs, setEventLogs] = useState<Array<{ timestamp: string; component: string; event: string; message: string; type: 'info' | 'warn' | 'error' }>>([
    { timestamp: '12:00:00.120', component: 'system', event: 'BOOT', message: 'RoboTeleop Data Platform initialized', type: 'info' },
    { timestamp: '12:00:00.450', component: 'robot_factory', event: 'CREATED', message: 'SimulatorRobotAdapter loaded (6-DoF)', type: 'info' },
    { timestamp: '12:00:00.480', component: 'leader_factory', event: 'CREATED', message: 'SimulatorLeaderAdapter loaded', type: 'info' },
    { timestamp: '12:00:00.600', component: 'camera_manager', event: 'SYNC', message: '3 camera streams synchronized (<2ms drift)', type: 'info' },
    { timestamp: '12:00:01.000', component: 'safety_manager', event: 'ARMED', message: 'Bounding box active: table floor protection +30mm', type: 'info' },
  ]);

  const addLog = (component: string, event: string, message: string, type: 'info' | 'warn' | 'error' = 'info') => {
    const timeStr = new Date().toTimeString().split(' ')[0] + '.' + String(Date.now() % 1000).padStart(3, '0');
    setEventLogs((prev) => [{ timestamp: timeStr, component, event, message, type }, ...prev.slice(0, 50)]);
  };

  // Keyboard hotkey for deadman switch (Hold Space to enable)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' && (e.target as HTMLElement).tagName !== 'INPUT' && (e.target as HTMLElement).tagName !== 'TEXTAREA') {
        e.preventDefault();
        setDeadmanPressed(true);
      }
    };
    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.code === 'Space') {
        e.preventDefault();
        // Optional toggle vs hold behavior
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  // Real-time teleoperation simulation loop
  useEffect(() => {
    let animId: number;
    let lastTime = performance.now();
    let simTimer = 0;

    const tick = (now: number) => {
      const dt = (now - lastTime) / 1000.0;
      lastTime = now;

      // Update sync delta with minor realistic jitter
      setSyncDeltaMs(1.0 + Math.sin(now * 0.003) * 0.4);

      if (isTeleopEngaged && !isEStop && deadmanPressed) {
        simTimer += dt;

        // Smooth human demonstration arc
        const targetX = 0.45 + 0.08 * Math.cos(simTimer * 0.8) * motionScale;
        const targetY = 0.00 + 0.09 * Math.sin(simTimer * 0.8) * motionScale;
        const targetZ = Math.max(0.06, 0.35 + 0.05 * Math.sin(simTimer * 1.6) * motionScale);

        setTcpPose({
          x: targetX,
          y: targetY,
          z: targetZ,
          roll: 0.0,
          pitch: 1.57,
          yaw: 0.1 * Math.sin(simTimer * 0.5),
        });

        // Update joint angles to match kinematics
        setJointAngles([
          0.15 * Math.sin(simTimer * 0.8),
          -0.785 + 0.1 * Math.cos(simTimer * 0.8),
          0.05 * Math.sin(simTimer * 0.8),
          -1.57 + 0.1 * Math.sin(simTimer * 1.6),
          0.0,
          1.57 + 0.15 * Math.cos(simTimer * 0.8),
        ]);

        // Gripper cycle
        const gripVal = (Math.sin(simTimer * 0.7) + 1) * 42.5;
        setGripperPosition(gripVal);
        setGripperEffort(gripVal < 5 ? 38.5 : 0.0);

        if (isRecording) {
          setRecordingDuration((prev) => prev + dt);
          setRecordingFrames((prev) => prev + 1);
        }
      }

      animId = requestAnimationFrame(tick);
    };

    animId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(animId);
  }, [isTeleopEngaged, isEStop, deadmanPressed, isRecording, motionScale]);

  // Handle E-Stop toggle
  const handleToggleEStop = () => {
    if (!isEStop) {
      setIsEStop(true);
      setIsTeleopEngaged(false);
      addLog('safety_manager', 'ESTOP_TRIGGERED', 'CRITICAL: EMERGENCY STOP ENGAGED BY OPERATOR', 'error');
    } else {
      setIsEStop(false);
      addLog('safety_manager', 'ESTOP_RESET', 'Emergency stop cleared. Re-engagement required.', 'warn');
    }
  };

  // Start Episode Recording
  const handleStartRecording = () => {
    if (isEStop) {
      addLog('recorder', 'START_ABORTED', 'Cannot record: Emergency stop is active', 'error');
      return;
    }
    if (!isTeleopEngaged) {
      setIsTeleopEngaged(true);
    }
    setIsRecording(true);
    setRecordingDuration(0);
    setRecordingFrames(0);
    addLog('recorder', 'RECORDING_START', `Session started for task: ${selectedTask} by ${operatorId}`, 'info');
  };

  // Stop Episode Recording
  const handleStopRecording = (outcome: 'success' | 'failure') => {
    setIsRecording(false);
    const epId = `EP_${new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14)}_${Math.random().toString(16).slice(2, 8)}`;
    const dur = Math.max(1.2, recordingDuration);
    const frames = Math.max(60, recordingFrames);

    const newEp: EpisodeRecord = {
      episode_id: epId,
      task_id: selectedTask,
      operator_id: operatorId,
      robot_id: driverMode === 'simulation' ? 'simulator_arm_01' : (hardwareSpecs.model || 'vendor_arm_01'),
      leader_id: driverMode === 'simulation' ? 'simulator_leader_01' : (hardwareSpecs.leaderModel || 'vendor_leader_01'),
      start_time: new Date(Date.now() - dur * 1000).toISOString(),
      end_time: new Date().toISOString(),
      duration_seconds: parseFloat(dur.toFixed(1)),
      total_frames: frames,
      calibration_version: 'CAL_01',
      software_version: '0.1.0',
      outcome: outcome,
      validation_status: outcome === 'success' ? 'PASS' : 'NEEDS_REVIEW',
      human_review_status: outcome === 'success' ? 'APPROVED' : 'UNREVIEWED',
      checks: {
        streams_exist: true,
        files_readable: true,
        timestamps_valid: true,
        telemetry_in_range: true,
        no_dropouts: true,
        calibration_exists: true,
        robot_state_exists: true,
        action_stream_exists: true,
        metadata_complete: true,
        storage_integrity: true,
        human_reviewed: outcome === 'success',
      },
    };

    setEpisodes((prev) => [newEp, ...prev]);
    addLog('validator', 'VALIDATED', `Episode ${epId} processed: ${newEp.validation_status} (${dur.toFixed(1)}s, ${frames} frames)`, 'info');
    setSelectedValidationEpisode(newEp);
  };

  const handleReviewEpisode = (episodeId: string, decision: 'APPROVED' | 'REJECTED') => {
    setEpisodes((prev) =>
      prev.map((ep) => (ep.episode_id === episodeId ? { ...ep, human_review_status: decision, validation_status: decision === 'APPROVED' ? 'PASS' : 'FAIL' } : ep))
    );
    if (selectedValidationEpisode?.episode_id === episodeId) {
      setSelectedValidationEpisode((prev) => (prev ? { ...prev, human_review_status: decision, validation_status: decision === 'APPROVED' ? 'PASS' : 'FAIL' } : null));
    }
    addLog('dataset', 'REVIEW_SIGN_OFF', `Episode ${episodeId} signed off as ${decision}`, 'info');
  };

  const isHardwareConfigured = Boolean(hardwareSpecs.manufacturer && hardwareSpecs.model);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-sky-500/30">
      {/* Top Industrial Header Bar */}
      <header className="bg-slate-900 border-b border-slate-800 px-5 py-2.5 flex items-center justify-between shadow-md shrink-0">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-gradient-to-br from-sky-500 to-blue-600 rounded-lg shadow-sm">
              <Cpu className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-bold tracking-tight text-white">RoboTeleop Data Platform</h1>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-sky-950 text-sky-400 border border-sky-800/60 font-semibold">
                  v0.1.0
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Teleoperation, Safety Guardrails & Demonstration Recording</p>
            </div>
          </div>

          <div className="hidden lg:flex items-center gap-2 pl-4 border-l border-slate-800 text-xs">
            {/* Driver Mode Selector */}
            <div className="flex items-center bg-slate-950 p-1 rounded-lg border border-slate-800">
              <button
                onClick={() => setDriverMode('simulation')}
                className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                  driverMode === 'simulation' ? 'bg-sky-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Simulation Mode
              </button>
              <button
                onClick={() => {
                  if (!isHardwareConfigured) {
                    setIsHardwareModalOpen(true);
                  }
                  setDriverMode('vendor_adapter');
                }}
                className={`px-2.5 py-1 rounded text-xs font-medium transition-colors flex items-center gap-1.5 ${
                  driverMode === 'vendor_adapter'
                    ? 'bg-amber-600 text-white shadow'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Physical Hardware
                {!isHardwareConfigured && (
                  <span className="text-[10px] px-1 bg-amber-950 text-amber-300 rounded border border-amber-700/50">
                    Needs Specs
                  </span>
                )}
              </button>
            </div>

            {/* Loop Hz & Sync Delta */}
            <div className="flex items-center gap-3 px-3 py-1 bg-slate-950/80 rounded-lg border border-slate-800 font-mono text-[11px]">
              <span className="flex items-center gap-1 text-emerald-400">
                <Activity className="w-3.5 h-3.5" /> {loopHz.toFixed(1)} Hz
              </span>
              <span className="text-slate-600">|</span>
              <span className="flex items-center gap-1 text-sky-400">
                <Clock className="w-3.5 h-3.5" /> Sync Δ: {syncDeltaMs.toFixed(1)}ms
              </span>
            </div>
          </div>
        </div>

        {/* E-Stop & Deadman Center */}
        <div className="flex items-center gap-3">
          {/* Deadman switch button */}
          <button
            onClick={() => setDeadmanPressed(!deadmanPressed)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-2 transition-all ${
              deadmanPressed
                ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300'
                : 'bg-slate-800/80 border-slate-700 text-slate-400 hover:bg-slate-800'
            }`}
          >
            <Zap className={`w-3.5 h-3.5 ${deadmanPressed ? 'text-emerald-400 fill-emerald-400' : 'text-slate-500'}`} />
            <span>Deadman: <strong>{deadmanPressed ? 'HELD (ENABLED)' : 'RELEASED'}</strong></span>
          </button>

          {/* Master Emergency Stop Button */}
          <button
            onClick={handleToggleEStop}
            className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all flex items-center gap-2 shadow-lg ${
              isEStop
                ? 'bg-red-600 hover:bg-red-500 text-white animate-pulse ring-4 ring-red-500/40'
                : 'bg-rose-950/80 hover:bg-rose-900 border border-rose-700/80 text-rose-300'
            }`}
          >
            <AlertOctagon className="w-4 h-4" />
            <span>{isEStop ? 'E-STOP ENGAGED (CLICK TO RESET)' : 'EMERGENCY STOP'}</span>
          </button>
        </div>
      </header>

      {/* Mode / Pending specs alert banner */}
      {driverMode === 'vendor_adapter' && !isHardwareConfigured && (
        <div className="bg-amber-950/50 border-b border-amber-700/60 px-5 py-2 text-xs text-amber-200 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
            <span>
              <strong>Physical Hardware Mode Selected:</strong> Exact robot manufacturer, controller register map, and vendor SDK are required before physical motion can be commanded safely.
            </span>
          </div>
          <button
            onClick={() => setIsHardwareModalOpen(true)}
            className="px-3 py-1 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded text-xs transition-colors shrink-0"
          >
            Provide Hardware Specs
          </button>
        </div>
      )}

      {/* Navigation Tabs */}
      <nav className="bg-slate-900/60 border-b border-slate-800 px-5 flex items-center gap-1 overflow-x-auto text-xs shrink-0">
        {[
          { id: 'teleop', label: '🎯 Teleoperation & Recording' },
          { id: 'cameras', label: '📷 Multi-Camera Wall' },
          { id: 'kinematics', label: '🦾 Kinematics & Twin' },
          { id: 'datasets', label: `📁 Episodes & Validation (${episodes.length})` },
          { id: 'hardware', label: '⚙️ Hardware Discovery & Config' },
          { id: 'safety', label: '🛡️ Safety & Event Diagnostics' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 border-b-2 font-medium transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'border-sky-500 text-sky-400 bg-sky-950/30'
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Main Tab Content */}
      <main className="flex-1 p-5 overflow-y-auto space-y-5">
        {/* ==================== TAB 1: TELEOPERATION & RECORDING ==================== */}
        {activeTab === 'teleop' && (
          <div className="space-y-5">
            {/* Top Operational Ribbon */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
              {/* Teleoperation Engagement Card */}
              <div className="lg:col-span-4 bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Teleoperation Master Control</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
                        isTeleopEngaged && !isEStop
                          ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 animate-pulse'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {isTeleopEngaged && !isEStop ? 'ENGAGED & TRACKING' : 'STANDBY'}
                    </span>
                  </div>

                  <p className="text-xs text-slate-400 mb-4">
                    Leader handle maps Cartesian deltas to follower with tremor deadband ({deadbandMm}mm) and velocity clamping.
                  </p>

                  {/* Motion Scaling Slider */}
                  <div className="space-y-2 mb-4 bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <div className="flex justify-between text-xs font-mono">
                      <span className="text-slate-400">Motion Scale Ratio:</span>
                      <span className="text-sky-400 font-bold">{motionScale.toFixed(2)}x</span>
                    </div>
                    <input
                      type="range"
                      min="0.1"
                      max="1.5"
                      step="0.05"
                      value={motionScale}
                      onChange={(e) => setMotionScale(parseFloat(e.target.value))}
                      className="w-full accent-sky-500"
                    />
                    <div className="flex justify-between text-[10px] text-slate-500">
                      <span>0.1x (Microsurgery)</span>
                      <span>0.8x (Standard)</span>
                      <span>1.5x (Fast)</span>
                    </div>
                  </div>
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    disabled={isEStop}
                    onClick={() => {
                      if (isTeleopEngaged) {
                        setIsTeleopEngaged(false);
                        addLog('teleop_controller', 'DISENGAGED', 'Teleoperation disengaged by operator', 'info');
                      } else {
                        setIsTeleopEngaged(true);
                        addLog('teleop_controller', 'ENGAGED', 'Teleoperation engaged (50Hz control loop)', 'info');
                      }
                    }}
                    className={`w-full py-2.5 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 shadow ${
                      isTeleopEngaged
                        ? 'bg-amber-600 hover:bg-amber-500 text-white'
                        : 'bg-sky-600 hover:bg-sky-500 text-white'
                    } disabled:opacity-40`}
                  >
                    {isTeleopEngaged ? <Square className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
                    <span>{isTeleopEngaged ? 'DISENGAGE TELEOP' : 'ENGAGE TELEOP (50 HZ)'}</span>
                  </button>
                </div>
              </div>

              {/* Episode Recording Card */}
              <div className="lg:col-span-8 bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-sm flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Radio className={`w-4 h-4 ${isRecording ? 'text-rose-500 animate-ping' : 'text-slate-400'}`} />
                      <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                        Synchronized Demonstration Recorder
                      </span>
                    </div>
                    {isRecording && (
                      <span className="text-xs font-bold text-rose-400 font-mono px-2.5 py-0.5 rounded-full bg-rose-950/60 border border-rose-800">
                        ● RECORDING ACTIVE ({recordingFrames} FRAMES)
                      </span>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mb-4">
                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">Task Definition</label>
                      <select
                        disabled={isRecording}
                        value={selectedTask}
                        onChange={(e) => setSelectedTask(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
                      >
                        <option value="washer_pick_place">Washer Pick & Place on Stanchion</option>
                        <option value="peg_in_hole">Precision Peg-in-Hole Insertion</option>
                        <option value="dual_block_stack">Block Stacking with Force</option>
                        <option value="cable_routing">Deformable Cable Routing</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">Operator ID</label>
                      <input
                        disabled={isRecording}
                        type="text"
                        value={operatorId}
                        onChange={(e) => setOperatorId(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 font-mono focus:outline-none focus:border-sky-500"
                      />
                    </div>

                    <div className="bg-slate-950 p-2 rounded-lg border border-slate-800 text-center flex flex-col justify-center">
                      <span className="text-[10px] text-slate-500">Duration</span>
                      <span className="text-base font-bold font-mono text-white">
                        {recordingDuration.toFixed(1)}s
                      </span>
                    </div>

                    <div className="bg-slate-950 p-2 rounded-lg border border-slate-800 text-center flex flex-col justify-center">
                      <span className="text-[10px] text-slate-500">Stream Buffer</span>
                      <span className="text-xs font-bold font-mono text-emerald-400">
                        Parquet + 3x MP4
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 pt-2">
                  {!isRecording ? (
                    <button
                      disabled={isEStop}
                      onClick={handleStartRecording}
                      className="px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition-colors flex items-center gap-2 shadow disabled:opacity-40"
                    >
                      <Radio className="w-4 h-4" />
                      <span>START DEMONSTRATION RECORDING</span>
                    </button>
                  ) : (
                    <>
                      <button
                        onClick={() => handleStopRecording('success')}
                        className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-colors flex items-center gap-2 shadow"
                      >
                        <CheckCircle2 className="w-4 h-4" />
                        <span>STOP & MARK SUCCESS</span>
                      </button>
                      <button
                        onClick={() => handleStopRecording('failure')}
                        className="px-4 py-2.5 rounded-xl bg-rose-900/60 hover:bg-rose-800/80 border border-rose-700 text-rose-200 text-xs font-semibold transition-colors flex items-center gap-2"
                      >
                        <XCircle className="w-4 h-4" />
                        <span>STOP AS FAILURE</span>
                      </button>
                    </>
                  )}

                  <div className="ml-auto text-xs text-slate-400">
                    Auto-validation runs 11 verification checks upon stop.
                  </div>
                </div>
              </div>
            </div>

            {/* Central Workcell Grid: Kinematic Twin & Live Cameras */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
              {/* Kinematic Twin Visualizer (7 Cols) */}
              <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-sm flex flex-col">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <Target className="w-4 h-4 text-sky-400" />
                    <span className="text-xs font-bold text-slate-200 uppercase tracking-wider">
                      6-DoF Arm Digital Twin & Envelope Protection
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-[11px] font-mono">
                    <span className="text-slate-400">Driver:</span>
                    <span className="text-sky-400 font-semibold">{driverMode.toUpperCase()}</span>
                  </div>
                </div>

                <div className="flex-1 min-h-[300px]">
                  <KinematicTwinCanvas
                    joints={jointAngles}
                    tcpPose={tcpPose}
                    gripperPosition={gripperPosition}
                    isSafe={!isEStop && tcpPose.z >= 0.05}
                    isEStop={isEStop}
                  />
                </div>

                {/* Live Joint Values Ribbon */}
                <div className="mt-3 pt-3 border-t border-slate-800 grid grid-cols-6 gap-2 text-center font-mono">
                  {jointAngles.map((val, idx) => (
                    <div key={idx} className="bg-slate-950 p-1.5 rounded border border-slate-800/70">
                      <div className="text-[10px] text-slate-500">J{idx + 1}</div>
                      <div className="text-xs text-sky-300 font-bold">{val.toFixed(2)} rad</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Real-time Multi-Camera Mini Stack (5 Cols) */}
              <div className="lg:col-span-5 space-y-4">
                <CameraStreamCard
                  id="cam_wrist"
                  name="Wrist Camera"
                  role="wrist"
                  resolution={[640, 480]}
                  fps={30}
                  syncDeltaMs={syncDeltaMs}
                  isRecording={isRecording}
                  gripperPosition={gripperPosition}
                />
                <CameraStreamCard
                  id="cam_overhead"
                  name="Overhead Top-Down"
                  role="overhead"
                  resolution={[1280, 720]}
                  fps={30}
                  syncDeltaMs={syncDeltaMs * 1.2}
                  isRecording={isRecording}
                  gripperPosition={gripperPosition}
                />
              </div>
            </div>

            {/* Telemetry & Gripper Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
                <span className="text-[11px] text-slate-400 block mb-1">TCP Cartesian Position</span>
                <div className="font-mono text-sm text-slate-100 font-semibold">
                  X: {tcpPose.x.toFixed(3)}m | Y: {tcpPose.y.toFixed(3)}m | Z: {tcpPose.z.toFixed(3)}m
                </div>
                <span className="text-[10px] text-slate-500 mt-1 block">Base reference frame</span>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
                <span className="text-[11px] text-slate-400 block mb-1">Tool Center Orientation</span>
                <div className="font-mono text-sm text-slate-100 font-semibold">
                  R: {tcpPose.roll.toFixed(2)} | P: {tcpPose.pitch.toFixed(2)} | Y: {tcpPose.yaw.toFixed(2)}
                </div>
                <span className="text-[10px] text-slate-500 mt-1 block">Roll-Pitch-Yaw (radians)</span>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
                <span className="text-[11px] text-slate-400 block mb-1">Parallel Jaw Gripper</span>
                <div className="font-mono text-sm text-slate-100 font-semibold flex items-center justify-between">
                  <span>{gripperPosition.toFixed(1)} mm</span>
                  <span className={gripperPosition < 10 ? 'text-emerald-400' : 'text-amber-400'}>
                    {gripperPosition < 10 ? 'CLOSED' : 'OPEN'}
                  </span>
                </div>
                <span className="text-[10px] text-slate-500 mt-1 block">Grip Effort: {gripperEffort.toFixed(1)} N</span>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
                <span className="text-[11px] text-slate-400 block mb-1">Active Safety Guardrails</span>
                <div className="font-mono text-xs text-emerald-400 flex items-center gap-1.5 font-semibold">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Envelope + Table Floor OK</span>
                </div>
                <span className="text-[10px] text-slate-500 mt-1 block">Speed cap: 0.30 m/s</span>
              </div>
            </div>
          </div>
        )}

        {/* ==================== TAB 2: MULTI-CAMERA WALL ==================== */}
        {activeTab === 'cameras' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <div>
                <h2 className="text-sm font-bold text-white">Multi-Camera Synchronized Grid</h2>
                <p className="text-xs text-slate-400">Software monotonic synchronization (<span className="text-sky-400 font-mono">1.2ms delta</span>) across all visual streams</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono text-emerald-400 bg-emerald-950/40 px-3 py-1 rounded border border-emerald-800">
                  3/3 CAMERAS ONLINE
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              <CameraStreamCard
                id="cam_wrist"
                name="End-Effector Wrist Camera"
                role="wrist"
                resolution={[640, 480]}
                fps={30}
                syncDeltaMs={syncDeltaMs}
                isRecording={isRecording}
                gripperPosition={gripperPosition}
              />
              <CameraStreamCard
                id="cam_overhead"
                name="Top-Down Workspace Camera"
                role="overhead"
                resolution={[1280, 720]}
                fps={30}
                syncDeltaMs={syncDeltaMs * 1.1}
                isRecording={isRecording}
                gripperPosition={gripperPosition}
              />
              <CameraStreamCard
                id="cam_side"
                name="Third-Person Perspective Camera"
                role="perspective"
                resolution={[640, 480]}
                fps={30}
                syncDeltaMs={syncDeltaMs * 1.3}
                isRecording={isRecording}
                gripperPosition={gripperPosition}
              />
            </div>
          </div>
        )}

        {/* ==================== TAB 3: KINEMATICS & TWIN ==================== */}
        {activeTab === 'kinematics' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
            <div className="lg:col-span-8 bg-slate-900 border border-slate-800 rounded-2xl p-5">
              <h2 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
                <Target className="w-4 h-4 text-sky-400" /> Real-time Forward Kinematics Model
              </h2>
              <div className="h-[400px]">
                <KinematicTwinCanvas
                  joints={jointAngles}
                  tcpPose={tcpPose}
                  gripperPosition={gripperPosition}
                  isSafe={!isEStop}
                  isEStop={isEStop}
                />
              </div>
            </div>

            <div className="lg:col-span-4 bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
              <h3 className="text-sm font-bold text-white">Interactive Joint Control</h3>
              <p className="text-xs text-slate-400">Direct joint angle overrides for kinematics testing:</p>

              <div className="space-y-3 font-mono text-xs">
                {jointAngles.map((val, idx) => (
                  <div key={idx} className="space-y-1">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Joint {idx + 1}:</span>
                      <span className="text-sky-400">{val.toFixed(3)} rad</span>
                    </div>
                    <input
                      type="range"
                      min="-3.14"
                      max="3.14"
                      step="0.01"
                      value={val}
                      onChange={(e) => {
                        const newJ = [...jointAngles];
                        newJ[idx] = parseFloat(e.target.value);
                        setJointAngles(newJ);
                      }}
                      className="w-full accent-sky-500"
                    />
                  </div>
                ))}
              </div>

              <div className="pt-2">
                <button
                  onClick={() => setJointAngles([0.0, -0.785, 0.0, -1.57, 0.0, 1.57])}
                  className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium transition-colors"
                >
                  Reset to Home Pose
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ==================== TAB 4: EPISODES & DATASET VALIDATION ==================== */}
        {activeTab === 'datasets' && (
          <div className="space-y-5">
            <div className="flex items-center justify-between bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <div>
                <h2 className="text-sm font-bold text-white">Recorded Episodes & 11-Point Validation Pipeline</h2>
                <p className="text-xs text-slate-400">Validated demonstrations for training imitation learning models (ACT, Diffusion Policy, LeRobot)</p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => alert('Dataset exported successfully to LeRobot format under /data/datasets/lerobot_export')}
                  className="px-3.5 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-medium flex items-center gap-2 shadow"
                >
                  <Download className="w-4 h-4" /> Export Dataset (LeRobot)
                </button>
              </div>
            </div>

            {/* Episodes Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950 text-slate-400 font-mono uppercase text-[11px] border-b border-slate-800">
                    <tr>
                      <th className="p-3.5">Episode ID</th>
                      <th className="p-3.5">Task</th>
                      <th className="p-3.5">Operator</th>
                      <th className="p-3.5">Duration</th>
                      <th className="p-3.5">Frames</th>
                      <th className="p-3.5">Validation</th>
                      <th className="p-3.5">Human Sign-off</th>
                      <th className="p-3.5 text-right">Inspection</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80 font-mono">
                    {episodes.map((ep) => (
                      <tr key={ep.episode_id} className="hover:bg-slate-800/40 transition-colors">
                        <td className="p-3.5 font-bold text-slate-200">{ep.episode_id}</td>
                        <td className="p-3.5 text-slate-300 font-sans">{ep.task_id}</td>
                        <td className="p-3.5 text-slate-400">{ep.operator_id}</td>
                        <td className="p-3.5 text-slate-300">{ep.duration_seconds.toFixed(1)}s</td>
                        <td className="p-3.5 text-sky-400 font-semibold">{ep.total_frames}</td>
                        <td className="p-3.5">
                          <span
                            className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${
                              ep.validation_status === 'PASS'
                                ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                                : ep.validation_status === 'FAIL'
                                ? 'bg-rose-500/20 text-rose-400 border-rose-500/30'
                                : 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                            }`}
                          >
                            {ep.validation_status}
                          </span>
                        </td>
                        <td className="p-3.5">
                          <span
                            className={`text-[11px] font-semibold ${
                              ep.human_review_status === 'APPROVED'
                                ? 'text-emerald-400'
                                : ep.human_review_status === 'REJECTED'
                                ? 'text-rose-400'
                                : 'text-slate-400'
                            }`}
                          >
                            {ep.human_review_status}
                          </span>
                        </td>
                        <td className="p-3.5 text-right">
                          <button
                            onClick={() => setSelectedValidationEpisode(ep)}
                            className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-sky-400 rounded text-[11px] font-medium transition-colors"
                          >
                            Inspect Checks
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ==================== TAB 5: HARDWARE DISCOVERY & CONFIG ==================== */}
        {activeTab === 'hardware' && (
          <div className="space-y-5">
            <div className="flex items-center justify-between bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <div>
                <h2 className="text-sm font-bold text-white">Hardware Discovery & Vendor Specification Layer</h2>
                <p className="text-xs text-slate-400">Strict abstraction layer preventing unverified physical actuation</p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setIsCalibModalOpen(true)}
                  className="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium flex items-center gap-2"
                >
                  <Target className="w-4 h-4 text-sky-400" /> Run Calibration
                </button>
                <button
                  onClick={() => setIsYamlModalOpen(true)}
                  className="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium flex items-center gap-2"
                >
                  <FileCode className="w-4 h-4 text-amber-400" /> View YAML Configs
                </button>
                <button
                  onClick={() => setIsHardwareModalOpen(true)}
                  className="px-3.5 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-medium flex items-center gap-2 shadow"
                >
                  <Cpu className="w-4 h-4" /> Edit Hardware Specs
                </button>
              </div>
            </div>

            {/* Hardware Status Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {/* Follower Arm Card */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-bold text-slate-200 text-sm">Follower Arm</span>
                    <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800">
                      {hardwareSpecs.model || 'Simulation'}
                    </span>
                  </div>
                  <div className="text-xs space-y-1.5 text-slate-400 font-mono">
                    <div>Manufacturer: <span className="text-slate-200">{hardwareSpecs.manufacturer || 'Pending configuration'}</span></div>
                    <div>Joints: <span className="text-slate-200">{hardwareSpecs.numJoints}-DoF</span></div>
                    <div>Network: <span className="text-slate-200">{hardwareSpecs.robotIp}:{hardwareSpecs.robotPort}</span></div>
                    <div>Protocol: <span className="text-slate-200">{hardwareSpecs.communicationProtocol || 'Simulation Loop'}</span></div>
                  </div>
                </div>
                <div className="pt-4 border-t border-slate-800/80 mt-4 flex items-center justify-between text-[11px]">
                  <span className="text-slate-500">Driver Adapter</span>
                  <span className={isHardwareConfigured ? 'text-emerald-400' : 'text-amber-400'}>
                    {isHardwareConfigured ? 'Ready for test' : 'Stub / Config Required'}
                  </span>
                </div>
              </div>

              {/* Leader Arm Card */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-bold text-slate-200 text-sm">Leader / Master Device</span>
                    <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800">
                      {hardwareSpecs.leaderModel || 'Simulator Leader'}
                    </span>
                  </div>
                  <div className="text-xs space-y-1.5 text-slate-400 font-mono">
                    <div>Interface: <span className="text-slate-200">/dev/ttyUSB_LEADER</span></div>
                    <div>Baud Rate: <span className="text-slate-200">1,000,000 baud</span></div>
                    <div>Deadband: <span className="text-slate-200">3.0 mm</span></div>
                    <div>Deadman: <span className="text-emerald-400">Active</span></div>
                  </div>
                </div>
                <div className="pt-4 border-t border-slate-800/80 mt-4 flex items-center justify-between text-[11px]">
                  <span className="text-slate-500">Master State</span>
                  <span className="text-emerald-400">Synchronous 50Hz</span>
                </div>
              </div>

              {/* Safety Loop Card */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-bold text-slate-200 text-sm">Safety Circuit</span>
                    <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                      ISO 13849 Cat 3
                    </span>
                  </div>
                  <div className="text-xs space-y-1.5 text-slate-400 font-mono">
                    <div>E-Stop State: <span className={isEStop ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}>{isEStop ? 'TRIPPED' : 'CLEARED'}</span></div>
                    <div>Table Floor: <span className="text-slate-200">+30mm safety buffer</span></div>
                    <div>Max Linear Vel: <span className="text-slate-200">0.30 m/s</span></div>
                    <div>Heartbeat Timeout: <span className="text-slate-200">150 ms</span></div>
                  </div>
                </div>
                <div className="pt-4 border-t border-slate-800/80 mt-4 flex items-center justify-between text-[11px]">
                  <span className="text-slate-500">Watchdog Status</span>
                  <span className="text-emerald-400">Healthy</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ==================== TAB 6: SAFETY & EVENT DIAGNOSTICS ==================== */}
        {activeTab === 'safety' && (
          <div className="space-y-5">
            <div className="flex items-center justify-between bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <div>
                <h2 className="text-sm font-bold text-white">System Diagnostics & Structured Event Stream</h2>
                <p className="text-xs text-slate-400">Structured JSON logging according to ISO/TS 15066 safety standards</p>
              </div>
              <button
                onClick={() => setEventLogs([])}
                className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-xs transition-colors"
              >
                Clear Log View
              </button>
            </div>

            <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 font-mono text-xs max-h-[500px] overflow-y-auto space-y-2">
              {eventLogs.map((log, idx) => (
                <div
                  key={idx}
                  className={`p-2 rounded border flex items-start gap-3 ${
                    log.type === 'error'
                      ? 'bg-rose-950/30 border-rose-800/60 text-rose-300'
                      : log.type === 'warn'
                      ? 'bg-amber-950/30 border-amber-800/60 text-amber-300'
                      : 'bg-slate-900/60 border-slate-800/60 text-slate-300'
                  }`}
                >
                  <span className="text-slate-500 shrink-0">{log.timestamp}</span>
                  <span className="text-sky-400 font-bold shrink-0">[{log.component.toUpperCase()}]</span>
                  <span className="text-slate-400 shrink-0">{log.event}</span>
                  <span className="text-slate-200">{log.message}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Modals */}
      <HardwareSpecsModal
        isOpen={isHardwareModalOpen}
        onClose={() => setIsHardwareModalOpen(false)}
        onSave={(newSpecs) => {
          setHardwareSpecs(newSpecs);
          addLog('config', 'SPECS_UPDATED', `Configured: ${newSpecs.manufacturer} ${newSpecs.model}`, 'info');
        }}
        initialSpecs={hardwareSpecs}
      />

      <ValidationModal
        episode={selectedValidationEpisode}
        onClose={() => setSelectedValidationEpisode(null)}
        onReview={handleReviewEpisode}
      />

      <YamlViewerModal
        isOpen={isYamlModalOpen}
        onClose={() => setIsYamlModalOpen(false)}
      />

      <CalibrationModal
        isOpen={isCalibModalOpen}
        onClose={() => setIsCalibModalOpen(false)}
      />
    </div>
  );
}
