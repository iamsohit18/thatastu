import React, { useEffect, useRef } from 'react';
import { CartesianPose, JointState } from '../types/robotics';

interface KinematicTwinCanvasProps {
  joints: number[];
  tcpPose: CartesianPose;
  gripperPosition: number;
  isSafe: boolean;
  isEStop: boolean;
}

export const KinematicTwinCanvas: React.FC<KinematicTwinCanvasProps> = ({
  joints,
  tcpPose,
  gripperPosition,
  isSafe,
  isEStop,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;

    const render = () => {
      const width = canvas.width;
      const height = canvas.height;

      // Dark industrial grid background
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, width, height);

      // Draw coordinate grid
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 1;
      const step = 30;
      for (let x = 0; x < width; x += step) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += step) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Base pedestal coordinates
      const baseX = width * 0.45;
      const baseY = height * 0.72;

      // Draw Table Surface (Safety Floor)
      ctx.fillStyle = '#334155';
      ctx.fillRect(baseX - 220, baseY + 4, 440, 16);
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 2;
      ctx.strokeRect(baseX - 220, baseY + 4, 440, 16);

      // Table floor warning line (Z = 0.03m margin)
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = '#eab308';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(baseX - 210, baseY - 12);
      ctx.lineTo(baseX + 210, baseY - 12);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#eab308';
      ctx.font = '10px monospace';
      ctx.fillText('TABLE SAFETY FLOOR (+30mm)', baseX - 200, baseY - 16);

      // Draw Robot Base
      ctx.fillStyle = '#1e293b';
      ctx.strokeStyle = isEStop ? '#ef4444' : isSafe ? '#0284c7' : '#f59e0b';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.roundRect(baseX - 35, baseY - 15, 70, 20, [6, 6, 0, 0]);
      ctx.fill();
      ctx.stroke();

      // Kinematic forward projection for visual simulation
      // Links lengths in pixels
      const link1 = 65;
      const link2 = 70;
      const link3 = 55;
      const link4 = 30;

      const q0 = joints[0] || 0; // base yaw (subtle side perspective offset)
      const q1 = (joints[1] || -0.785) - Math.PI / 2; // shoulder pitch
      const q2 = joints[2] || 0;
      const q3 = (joints[3] || -1.57); // elbow pitch
      const q4 = joints[4] || 0;
      const q5 = joints[5] || 1.57; // wrist pitch

      // Joint 1: Base pivot
      const j1X = baseX + Math.sin(q0) * 15;
      const j1Y = baseY - 15;

      // Joint 2: Shoulder
      const j2X = j1X;
      const j2Y = j1Y - 20;

      // Joint 3: Elbow
      const angle1 = q1 + q2 * 0.2;
      const j3X = j2X + Math.cos(angle1) * link1;
      const j3Y = j2Y + Math.sin(angle1) * link1;

      // Joint 4: Forearm
      const angle2 = angle1 + q3 + q4 * 0.2;
      const j4X = j3X + Math.cos(angle2) * link2;
      const j4Y = j3Y + Math.sin(angle2) * link2;

      // Joint 5: Wrist
      const angle3 = angle2 + q5 * 0.6;
      const j5X = j4X + Math.cos(angle3) * link3;
      const j5Y = j4Y + Math.sin(angle3) * link3;

      // TCP End-effector
      const tcpX = j5X + Math.cos(angle3) * link4;
      const tcpY = j5Y + Math.sin(angle3) * link4;

      // Draw link segments
      const drawLink = (x1: number, y1: number, x2: number, y2: number, color: string, w: number) => {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = color;
        ctx.lineWidth = w;
        ctx.lineCap = 'round';
        ctx.stroke();
      };

      const linkColor = isEStop ? '#ef4444' : '#38bdf8';
      const jointColor = '#f8fafc';

      // Draw Arm Links
      drawLink(j1X, j1Y, j2X, j2Y, '#64748b', 16);
      drawLink(j2X, j2Y, j3X, j3Y, linkColor, 14);
      drawLink(j3X, j3Y, j4X, j4Y, linkColor, 10);
      drawLink(j4X, j4Y, j5X, j5Y, '#94a3b8', 8);
      drawLink(j5X, j5Y, tcpX, tcpY, '#cbd5e1', 6);

      // Draw Joint Knuckles
      const drawJoint = (x: number, y: number, r: number) => {
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fillStyle = jointColor;
        ctx.fill();
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 2;
        ctx.stroke();
      };

      drawJoint(j2X, j2Y, 7);
      drawJoint(j3X, j3Y, 6);
      drawJoint(j4X, j4Y, 5);
      drawJoint(j5X, j5Y, 4);

      // Draw Gripper Jaws
      const gripAngle = angle3 + Math.PI / 2;
      const halfAperture = (gripperPosition / 85.0) * 12 + 2; // scaled aperture

      const jaw1X = tcpX + Math.cos(gripAngle) * halfAperture;
      const jaw1Y = tcpY + Math.sin(gripAngle) * halfAperture;
      const jaw2X = tcpX - Math.cos(gripAngle) * halfAperture;
      const jaw2Y = tcpY - Math.sin(gripAngle) * halfAperture;

      ctx.fillStyle = gripperPosition < 10 ? '#22c55e' : '#f59e0b';
      ctx.beginPath();
      ctx.arc(tcpX, tcpY, 4, 0, Math.PI * 2);
      ctx.fill();

      // Gripper fingers
      ctx.strokeStyle = '#f8fafc';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(tcpX, tcpY);
      ctx.lineTo(jaw1X, jaw1Y);
      ctx.lineTo(jaw1X + Math.cos(angle3) * 14, jaw1Y + Math.sin(angle3) * 14);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(tcpX, tcpY);
      ctx.lineTo(jaw2X, jaw2Y);
      ctx.lineTo(jaw2X + Math.cos(angle3) * 14, jaw2Y + Math.sin(angle3) * 14);
      ctx.stroke();

      // Tool Center Point Reticle
      ctx.strokeStyle = '#ec4899';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(tcpX, tcpY, 10, 0, Math.PI * 2);
      ctx.stroke();

      // Overlay text
      ctx.fillStyle = '#94a3b8';
      ctx.font = '11px monospace';
      ctx.fillText(`TCP: [X: ${tcpPose.x.toFixed(3)}m, Y: ${tcpPose.y.toFixed(3)}m, Z: ${tcpPose.z.toFixed(3)}m]`, 14, 20);
      ctx.fillText(`Orientation: [R: ${tcpPose.roll.toFixed(2)}, P: ${tcpPose.pitch.toFixed(2)}, Y: ${tcpPose.yaw.toFixed(2)}]`, 14, 36);
      ctx.fillText(`Gripper Aperture: ${gripperPosition.toFixed(1)}mm (${gripperPosition < 10 ? 'CLOSED' : 'OPEN'})`, 14, 52);

      // Status watermark
      ctx.fillStyle = isEStop ? '#ef4444' : isSafe ? '#22c55e' : '#f59e0b';
      ctx.font = 'bold 12px monospace';
      ctx.fillText(isEStop ? '● HARDWARE E-STOP ENGAGED' : isSafe ? '● NOMINAL KINEMATICS' : '▲ SAFETY BOUNDARY WARNING', width - 260, 20);
    };

    render();
  }, [joints, tcpPose, gripperPosition, isSafe, isEStop]);

  return (
    <div className="relative w-full h-full bg-slate-950 rounded-xl overflow-hidden border border-slate-800 shadow-inner">
      <canvas
        ref={canvasRef}
        width={640}
        height={340}
        className="w-full h-full object-contain block"
      />
      <div className="absolute bottom-2 right-3 flex items-center gap-3 text-xs font-mono text-slate-400 bg-slate-900/80 px-2.5 py-1 rounded border border-slate-700/60">
        <span>6-DoF Forward Kinematics</span>
        <span>|</span>
        <span className="text-sky-400">50 Hz Digital Twin</span>
      </div>
    </div>
  );
};
