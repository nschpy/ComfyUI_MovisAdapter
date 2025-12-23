"""
Color grading node for ComfyUI MoviePy integration.
"""

from typing import Tuple
from .video_types import VideoWrapper
from .color_grading import apply_color_grading


class ColorGrading:
    """
    Apply color grading to a video clip.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("VIDEO",),
                "brightness": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": -1.0,
                        "max": 1.0,
                        "step": 0.01,
                    },
                ),
                "contrast": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": -1.0,
                        "max": 1.0,
                        "step": 0.01,
                    },
                ),
                "saturation": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": -1.0,
                        "max": 1.0,
                        "step": 0.01,
                    },
                ),
                "gamma": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.1,
                        "max": 3.0,
                        "step": 0.01,
                    },
                ),
                "hue_shift": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": -180.0,
                        "max": 180.0,
                        "step": 1.0,
                    },
                ),
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "apply_grading"
    CATEGORY = "video/moviepy/edit"

    def apply_grading(
        self, video: VideoWrapper, brightness: float, contrast: float, saturation: float, gamma: float, hue_shift: float
    ) -> Tuple[VideoWrapper]:
        """Apply color grading to video."""
        result_clip = apply_color_grading(
            video.clip, brightness=brightness, contrast=contrast, saturation=saturation, gamma=gamma, hue_shift=hue_shift
        )

        return (VideoWrapper(result_clip),)
