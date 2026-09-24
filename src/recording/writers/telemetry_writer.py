"""Parquet and JSONL telemetry stream writer."""
import os
import json
from typing import List, Dict, Any
from src.common.models import RobotTelemetry

try:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    HAS_PARQUET = True
except ImportError:
    HAS_PARQUET = False


class TelemetryWriter:
    """Streams robot joint, Cartesian, and gripper observations to disk."""

    def __init__(self, output_file: str, format_type: str = "parquet"):
        self.output_file = output_file
        self.format_type = format_type
        self.buffer: List[Dict[str, Any]] = []

    def write_sample(self, telemetry: RobotTelemetry) -> None:
        flat_record = {
            "timestamp": telemetry.timestamp,
            "monotonic_ns": telemetry.monotonic_timestamp_ns,
            "sequence_number": telemetry.sequence_number,
            "joint_positions": telemetry.joint_state.positions,
            "joint_velocities": telemetry.joint_state.velocities,
            "joint_torques": telemetry.joint_state.torques,
            "tcp_x": telemetry.tcp_pose.x,
            "tcp_y": telemetry.tcp_pose.y,
            "tcp_z": telemetry.tcp_pose.z,
            "tcp_roll": telemetry.tcp_pose.roll,
            "tcp_pitch": telemetry.tcp_pose.pitch,
            "tcp_yaw": telemetry.tcp_pose.yaw,
            "gripper_position": telemetry.gripper_state.position,
            "gripper_effort": telemetry.gripper_state.effort,
            "is_safe": telemetry.is_safe,
        }
        self.buffer.append(flat_record)

    def close(self) -> None:
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        if HAS_PARQUET and self.format_type == "parquet":
            df = pd.DataFrame(self.buffer)
            table = pa.Table.from_pandas(df)
            pq.write_table(table, self.output_file)
        else:
            # Fallback JSONL output
            jsonl_file = self.output_file.replace(".parquet", ".jsonl")
            with open(jsonl_file, "w", encoding="utf-8") as f:
                for row in self.buffer:
                    f.write(json.dumps(row) + "\n")
