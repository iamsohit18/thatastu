import React, { useEffect, useRef } from 'react';
import { Camera, RefreshCw, Radio, CheckCircle, AlertTriangle } from 'lucide-react';

interface CameraStreamCardProps {
  id: string;
  name: string;
  role: 'wrist' | 'overhead' | 'perspective';
  resolution: [number, number];
  fps: number;
  syncDeltaMs: number;
  isRecording: boolean;
  gripperPosition: number;
}

export const CameraStreamCard: React.FC<CameraStreamCardProps> = ({
  id,
  name,
  role,
  resolution,
  fps,
  syncDeltaMs,
  isRecording,
  gripperPosition,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let frameId: number;
    let frameNum = 0;

    const render = () => {
      frameNum++;
      const w = canvas.width;
      const h = canvas.height;

      // Realistic camera sensor simulation canvas
      ctx.fillStyle = '#0b0f19';
      ctx.fillRect(0, 0, w, h);

      // Render camera views according to role
      if (role === 'wrist') {
        // Looking down through gripper jaws onto workbench
        const cx = w / 2;
        const cy = h / 2;

        // Worktable texture
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(0, 0, w, h);

        // Circular target disc / bolt
        ctx.beginPath();
        ctx.arc(cx, cy, 32, 0, Math.PI * 2);
        ctx.fillStyle = '#334155';
        ctx.fill();
        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(cx, cy, 14, 0, Math.PI * 2);
        ctx.fillStyle = '#0f172a';
        ctx.fill();

        // Moving Gripper fingers from top perspective
        const jawDist = (gripperPosition / 85.0) * 55 + 10;
        ctx.fillStyle = '#475569';
        ctx.fillRect(cx - jawDist - 18, cy - 35, 18, 70);
        ctx.fillRect(cx + jawDist, cy - 35, 18, 70);

        ctx.strokeStyle = '#94a3b8';
        ctx.strokeRect(cx - jawDist - 18, cy - 35, 18, 70);
        ctx.strokeRect(cx + jawDist, cy - 35, 18, 70);

        // Crosshairs
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(cx - 20, cy);
        ctx.lineTo(cx + 20, cy);
        ctx.moveTo(cx, cy - 20);
        ctx.lineTo(cx, cy + 20);
        ctx.stroke();
      } else if (role === 'overhead') {
        // Overhead top-down view of workcell
        ctx.fillStyle = '#111827';
        ctx.fillRect(0, 0, w, h);

        // Grid lines on mat
        ctx.strokeStyle = '#1f2937';
        ctx.lineWidth = 1;
        for (let x = 20; x < w; x += 30) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, h);
          ctx.stroke();
        }
        for (let y = 20; y < h; y += 30) {
          ctx.beginPath();
          ctx.moveTo(0, y);
          ctx.lineTo(w, y);
          ctx.stroke();
        }

        // Object fixture 1: Peg stand
        ctx.fillStyle = '#3b82f6';
        ctx.fillRect(w * 0.35, h * 0.4, 40, 40);
        ctx.strokeStyle = '#60a5fa';
        ctx.strokeRect(w * 0.35, h * 0.4, 40, 40);

        // Object fixture 2: Cup / bin
        ctx.fillStyle = '#10b981';
        ctx.beginPath();
        ctx.arc(w * 0.65, h * 0.45, 24, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#34d399';
        ctx.stroke();

        // Robot base shadow
        ctx.fillStyle = '#374151';
        ctx.beginPath();
        ctx.arc(w * 0.5, h * 0.85, 30, 0, Math.PI * 2);
        ctx.fill();
      } else {
        // Perspective third-person side view
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, w, h);

        // Laboratory table edge
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(0, h * 0.6, w, h * 0.4);
        ctx.strokeStyle = '#334155';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, h * 0.6);
        ctx.lineTo(w, h * 0.6);
        ctx.stroke();

        // Arm silhouette
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(w * 0.25, h * 0.6);
        ctx.lineTo(w * 0.35, h * 0.35);
        ctx.lineTo(w * 0.55, h * 0.45);
        ctx.lineTo(w * 0.62, h * 0.55);
        ctx.stroke();
      }

      // Timecode overlay
      const now = new Date();
      const timeStr = `${now.toISOString().substring(11, 23)} UTC`;
      ctx.fillStyle = '#000000aa';
      ctx.fillRect(8, h - 26, 210, 18);
      ctx.fillStyle = '#22c55e';
      ctx.font = '10px monospace';
      ctx.fillText(`${timeStr} | F#${frameNum}`, 14, h - 13);

      frameId = requestAnimationFrame(render);
    };

    render();
    return () => cancelAnimationFrame(frameId);
  }, [role, gripperPosition]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg flex flex-col">
      {/* Header */}
      <div className="px-3.5 py-2 bg-slate-950 border-b border-slate-800 flex items-center justify-between text-xs">
        <div className="flex items-center gap-2">
          <Camera className="w-3.5 h-3.5 text-sky-400" />
          <span className="font-semibold text-slate-200">{name}</span>
          <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
            {role}
          </span>
        </div>
        <div className="flex items-center gap-2">
          {isRecording ? (
            <span className="flex items-center gap-1 text-[11px] font-bold text-rose-400 animate-pulse">
              <Radio className="w-3 h-3" /> REC
            </span>
          ) : (
            <span className="flex items-center gap-1 text-[11px] font-mono text-emerald-400">
              <CheckCircle className="w-3 h-3" /> ACTIVE
            </span>
          )}
        </div>
      </div>

      {/* Stream Canvas */}
      <div className="relative aspect-video w-full bg-black">
        <canvas ref={canvasRef} width={360} height={202} className="w-full h-full object-cover block" />
        <div className="absolute top-2 left-2 flex items-center gap-1.5 bg-black/70 px-2 py-0.5 rounded text-[10px] font-mono text-slate-300">
          <span className="text-emerald-400">● LIVE</span>
          <span>{resolution[0]}x{resolution[1]}</span>
          <span>@{fps}fps</span>
        </div>
        <div className="absolute top-2 right-2 flex items-center gap-1 bg-black/70 px-2 py-0.5 rounded text-[10px] font-mono">
          <span className="text-slate-400">Sync Δ:</span>
          <span className={syncDeltaMs > 30 ? 'text-rose-400 font-bold' : 'text-sky-300'}>
            {syncDeltaMs.toFixed(1)}ms
          </span>
        </div>
      </div>

      {/* Footer Info */}
      <div className="px-3 py-1.5 bg-slate-950/70 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
        <span>Device: {id}</span>
        <span>Driver: OpenCV / V4L2</span>
      </div>
    </div>
  );
};
