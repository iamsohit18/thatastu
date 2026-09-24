import React, { useState } from 'react';
import { X, Target, CheckCircle2, RotateCcw, Sliders, ShieldCheck } from 'lucide-react';

interface CalibrationModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CalibrationModal: React.FC<CalibrationModalProps> = ({ isOpen, onClose }) => {
  const [step, setStep] = useState<number>(1);
  const [calibrating, setCalibrating] = useState<boolean>(false);
  const [calibId, setCalibId] = useState<string>('CAL_20260924_01');

  if (!isOpen) return null;

  const handleRunStep = (stepNum: number) => {
    setCalibrating(true);
    setTimeout(() => {
      setCalibrating(false);
      setStep(stepNum + 1);
    }, 1200);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-xl rounded-2xl shadow-2xl overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <Target className="w-5 h-5 text-sky-400" />
            <div>
              <h2 className="text-base font-bold text-white">Workcell & Device Calibration</h2>
              <p className="text-xs text-slate-400">Zero-offset reference, gripper stroke, and table safety planes</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4 text-xs">
          {/* Step 1: Master Zero Reference */}
          <div className={`p-4 rounded-xl border transition-all ${step === 1 ? 'border-sky-500 bg-sky-950/20' : step > 1 ? 'border-emerald-500/40 bg-emerald-950/10' : 'border-slate-800 bg-slate-950/50'}`}>
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-sm text-slate-200">1. Master Zero Reference Alignment</span>
              {step > 1 && <span className="text-emerald-400 font-mono flex items-center gap-1"><CheckCircle2 className="w-4 h-4" /> CALIBRATED</span>}
            </div>
            <p className="text-slate-400 mb-3">Position the master handle into the mechanical zero fixture to zero joint encoders.</p>
            {step === 1 && (
              <button
                disabled={calibrating}
                onClick={() => handleRunStep(1)}
                className="px-3.5 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded font-medium disabled:opacity-50 flex items-center gap-2"
              >
                {calibrating ? <RotateCcw className="w-3.5 h-3.5 animate-spin" /> : null}
                {calibrating ? 'Zeroing Encoders...' : 'Record Zero Reference'}
              </button>
            )}
          </div>

          {/* Step 2: Gripper Stroke */}
          <div className={`p-4 rounded-xl border transition-all ${step === 2 ? 'border-sky-500 bg-sky-950/20' : step > 2 ? 'border-emerald-500/40 bg-emerald-950/10' : 'border-slate-800 bg-slate-950/50'}`}>
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-sm text-slate-200">2. Gripper Full-Stroke Mapping</span>
              {step > 2 && <span className="text-emerald-400 font-mono flex items-center gap-1"><CheckCircle2 className="w-4 h-4" /> CALIBRATED</span>}
            </div>
            <p className="text-slate-400 mb-3">Cycles opening to 85.0mm and closed contact 0.0mm to map analog triggers.</p>
            {step === 2 && (
              <button
                disabled={calibrating}
                onClick={() => handleRunStep(2)}
                className="px-3.5 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded font-medium disabled:opacity-50 flex items-center gap-2"
              >
                {calibrating ? <RotateCcw className="w-3.5 h-3.5 animate-spin" /> : null}
                {calibrating ? 'Cycling Gripper...' : 'Run Gripper Calibration'}
              </button>
            )}
          </div>

          {/* Step 3: Workspace Bounds */}
          <div className={`p-4 rounded-xl border transition-all ${step >= 3 ? 'border-emerald-500/40 bg-emerald-950/10' : 'border-slate-800 bg-slate-950/50'}`}>
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-sm text-slate-200">3. Workspace Envelopes & Table Floor</span>
              {step >= 3 && <span className="text-emerald-400 font-mono flex items-center gap-1"><CheckCircle2 className="w-4 h-4" /> ACTIVE</span>}
            </div>
            <p className="text-slate-400">
              Active Envelope: X: [-0.65, 0.65]m, Y: [0.25, 0.80]m, Z: [0.03, 0.70]m. Table safety floor margin: 30mm.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between">
          <span className="text-xs text-slate-400 font-mono">Active Tag: {calibId}</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};
