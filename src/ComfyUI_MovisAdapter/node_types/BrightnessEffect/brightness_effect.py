"""BrightnessEffect node - Adjusts video brightness."""

import torch
from moviepy.video import fx
from ...common import image_tensor_to_moviepy_clip, moviepy_clip_to_image_tensor


class MPABrightnessEffect:
    """
    Adjusts the brightness of a video clip.
    
    This node applies a brightness adjustment to all frames of the video.
    Factor > 1.0 increases brightness, < 1.0 decreases brightness.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IMAGE": ("IMAGE",),
                "factor": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 3.0,
                    "step": 0.01,
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
    RETURN_NAMES = ("adjusted_video",)
    FUNCTION = "apply_brightness"
    CATEGORY = "MPA/video"
    
    def apply_brightness(self, IMAGE, factor, fps):
        """
        Apply brightness adjustment to video.
        
        Args:
            IMAGE: Input video as IMAGE tensor
            factor: Brightness multiplier (1.0 = no change, >1.0 = brighter, <1.0 = darker)
            fps: Frames per second for the video
            
        Returns:
            Tuple containing the brightness-adjusted video as IMAGE tensor
        """
        # Convert IMAGE tensor to MoviePy clip
        clip = image_tensor_to_moviepy_clip(IMAGE, fps=fps)
        
        # Apply brightness effect using MoviePy's colorx effect
        # colorx multiplies all RGB values by the factor
        adjusted_clip = clip.with_effects([fx.MultiplyColor(factor)])        
        # Convert back to IMAGE tensor
        result_tensor = moviepy_clip_to_image_tensor(adjusted_clip)
        
        return (result_tensor,)

