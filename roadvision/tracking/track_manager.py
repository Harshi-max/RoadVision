from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class TrackState(Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    LOST = "LOST"
    CLOSED = "CLOSED"


@dataclass
class TrackRecord:
    track_id: int
    first_frame: int
    last_frame: int
    state: TrackState = TrackState.NEW
    detection_count: int = 0
    confidence_history: List[float] = field(default_factory=list)
    boxes: List[Tuple[int, int, int, int]] = field(default_factory=list)
    severity: str = "LOW"
    location: Optional[Tuple[float, float]] = None
    timestamp: Optional[str] = None

    def update(self, frame_id: int, confidence: float, box: Tuple[int, int, int, int]) -> None:
        self.last_frame = frame_id
        self.detection_count += 1
        self.confidence_history.append(float(confidence))
        self.boxes.append(box)


class TrackManager:
    def __init__(self) -> None:
        self.tracks: Dict[int, TrackRecord] = {}

    def register_track(self, track_id: int, frame_id: int) -> TrackRecord:
        track = TrackRecord(track_id=track_id, first_frame=frame_id, last_frame=frame_id)
        self.tracks[track_id] = track
        return track

    def get_track(self, track_id: int) -> Optional[TrackRecord]:
        return self.tracks.get(track_id)

    def update_track(
        self,
        track_id: int,
        frame_id: int,
        confidence: float,
        box: Tuple[int, int, int, int],
    ) -> TrackRecord:
        track = self.tracks.get(track_id)
        if track is None:
            track = self.register_track(track_id, frame_id)
        track.state = TrackState.ACTIVE
        track.update(frame_id, confidence, box)
        return track

    def mark_lost(self, track_id: int) -> TrackRecord:
        track = self.tracks.get(track_id)
        if track is None:
            raise KeyError(f"No track found for id {track_id}")
        track.state = TrackState.LOST
        return track

    def close_track(self, track_id: int) -> TrackRecord:
        track = self.tracks.get(track_id)
        if track is None:
            raise KeyError(f"No track found for id {track_id}")
        track.state = TrackState.CLOSED
        return track

    def active_tracks(self) -> List[TrackRecord]:
        return [track for track in self.tracks.values() if track.state == TrackState.ACTIVE]
