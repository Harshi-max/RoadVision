from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class RoadDefectIncident:
    incident_id: str
    track_id: int
    defect_type: str = "pothole"
    severity: str = "LOW"
    severity_score: float = 0.0
    confidence: float = 0.0
    first_seen: str = ""
    last_seen: str = ""
    frame_count: int = 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    OCR_text: str = ""
    source_video: str = ""
    thumbnail_path: str = ""
    status: str = "NEW"
    location_status: str = "unavailable"
    metadata: Dict[str, Any] = field(default_factory=dict)


class IncidentManager:
    def __init__(self) -> None:
        self._incidents: Dict[str, Dict[str, Any]] = {}
        self._track_index: Dict[int, str] = {}

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def create_incident(self, track_id: int, confidence: float, severity: str, source_video: str, **kwargs: Any) -> Dict[str, Any]:
        existing_id = self._track_index.get(track_id)
        if existing_id and existing_id in self._incidents:
            incident = self._incidents[existing_id]
            incident["confidence"] = max(float(confidence), float(incident.get("confidence", 0.0)))
            incident["severity"] = severity
            incident["last_seen"] = self._now()
            incident["frame_count"] += 1
            return incident

        incident_id = f"INC-{len(self._incidents) + 1:04d}"
        incident = {
            "incident_id": incident_id,
            "track_id": track_id,
            "defect_type": kwargs.get("defect_type", "pothole"),
            "severity": severity,
            "severity_score": kwargs.get("severity_score", 0.0),
            "confidence": float(confidence),
            "first_seen": self._now(),
            "last_seen": self._now(),
            "frame_count": kwargs.get("frame_count", 1),
            "latitude": kwargs.get("latitude"),
            "longitude": kwargs.get("longitude"),
            "OCR_text": kwargs.get("OCR_text", ""),
            "source_video": source_video,
            "thumbnail_path": kwargs.get("thumbnail_path", ""),
            "status": kwargs.get("status", "NEW"),
            "location_status": kwargs.get("location_status", "unavailable"),
        }
        self._incidents[incident_id] = incident
        self._track_index[track_id] = incident_id
        return incident

    def get_incident_count(self) -> int:
        return len(self._incidents)

    def list_incidents(self) -> list[Dict[str, Any]]:
        return list(self._incidents.values())
