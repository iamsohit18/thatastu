"""Action stream writer for commands issued during demonstration."""
import os
import json
from typing import List, Dict, Any
from src.common.models import TeleopAction

try:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    HAS_PARQUET = True
except ImportError:
    HAS_PARQUET = False


class ActionWriter:
    """Streams commanded actions (target poses, joints, gripper) to disk."""

    def __init__(self, output_file: str, format_type: str = "parquet"):
        self.output_file = output_file
        self.format_type = format_type
        self.buffer: List[Dict[str, Any]] = []

    def write_action(self, action: TeleopAction) -> None:
        flat_record = {
            "timestamp": action.timestamp,
            "sequence_number": action.sequence_number,
            "command_mode": action.command_mode,
            "target_tcp_x": action.target_tcp_pose.x if action.target_tcp_pose else None,
            "target_tcp_y": action.target_tcp_pose.y if action.target_tcp_pose else None,
            "target_tcp_z": action.target_tcp_pose.z if action.target_tcp_pose else None,
            "target_tcp_roll": action.target_tcp_pose.roll if action.target_tcp_pose else None,
            "target_tcp_pitch": action.target_tcp_pose.pitch if action.target_tcp_pose else None,
            "target_tcp_yaw": action.target_tcp_pose.yaw if action.target_tcp_pose else None,
            "target_gripper_position": action.target_gripper_position,
        }
        self.buffer.append(flat_record)

    def close(self) -> None:
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        if HAS_PARQUET and self.format_type == "parquet":
            df = pd.DataFrame(self.buffer)
            table = pa.Table.from_pandas(df)
            pq.write_table(table, self.output_file)
        else:
            jsonl_file = self.output_file.replace(".parquet", ".jsonl")
            with open(jsonl_file, "w", encoding="utf-8") as f:
                for row in self.buffer:
                    f.write(json.dumps(row) + "\n")
