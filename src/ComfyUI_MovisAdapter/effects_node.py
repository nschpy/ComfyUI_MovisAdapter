"""
Video effects node for ComfyUI MoviePy integration.
"""

from typing import Tuple
from .video_types import VideoWrapper
from .effects import apply_effect


class VideoEffects:
    """
    Apply effects to a video clip.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("VIDEO",),
                "effect_type": (["none", "blur", "sharpen", "mirror_x", "mirror_y", "speed_up", "slow_down", "noise", "vignette"],),
                "intensity": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 10.0,
                        "step": 0.1,
                    },
                ),
            },
            "optional": {
                "blur_radius": (
                    "INT",
                    {
                        "default": 2,
                        "min": 1,
                        "max": 20,
                        "step": 1,
                    },
                ),
                "speed_factor": (
                    "FLOAT",
                    {
                        "default": 1.5,
                        "min": 0.1,
                        "max": 10.0,
                        "step": 0.1,
                    },
                ),
                "noise_level": (
                    "FLOAT",
                    {
                        "default": 0.1,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                    },
                ),
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "apply_effect"
    CATEGORY = "video/moviepy/edit"

    def apply_effect(
        self,
        video: VideoWrapper,
        effect_type: str,
        intensity: float,
        blur_radius: int = 2,
        speed_factor: float = 1.5,
        noise_level: float = 0.1,
    ) -> Tuple[VideoWrapper]:
        """Apply effect to video."""
        if effect_type == "none":
            return (video,)

        # Prepare effect parameters
        effect_params = {"intensity": intensity}

        if effect_type == "blur":
            effect_params["radius"] = blur_radius
        elif effect_type in ["speed_up", "slow_down"]:
            effect_params["speed_factor"] = speed_factor
        elif effect_type == "noise":
            effect_params["noise_level"] = noise_level

        # Apply effect
        result_clip = apply_effect(video.clip, effect_type, **effect_params)

        return (VideoWrapper(result_clip),)
