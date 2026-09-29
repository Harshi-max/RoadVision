from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "detection": {
        "confidence_threshold": 0.70,
        "imgsz": 960,
        "iou_threshold": 0.45,
        "source": "video",
        "roi_enabled": False,
        "min_detection_area": 0.002,
    },
    "tracking": {
        "tracker": "bytetrack.yaml",
        "persist": True,
        "max_lost_frames": 10,
        "min_track_frames": 2,
    },
    "preprocessing": {
        "enabled": False,
        "resize": 0,
        "normalize": False,
        "gaussian_blur": 0,
        "brightness": 0,
        "contrast": 1.0,
        "clahe": False,
        "sharpen": False,
    },
    "severity": {
        "low_threshold": 0.33,
        "medium_threshold": 0.66,
    },
    "ocr": {
        "enabled": False,
        "sample_every_n_frames": 60,
        "min_confidence": 0.4,
    },
    "performance": {
        "enabled": True,
        "sample_window": 60,
    },
    "location": {
        "provider": "mock",
        "gps_enabled": False,
    },
    "notifications": {
        "mode": "console",
        "email_enabled": False,
        "webhook_enabled": False,
    },
}


def load_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    """Load the RoadVision YAML configuration and merge it with defaults."""
    base_dir = Path(__file__).resolve().parents[1]
    if config_path is None:
        config_path = base_dir / "config" / "config.yaml"

    config = dict(DEFAULT_CONFIG)
    path = Path(config_path)
    if not path.exists():
        return config

    try:
        import yaml
    except Exception:
        return config

    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in override.items():
            if isinstance(value, dict) and isinstance(base.get(key), dict):
                base[key] = deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    return deep_merge(config, loaded)
