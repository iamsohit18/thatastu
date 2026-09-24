"""Video stream readability, frame count, and corruption validator."""
import os
from typing import List, Tuple

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    cv2 = None
    HAS_CV2 = False


class VideoValidator:
    """Verifies recorded camera video files exist, are readable, and match expected frame count."""

    def validate_video_file(self, video_path: str, expected_min_frames: int = 10) -> Tuple[bool, List[str]]:
        reasons = []
        if not os.path.exists(video_path):
            return False, [f"Video file missing: {video_path}"]

        file_size = os.path.getsize(video_path)
        if file_size == 0:
            return False, [f"Video file is 0 bytes: {video_path}"]

        if HAS_CV2:
            try:
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    return False, [f"Cannot open video container: {video_path}"]

                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()

                if frame_count < expected_min_frames:
                    reasons.append(f"Video frame count {frame_count} is less than minimum {expected_min_frames}")
            except Exception as e:
                reasons.append(f"Error inspecting video {video_path}: {e}")

        return len(reasons) == 0, reasons
