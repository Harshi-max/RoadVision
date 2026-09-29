from __future__ import annotations

import re
from typing import Any, Dict, Optional


def normalize_ocr_result(text: Optional[str], confidence: float, frame_id: int, timestamp: Optional[str]) -> Dict[str, Any]:
    cleaned = re.sub(r"\s+", " ", (text or "")).strip()
    normalized = cleaned.lower()
    return {
        "text": normalized,
        "confidence": float(confidence),
        "frame_id": int(frame_id),
        "timestamp": timestamp,
    }


class OCRService:
    def __init__(self, enabled: bool = False, min_confidence: float = 0.4) -> None:
        self.enabled = enabled
        self.min_confidence = min_confidence

    def process_frame(self, image: Any, frame_id: int, timestamp: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return None
        try:
            import pytesseract
            from PIL import Image
            if not hasattr(image, "copy"):
                image = Image.fromarray(image)
            text = pytesseract.image_to_string(image, config="--psm 6")
            confidence = 0.75 if text.strip() else 0.0
            result = normalize_ocr_result(text, confidence, frame_id, timestamp)
            if result["text"] and result["confidence"] >= self.min_confidence:
                return result
            return None
        except Exception:
            return None
