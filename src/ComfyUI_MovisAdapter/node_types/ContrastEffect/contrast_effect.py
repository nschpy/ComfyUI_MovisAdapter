"""ContrastEffect node - Adjusts video contrast."""

from moviepy.video import fx
from ...common import image_tensor_to_moviepy_clip, moviepy_clip_to_image_tensor


class MPAContrastEffect:
    """
    Adjusts the contrast of a video clip.
    
    This node applies a contrast adjustment to all frames of the video.
    Factor > 1.0 increases contrast, < 1.0 decreases contrast.
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
    FUNCTION = "apply_contrast"
    CATEGORY = "MPA/video"
    
    def apply_contrast(self, IMAGE, factor, fps):
        """
        Apply contrast adjustment to video.
        
        Args:
            IMAGE: Input video as IMAGE tensor
            factor: Contrast multiplier (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)
            fps: Frames per second for the video
            
        Returns:
            Tuple containing the contrast-adjusted video as IMAGE tensor
        """
        # Convert IMAGE tensor to MoviePy clip
        clip = image_tensor_to_moviepy_clip(IMAGE, fps=fps)
        
        # Apply contrast effect using MoviePy's lum_contrast effect
        # lum_contrast adjusts the contrast by modifying luminance
        adjusted_clip = clip.with_effects([fx.LumContrast(contrast=factor)])
        
        # Convert back to IMAGE tensor
        result_tensor = moviepy_clip_to_image_tensor(adjusted_clip)
        
        return (result_tensor,)

