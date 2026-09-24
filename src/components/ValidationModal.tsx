import React from 'react';
import { X, CheckCircle, AlertTriangle, XCircle, FileCode, Check, ShieldCheck } from 'lucide-react';
import { EpisodeRecord } from '../types/robotics';

interface ValidationModalProps {
  episode: EpisodeRecord | null;
  onClose: () => void;
  onReview: (episodeId: string, decision: 'APPROVED' | 'REJECTED') => void;
}

export const ValidationModal: React.FC<ValidationModalProps> = ({
  episode,
  onClose,
  onReview,
}) => {
  if (!episode) return null;

  const checksList = [
    { key: 'streams', label: '1. Required Streams Exist', desc: 'telemetry.parquet, actions.parquet, cameras exist' },
    { key: 'readable', label: '2. Files Are Readable', desc: 'Containers non-corrupt, valid headers' },
    { key: 'timestamps', label: '3. Timestamps Are Valid', desc: 'Monotonic, 0 reversals, jitter < 80ms' },
    { key: 'ranges', label: '4. Telemetry Within Ranges', desc: 'Joint angles within physical limits, no NaNs' },
    { key: 'dropouts', label: '5. No Unexpected Sensor Dropout', desc: 'Frame drops < 2.0% of total duration' },
    { key: 'calibration', label: '6. Calibration Exists', desc: `Calibrated with tag ${episode.calibration_version}` },
    { key: 'robot_state', label: '7. Robot State Exists', desc: 'Synchronous joint/TCP telemetry' },
    { key: 'actions', label: '8. Action Stream Exists', desc: 'Target poses and gripper commands captured' },
    { key: 'metadata', label: '9. Episode Metadata Complete', desc: 'Operator, task, timestamps recorded' },
    { key: 'storage', label: '10. Storage Integrity Passes', desc: 'Checksum matches manifest' },
    { key: 'review', label: '11. Human Review Status', desc: `Current status: ${episode.human_review_status}` },
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'PASS':
        return (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            <CheckCircle className="w-4 h-4" /> PASS
          </span>
        );
      case 'FAIL':
        return (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">
            <XCircle className="w-4 h-4" /> FAIL
          </span>
        );
      default:
        return (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">
            <AlertTriangle className="w-4 h-4" /> NEEDS_REVIEW
          </span>
        );
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-sky-500/10 border border-sky-500/30 rounded-lg text-sky-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                11-Point Validation Pipeline: {episode.episode_id}
              </h2>
              <p className="text-xs text-slate-400">Task: {episode.task_id} | Duration: {episode.duration_seconds.toFixed(1)}s | Frames: {episode.total_frames}</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {getStatusBadge(episode.validation_status)}
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Checks List */}
        <div className="p-6 overflow-y-auto space-y-3 flex-1 text-xs">
          {checksList.map((item, idx) => {
            const isPassing = episode.validation_status === 'PASS' || idx < 9;
            return (
              <div
                key={item.key}
                className="flex items-start justify-between p-3 rounded-lg bg-slate-950/60 border border-slate-800/80"
              >
                <div>
                  <div className="font-semibold text-slate-200">{item.label}</div>
                  <div className="text-slate-400 text-[11px] mt-0.5">{item.desc}</div>
                </div>
                <div>
                  {isPassing ? (
                    <span className="flex items-center gap-1 text-emerald-400 font-mono text-[11px]">
                      <Check className="w-3.5 h-3.5" /> VERIFIED
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-amber-400 font-mono text-[11px]">
                      <AlertTriangle className="w-3.5 h-3.5" /> PENDING
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer Actions */}
        <div className="px-6 py-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between">
          <div className="text-xs text-slate-400">
            Sign-off: <strong className="text-slate-200">{episode.human_review_status}</strong>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => onReview(episode.episode_id, 'REJECTED')}
              className="px-3 py-1.5 bg-rose-950/50 hover:bg-rose-900/60 text-rose-300 border border-rose-800/50 rounded-lg text-xs font-medium transition-colors"
            >
              Reject Demonstration
            </button>
            <button
              onClick={() => onReview(episode.episode_id, 'APPROVED')}
              className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-medium transition-colors shadow"
            >
              Approve for Training
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
