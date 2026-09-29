from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


class LocationProvider:
    def get_location(self) -> Dict[str, Any]:
        return {"latitude": None, "longitude": None, "location_status": "unavailable"}


class MockLocationProvider(LocationProvider):
    def __init__(self, latitude: float = 0.0, longitude: float = 0.0) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def get_location(self) -> Dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location_status": "available",
        }


class FileLocationProvider(LocationProvider):
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def get_location(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            return {"latitude": None, "longitude": None, "location_status": "unavailable"}
        try:
            with self.file_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            return {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "location_status": "available" if data.get("latitude") is not None and data.get("longitude") is not None else "unavailable",
            }
        except Exception:
            return {"latitude": None, "longitude": None, "location_status": "unavailable"}
