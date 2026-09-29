from __future__ import annotations

from typing import Any, Dict


class NotificationService:
    def __init__(self, mode: str = "console") -> None:
        self.mode = mode

    def send(self, report: Dict[str, Any]) -> Dict[str, Any]:
        if self.mode == "console":
            return ConsoleNotifier().send(report)
        if self.mode == "email":
            return EmailNotifier().send(report)
        if self.mode == "webhook":
            return WebhookNotifier().send(report)
        return ConsoleNotifier().send(report)


class ConsoleNotifier:
    def send(self, report: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[RoadVision] {report.get('incident_id')} {report.get('severity', 'UNKNOWN')}")
        return {"status": "sent", "mode": "console"}


class EmailNotifier:
    def send(self, report: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "mock", "mode": "email", "incident_id": report.get("incident_id")}


class WebhookNotifier:
    def send(self, report: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "mock", "mode": "webhook", "incident_id": report.get("incident_id")}
