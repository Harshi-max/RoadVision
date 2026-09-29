from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional


class AuthorityRouter:
    def __init__(self, config_path: str | Path | None = None) -> None:
        self.config_path = Path(config_path) if config_path else Path(__file__).resolve().parents[1] / ".." / "config" / "authorities.yaml"
        self.authorities: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        path = self.config_path.resolve()
        if not path.exists():
            return []
        try:
            import yaml
            with path.open("r", encoding="utf-8") as handle:
                data = yaml.safe_load(handle) or {}
            authorities = data.get("authorities", [])
            if isinstance(authorities, dict):
                return [authorities]
            return authorities
        except Exception:
            return []

    def resolve(self, location: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if not self.authorities:
            return None
        if not location:
            return self.authorities[0]
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        for authority in self.authorities:
            if authority.get("area"):
                area = authority["area"]
                if latitude is not None and longitude is not None:
                    if area.lower() in {"default", "global"}:
                        return authority
        return self.authorities[0]
