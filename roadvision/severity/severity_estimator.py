from __future__ import annotations

from typing import Any, Dict


def estimate_severity(
    confidence: float,
    relative_area: float,
    persistence: float,
    road_coverage: float,
    low_threshold: float = 0.33,
    medium_threshold: float = 0.66,
) -> Dict[str, Any]:
    """Estimate severity using only measurable visual and temporal features."""
    confidence = max(0.0, min(float(confidence), 1.0))
    relative_area = max(0.0, min(float(relative_area), 1.0))
    persistence = max(0.0, min(float(persistence), 1.0))
    road_coverage = max(0.0, min(float(road_coverage), 1.0))

    score = (
        0.35 * confidence
        + 0.30 * relative_area
        + 0.20 * persistence
        + 0.15 * road_coverage
    )

    if score < low_threshold:
        severity = "LOW"
    elif score < medium_threshold:
        severity = "MEDIUM"
    else:
        severity = "HIGH"

    return {
        "severity": severity,
        "severity_score": round(float(score), 3),
        "factors": {
            "confidence": round(confidence, 3),
            "relative_area": round(relative_area, 3),
            "persistence": round(persistence, 3),
            "road_coverage": round(road_coverage, 3),
        },
    }
