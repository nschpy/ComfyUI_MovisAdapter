"""SpeedEffect node - Changes video playback speed."""

from moviepy.video import fx
from ...common import image_tensor_to_moviepy_clip, moviepy_clip_to_image_tensor


class MPASpeedEffect:
    """
    Changes the playback speed of a video clip.
    
    This node applies a speed adjustment to the video.
    Factor > 1.0 speeds up the video, < 1.0 slows it down.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IMAGE": ("IMAGE",),
                "factor": ("FLOAT", {
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
    RETURN_NAMES = ("adjusted_video",)
    FUNCTION = "apply_speed"
    CATEGORY = "MPA/video"
    
    def apply_speed(self, IMAGE, factor, fps):
        """
        Apply speed adjustment to video.
        
        Args:
            IMAGE: Input video as IMAGE tensor
            factor: Speed multiplier (1.0 = normal, >1.0 = faster, <1.0 = slower)
            fps: Frames per second for the input video
            
        Returns:
            Tuple containing the speed-adjusted video as IMAGE tensor
        """
        # Convert IMAGE tensor to MoviePy clip
        clip = image_tensor_to_moviepy_clip(IMAGE, fps=fps)
        
        # Apply speed effect using MoviePy's speedx effect
        # speedx multiplies the playback speed by the factor
        adjusted_clip = clip.with_effects([fx.MultiplySpeed(factor)])
        
        # Convert back to IMAGE tensor
        result_tensor = moviepy_clip_to_image_tensor(adjusted_clip)
        
        return (result_tensor,)

