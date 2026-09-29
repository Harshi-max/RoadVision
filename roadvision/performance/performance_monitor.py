from __future__ import annotations

import math
import os
import time
from typing import Dict, List


class PerformanceMonitor:
    def __init__(self, sample_window: int = 60) -> None:
        self.sample_window = max(1, int(sample_window))
        self.latencies: List[float] = []
        self.frames_processed = 0
        self.dropped_frames = 0
        self.total_detections = 0
        self.unique_tracked_potholes = 0
        self.started_at = time.perf_counter()

    def record_frame(self, latency_seconds: float) -> None:
        self.frames_processed += 1
        self.latencies.append(float(latency_seconds))
        if len(self.latencies) > self.sample_window:
            self.latencies.pop(0)

    def record_dropped_frames(self, count: int = 1) -> None:
        self.dropped_frames += max(0, int(count))

    def record_detections(self, count: int = 1) -> None:
        self.total_detections += max(0, int(count))

    def record_unique_tracks(self, count: int) -> None:
        self.unique_tracked_potholes = max(0, int(count))

    def summary(self) -> Dict[str, float | int]:
        elapsed = max(time.perf_counter() - self.started_at, 1e-6)
        actual_fps = self.frames_processed / elapsed if self.frames_processed else 0.0
        avg_latency_ms = (sum(self.latencies) / len(self.latencies) * 1000.0) if self.latencies else 0.0
        p95 = 0.0 if not self.latencies else sorted(self.latencies)[max(0, math.ceil(0.95 * len(self.latencies)) - 1)] * 1000.0

        cpu_percent = 0.0
        memory_mb = 0.0
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=None)
            memory_mb = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        except Exception:
            pass

        return {
            "input_fps": 0.0,
            "actual_fps": round(actual_fps, 2),
            "avg_latency_ms": round(avg_latency_ms, 2),
            "average_latency_ms": round(avg_latency_ms, 2),
            "p95_latency_ms": round(p95, 2),
            "frames_processed": self.frames_processed,
            "dropped_frames": self.dropped_frames,
            "total_detections": self.total_detections,
            "unique_tracked_potholes": self.unique_tracked_potholes,
            "cpu_usage_percent": round(cpu_percent, 2),
            "memory_usage_mb": round(memory_mb, 2),
        }
