"""VideoTransition node - Adds transitions between video clips."""

import torch
from moviepy import concatenate_videoclips
from moviepy.video import fx
from ...common import image_tensor_to_moviepy_clip, moviepy_clip_to_image_tensor


class MPAVideoTransition:
    """
    Adds transitions between two video clips.
    
    This node supports various transition types including crossfade, fadein, fadeout, and fadeinout.
    The duration parameter controls the length of the transition effect.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IMAGE1": ("IMAGE",),
                "IMAGE2": ("IMAGE",),
                "transition_type": (["crossfade", "fadein", "fadeout", "fadeinout"],),
                "duration": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "number"
                }),
                "fps": ("FLOAT", {
                    "default": 24.0,
                    "min": 1.0,
                    "max": 120.0,
                    "step": 0.1,
                    "display": "number"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("video_with_transition",)
    FUNCTION = "add_transition"
    CATEGORY = "MPA/video"
    
    def add_transition(self, IMAGE1, IMAGE2, transition_type, duration, fps):
        """
        Add transition between two videos.
        
        Args:
            IMAGE1: First video clip
            IMAGE2: Second video clip
            transition_type: Type of transition (crossfade, fadein, fadeout, fadeinout)
            duration: Duration of the transition in seconds
            fps: Frames per second for the output video
            
        Returns:
            Tuple containing the video with transition as IMAGE tensor
        """
        # Convert IMAGE tensors to MoviePy clips
        clip1 = image_tensor_to_moviepy_clip(IMAGE1, fps=fps)
        clip2 = image_tensor_to_moviepy_clip(IMAGE2, fps=fps)
        
        # Apply transition based on type
        if transition_type == "crossfade":
            # Crossfade: first clip fades out while second fades in
            clip1 = clip1.with_effects([fx.CrossFadeOut(duration)])
            clip2 = clip2.with_effects([fx.CrossFadeIn(duration)])
        elif transition_type == "fadein":
            # Only fade in the second clip
            clip2 = clip2.with_effects([fx.FadeIn(duration=duration)])
        elif transition_type == "fadeout":
            # Only fade out the first clip
            clip1 = clip1.with_effects([fx.FadeOut(duration=duration)])
        elif transition_type == "fadeinout":
            # Fade out first clip and fade in second clip
            clip1 = clip1.with_effects([fx.FadeOut(duration=duration)])
            clip2 = clip2.with_effects([fx.FadeIn(duration=duration)])
        
        # Concatenate the clips
        combined_clip = concatenate_videoclips([clip1, clip2], method="compose")
        
        # Convert back to IMAGE tensor
        result_tensor = moviepy_clip_to_image_tensor(combined_clip)
        
        return (result_tensor,)

