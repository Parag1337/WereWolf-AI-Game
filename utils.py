"""
Utility functions for math, easing, and asset loading.
"""

import os
from typing import Optional

from config import ASSET_DIR, ASSET_VARIANTS


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp a value between low and high."""
    return max(low, min(high, value))


def lerp(start: float, end: float, amount: float) -> float:
    """Linear interpolation between start and end."""
    return start + (end - start) * amount


def ease_out_cubic(t: float) -> float:
    """Ease out cubic easing function."""
    return 1.0 - pow(1.0 - clamp(t), 3)


def ease_out_back(t: float) -> float:
    """Ease out back easing function."""
    t = clamp(t)
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * pow(t - 1.0, 3) + c1 * pow(t - 1.0, 2)


def resolve_asset_path(key: str) -> Optional[str]:
    """
    Resolve asset file path with fallback for alternate filenames.
    
    Handles filename variations like "dayBackround.png" vs "dayBackground.png"
    """
    for name in ASSET_VARIANTS[key]:
        path = os.path.join(ASSET_DIR, name)
        if os.path.exists(path):
            return path
    return None
