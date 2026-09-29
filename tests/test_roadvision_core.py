import pytest

from roadvision.config import load_config
from roadvision.incidents.incident_manager import IncidentManager
from roadvision.ocr.ocr_service import normalize_ocr_result
from roadvision.performance.performance_monitor import PerformanceMonitor
from roadvision.severity.severity_estimator import estimate_severity
from roadvision.tracking.track_manager import TrackManager, TrackState


def test_severity_estimation_ranges_and_factors():
    result = estimate_severity(
        confidence=0.92,
        relative_area=0.18,
        persistence=0.8,
        road_coverage=0.22,
    )
    assert result["severity"] in {"LOW", "MEDIUM", "HIGH"}
    assert 0.0 <= result["severity_score"] <= 1.0
    assert "factors" in result
    assert "confidence" in result["factors"]


def test_config_loading_uses_defaults():
    cfg = load_config()
    assert cfg["detection"]["confidence_threshold"] > 0
    assert cfg["tracking"]["max_lost_frames"] >= 1
    assert cfg["performance"]["enabled"] is True


def test_track_manager_lifecycle_updates():
    manager = TrackManager()
    track = manager.register_track(1, 0)
    assert track.state == TrackState.NEW
    track = manager.update_track(1, 0, 0.9, (10, 10, 100, 100))
    assert track.state == TrackState.ACTIVE
    track = manager.mark_lost(1)
    assert track.state == TrackState.LOST
    track = manager.close_track(1)
    assert track.state == TrackState.CLOSED


def test_ocr_result_normalization():
    result = normalize_ocr_result(" road sign  ", 0.81, 10, "2026-09-29T12:00:00Z")
    assert result["text"] == "road sign"
    assert result["confidence"] == 0.81
    assert result["frame_id"] == 10


def test_incident_manager_deduplicates_tracks():
    manager = IncidentManager()
    first = manager.create_incident(track_id=7, confidence=0.9, severity="HIGH", source_video="demo.mp4")
    second = manager.create_incident(track_id=7, confidence=0.94, severity="MEDIUM", source_video="demo.mp4")
    assert first["incident_id"] == second["incident_id"]
    assert manager.get_incident_count() == 1


def test_performance_monitor_records_diagnostics():
    monitor = PerformanceMonitor(sample_window=5)
    monitor.record_frame(0.017)
    monitor.record_frame(0.025)
    monitor.record_frame(0.1)
    stats = monitor.summary()
    assert stats["frames_processed"] >= 3
    assert stats["avg_latency_ms"] > 0
    assert stats["p95_latency_ms"] > 0
