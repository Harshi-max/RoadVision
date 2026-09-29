from __future__ import annotations

import cv2
import numpy as np
from typing import Any, Dict, Optional


class PreprocessingPipeline:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def apply(self, frame: Any) -> Any:
        if not self.config.get("enabled", False):
            return frame

        result = frame
        if self.config.get("resize", 0):
            height, width = result.shape[:2]
            scale = self.config["resize"] / max(width, height)
            if scale > 0:
                result = cv2.resize(result, (int(width * scale), int(height * scale)))

        if self.config.get("normalize", False):
            result = result.astype(np.float32) / 255.0

        if self.config.get("gaussian_blur", 0):
            k = int(self.config["gaussian_blur"])
            if k > 0 and k % 2 == 1:
                result = cv2.GaussianBlur(result, (k, k), 0)

        brightness = int(self.config.get("brightness", 0))
        if brightness:
            result = cv2.convertScaleAbs(result, alpha=1.0, beta=brightness)

        contrast = float(self.config.get("contrast", 1.0))
        if contrast != 1.0:
            result = cv2.convertScaleAbs(result, alpha=contrast, beta=0)

        if self.config.get("clahe", False):
            lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            result = cv2.merge((cl, a, b))
            result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

        if self.config.get("sharpen", False):
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
            result = cv2.filter2D(result, -1, kernel)

        return result
