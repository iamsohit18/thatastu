"""Unit tests for timestamp anomaly detection."""
from src.synchronization.timestamp import TimestampAnomalyDetector, SyncTimestamp

def test_timestamp_reversal_detection():
    detector = TimestampAnomalyDetector("test_cam", max_gap_seconds=0.05)
    s1 = SyncTimestamp(wall_time_s=1.0, monotonic_ns=1000, sequence_id=1, source_id="test")
    ok1, _ = detector.check_sample(s1)
    assert ok1 is True

    # Reverse timestamp
    s2 = SyncTimestamp(wall_time_s=0.9, monotonic_ns=900, sequence_id=2, source_id="test")
    ok2, err = detector.check_sample(s2)
    assert ok2 is False
    assert "reversal" in err.lower()
