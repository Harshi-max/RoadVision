from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class ReportGenerator:
    def __init__(self, output_dir: str | Path = "data/incident_reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_json(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "incident_id": incident.get("incident_id"),
            "defect_type": incident.get("defect_type", "pothole"),
            "severity": incident.get("severity", "LOW"),
            "confidence": incident.get("confidence", 0.0),
            "location": {
                "latitude": incident.get("latitude"),
                "longitude": incident.get("longitude"),
            },
            "ocr_text": incident.get("OCR_text", ""),
            "timestamp": incident.get("last_seen") or datetime.now(timezone.utc).isoformat(),
            "evidence_image": incident.get("thumbnail_path", ""),
        }
        out = self.output_dir / f"{payload['incident_id']}.json"
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload

    def generate_human_readable(self, incident: Dict[str, Any]) -> str:
        return (
            f"Incident: {incident.get('incident_id')}\n"
            f"Type: {incident.get('defect_type', 'pothole')}\n"
            f"Severity: {incident.get('severity', 'LOW')}\n"
            f"Confidence: {incident.get('confidence', 0.0)}\n"
            f"Location: {incident.get('latitude', 'N/A')}, {incident.get('longitude', 'N/A')}\n"
            f"OCR: {incident.get('OCR_text', 'N/A')}\n"
            f"Timestamp: {incident.get('last_seen') or 'unknown'}\n"
        )
