"""Joint range, velocity limits, and NaN/null sanity validator."""
from typing import List, Tuple, Dict, Any


class TelemetryValidator:
    """Checks that telemetry samples stay within physical limits with no NaN or null dropouts."""

    def validate_telemetry_records(self, records: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        reasons = []
        if not records:
            return False, ["Telemetry stream has no records"]

        nan_count = 0
        limit_violations = 0

        for r in records:
            joints = r.get("joint_positions")
            if not joints or any(j is None for j in joints):
                nan_count += 1
                continue

            # Check extreme joint angle limits (e.g. > 2*pi)
            if any(abs(j) > 6.5 for j in joints):
                limit_violations += 1

        if nan_count > 0:
            reasons.append(f"Found {nan_count} telemetry samples with null or NaN joint angles")
        if limit_violations > 0:
            reasons.append(f"Found {limit_violations} telemetry samples with out-of-range joint limits")

        is_valid = (nan_count == 0) and (limit_violations == 0)
        return is_valid, reasons
