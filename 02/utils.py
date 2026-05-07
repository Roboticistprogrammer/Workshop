"""Utility helpers for the ORB feature tracking demo.

This module keeps the non-demo specific pieces (video loading,
ORB/matcher construction, FPS calculation) separate from the main script.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Tuple

import cv2


def resolve_video_path(filename: str) -> str:
    """Resolve a video path relative to the repository root.

    The scripts in this project live under numbered folders (01, 02, ...).
    Videos are stored in the top-level "data" directory.
    """

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data", filename)


def create_video_capture(video_filename: str) -> cv2.VideoCapture:
    """Create an opened cv2.VideoCapture for the given video file.

    Raises a RuntimeError if the file cannot be opened.
    """

    video_path = resolve_video_path(video_filename)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video file: {video_path}")
    return cap


def create_orb_detector(max_features: int = 1000) -> cv2.ORB:
    """Create and configure an ORB detector suitable for real-time work."""

    return cv2.ORB_create(nfeatures=max_features)


def create_matcher() -> cv2.BFMatcher:
    """Create a brute-force matcher for ORB (binary) descriptors."""

    # NORM_HAMMING is the appropriate norm for ORB's binary descriptors.
    return cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


@dataclass
class FpsCounter:
    """Simple FPS helper to track average processing rate."""

    start_time: float = field(default_factory=time.time)
    frames: int = 0

    def update(self) -> float:
        """Record a processed frame and return the current average FPS."""

        self.frames += 1
        elapsed = max(time.time() - self.start_time, 1e-6)
        return self.frames / elapsed


def draw_fps(frame, fps: float, position: Tuple[int, int] = (40, 40)) -> None:
    """Overlay FPS text on a frame in-place."""

    text = f"FPS: {fps:.1f}"
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
