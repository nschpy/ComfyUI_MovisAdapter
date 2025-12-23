"""
Load video node for ComfyUI MoviePy integration.
"""

import os
from typing import Tuple
from moviepy import VideoFileClip  # type: ignore

from .video_types import VideoWrapper


class LoadVideo:
    """
    Load a video file and return a VIDEO object.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                    },
                ),
                "audio": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "load_video"
    CATEGORY = "video/moviepy/load"

    def load_video(self, video_path: str, audio: bool) -> Tuple[VideoWrapper]:
        """Load video from file path."""
        if not video_path:
            raise ValueError("Video path cannot be empty")

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        try:
            clip = VideoFileClip(video_path, audio=audio)
            return (VideoWrapper(clip),)
        except Exception as e:
            raise RuntimeError(f"Failed to load video: {str(e)}")
