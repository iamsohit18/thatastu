import React, { useState } from 'react';
import { X, Copy, Check, Cpu, ShieldAlert, FileText, Send } from 'lucide-react';
import { HardwareSpecForm } from '../types/robotics';

interface HardwareSpecsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (specs: HardwareSpecForm) => void;
  initialSpecs: HardwareSpecForm;
}

export const HardwareSpecsModal: React.FC<HardwareSpecsModalProps> = ({
  isOpen,
  onClose,
  onSave,
  initialSpecs,
}) => {
  const [specs, setSpecs] = useState<HardwareSpecForm>(initialSpecs);
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const generateQuestionnaireText = () => {
    return `Robot manufacturer: ${specs.manufacturer || '[PLEASE SPECIFY]'}
Robot model: ${specs.model || '[PLEASE SPECIFY]'}
Robot controller: ${specs.controller || '[PLEASE SPECIFY]'}
Number of joints: ${specs.numJoints}
End effector/gripper: ${specs.gripper || '[PLEASE SPECIFY]'}
Leader/master model: ${specs.leaderModel || '[PLEASE SPECIFY]'}
Follower model: ${specs.followerModel || '[PLEASE SPECIFY]'}
Camera models: ${specs.cameraModels || '[PLEASE SPECIFY]'}
Computer: ${specs.computer || '[PLEASE SPECIFY]'}
Operating system: ${specs.os || 'Ubuntu 22.04 LTS'}
CPU: ${specs.cpu || '[PLEASE SPECIFY]'}
GPU: ${specs.gpu || '[PLEASE SPECIFY]'}
RAM: ${specs.ram || '[PLEASE SPECIFY]'}
Network interface: ${specs.networkInterface || 'eth0 (isolated subnet)'}
Robot IP: ${specs.robotIp || '192.168.1.100'}
Robot port: ${specs.robotPort}
Communication protocol: ${specs.communicationProtocol || '[PLEASE SPECIFY]'}
SDK name/version: ${specs.sdkVersion || '[PLEASE SPECIFY]'}
ROS 2 version: ${specs.ros2Version || 'Humble Hawksbill'}
ROS 2 driver/package: ${specs.ros2Driver || '[PLEASE SPECIFY]'}
Required firmware: ${specs.firmware || '[PLEASE SPECIFY]'}
Safety/E-stop architecture: ${specs.estopArchitecture || 'Dual-channel Category 3 E-stop circuit'}`;
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generateQuestionnaireText());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-3xl rounded-2xl shadow-2xl overflow-hidden my-8 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Hardware Information Specification</h2>
              <p className="text-xs text-slate-400">Required before activating vendor-specific physical robot adapters</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Warning Banner */}
        <div className="bg-amber-950/40 border-b border-amber-800/40 px-6 py-3 text-xs text-amber-300 flex items-start gap-2.5">
          <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5" />
          <span>
            <strong>Safety Mandate:</strong> The platform abstraction layer keeps vendor code decoupled. Physical actuation code is held in stub mode until exact manufacturer parameters, register maps, and safety loops are verified.
          </span>
        </div>

        {/* Body Form */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-xs">
          {/* Section: Robotic Follower Arm */}
          <div>
            <h3 className="text-sm font-semibold text-sky-400 mb-3 flex items-center gap-2">
              <Cpu className="w-4 h-4" /> Follower Arm & Controller
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="block text-slate-300 mb-1">Robot Manufacturer</label>
                <input
                  type="text"
                  placeholder="e.g. Franka Emika, UR, Kinova"
                  value={specs.manufacturer}
                  onChange={(e) => setSpecs({ ...specs, manufacturer: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">Robot Model</label>
                <input
                  type="text"
                  placeholder="e.g. FR3, UR5e, Gen3"
                  value={specs.model}
                  onChange={(e) => setSpecs({ ...specs, model: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">Controller Model</label>
                <input
                  type="text"
                  placeholder="e.g. Control Box CB3/e-Series"
                  value={specs.controller}
                  onChange={(e) => setSpecs({ ...specs, controller: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">Number of Joints (DoF)</label>
                <input
                  type="number"
                  value={specs.numJoints}
                  onChange={(e) => setSpecs({ ...specs, numJoints: parseInt(e.target.value) || 6 })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">End Effector / Gripper</label>
                <input
                  type="text"
                  placeholder="e.g. Robotiq 2F-85, OnRobot RG2"
                  value={specs.gripper}
                  onChange={(e) => setSpecs({ ...specs, gripper: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">Firmware Version</label>
                <input
                  type="text"
                  placeholder="e.g. PolyScope 5.14 / v4.2.1"
                  value={specs.firmware}
                  onChange={(e) => setSpecs({ ...specs, firmware: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>
          </div>

          {/* Section: Master/Leader & Cameras */}
          <div>
            <h3 className="text-sm font-semibold text-sky-400 mb-3">Teleoperation Master & Vision</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-300 mb-1">Leader / Master Model</label>
                <input
                  type="text"
                  placeholder="e.g. GELLO, Aloha Master, Haply"
                  value={specs.leaderModel}
                  onChange={(e) => setSpecs({ ...specs, leaderModel: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">Camera Models</label>
                <input
                  type="text"
                  placeholder="e.g. 2x Intel RealSense D435i + 1x D405"
                  value={specs.cameraModels}
                  onChange={(e) => setSpecs({ ...specs, cameraModels: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>
          </div>

          {/* Section: Network & Protocol */}
          <div>
            <h3 className="text-sm font-semibold text-sky-400 mb-3">Network & Communication Protocol</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div>
                <label className="block text-slate-300 mb-1">Robot IP Address</label>
                <input
                  type="text"
                  value={specs.robotIp}
                  onChange={(e) => setSpecs({ ...specs, robotIp: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 font-mono focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">Port</label>
                <input
                  type="number"
                  value={specs.robotPort}
                  onChange={(e) => setSpecs({ ...specs, robotPort: parseInt(e.target.value) || 30003 })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 font-mono focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">Communication Protocol</label>
                <input
                  type="text"
                  placeholder="e.g. RTDE, FCI UDP, Modbus"
                  value={specs.communicationProtocol}
                  onChange={(e) => setSpecs({ ...specs, communicationProtocol: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-slate-300 mb-1">ROS 2 Version</label>
                <input
                  type="text"
                  value={specs.ros2Version}
                  onChange={(e) => setSpecs({ ...specs, ros2Version: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>
          </div>

          {/* Section: Safety & E-Stop */}
          <div>
            <h3 className="text-sm font-semibold text-sky-400 mb-3">Safety & E-Stop Architecture</h3>
            <div>
              <label className="block text-slate-300 mb-1">Safety / E-Stop Circuit Specification</label>
              <textarea
                rows={2}
                value={specs.estopArchitecture}
                onChange={(e) => setSpecs({ ...specs, estopArchitecture: e.target.value })}
                className="w-full bg-slate-950 border border-slate-700 rounded px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>
        </div>

        {/* Footer actions */}
        <div className="px-6 py-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between">
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium transition-colors border border-slate-700"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            {copied ? 'Copied Questionnaire' : 'Copy Questionnaire for Prompt'}
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium transition-colors"
            >
              Close
            </button>
            <button
              onClick={() => {
                onSave(specs);
                onClose();
              }}
              className="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-medium transition-colors shadow"
            >
              Save Configuration
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
