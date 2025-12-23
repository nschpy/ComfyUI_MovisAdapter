"""
Video concatenate node for ComfyUI MoviePy integration.
"""

from typing import List, Tuple
from moviepy import concatenate_videoclips  # type: ignore

from .video_types import VideoWrapper, normalize_video_params, resize_to_target, set_fps_if_needed
from .transitions import apply_transition


class VideoConcatenate:
    """
    Concatenate multiple video clips with optional transitions.
    """

    INPUT_IS_LIST = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "videos": ("VIDEO",),
                "mode": (["simple", "transition"],),
                "transition_type": (["none", "crossfade", "fade_black", "fade_white", "slide_left", "slide_right", "zoom_in", "zoom_out"],),
                "transition_duration": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.1,
                        "max": 10.0,
                        "step": 0.1,
                    },
                ),
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "concatenate"
    CATEGORY = "video/moviepy/edit"

    def concatenate(
        self, videos: List[VideoWrapper], mode: List[str], transition_type: List[str], transition_duration: List[float]
    ) -> Tuple[VideoWrapper]:
        """Concatenate videos with optional transitions."""
        # Extract single values from lists (ComfyUI list processing)
        mode = mode[0] if isinstance(mode, list) else mode
        transition_type = transition_type[0] if isinstance(transition_type, list) else transition_type
        transition_duration = transition_duration[0] if isinstance(transition_duration, list) else transition_duration

        if not videos:
            raise ValueError("No videos provided for concatenation")

        if len(videos) == 1:
            return (videos[0],)

        # Normalize video parameters
        target_fps, target_size = normalize_video_params(videos)

        # Prepare clips with normalized parameters
        normalized_clips = []
        for video_wrapper in videos:
            clip = video_wrapper.clip
            clip = set_fps_if_needed(clip, target_fps)
            clip = resize_to_target(clip, target_size)
            normalized_clips.append(clip)

        # Apply concatenation based on mode
        if mode == "simple" or transition_type == "none":
            result_clip = concatenate_videoclips(normalized_clips)
        else:
            result_clip = apply_transition(normalized_clips, transition_type, transition_duration)

        return (VideoWrapper(result_clip),)
