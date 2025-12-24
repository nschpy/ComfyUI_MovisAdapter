"""CombineVideos node - Combines multiple videos into one."""

import torch
from moviepy import concatenate_videoclips
from ...common import image_tensor_to_moviepy_clip, moviepy_clip_to_image_tensor, resize_clip_to_resolution


class MPACombineVideos:
    """
    Combines multiple video clips into one sequential video.
    
    This node accepts 1 to 10 video inputs (IMAGE tensors) and concatenates them
    into a single video. All videos are resized to match the resolution of the first video.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IMAGE1": ("IMAGE",),
                "fps": ("FLOAT", {
                    "default": 24.0,
                    "min": 1.0,
                    "max": 120.0,
                    "step": 0.1,
                    "display": "number"
                }),
            },
            "optional": {
                "IMAGE2": ("IMAGE",),
                "IMAGE3": ("IMAGE",),
                "IMAGE4": ("IMAGE",),
                "IMAGE5": ("IMAGE",),
                "IMAGE6": ("IMAGE",),
                "IMAGE7": ("IMAGE",),
                "IMAGE8": ("IMAGE",),
                "IMAGE9": ("IMAGE",),
                "IMAGE10": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("combined_video",)
    FUNCTION = "combine_videos"
    CATEGORY = "MPA/video"
    
    def combine_videos(self, IMAGE1, fps, IMAGE2=None, IMAGE3=None, IMAGE4=None, 
                       IMAGE5=None, IMAGE6=None, IMAGE7=None, IMAGE8=None, 
                       IMAGE9=None, IMAGE10=None):
        """
        Combine multiple videos into one sequential video.
        
        Args:
            IMAGE1: First video (required)
            fps: Frames per second for the output video
            IMAGE2-IMAGE10: Additional videos (optional)
            
        Returns:
            Tuple containing the combined video as IMAGE tensor
        """
        # Collect all non-None video inputs
        video_inputs = [IMAGE1]
        for img in [IMAGE2, IMAGE3, IMAGE4, IMAGE5, IMAGE6, IMAGE7, IMAGE8, IMAGE9, IMAGE10]:
            if img is not None:
                video_inputs.append(img)
        
        if len(video_inputs) == 0:
            raise ValueError("At least one video input is required")
        
        # Convert all IMAGE tensors to MoviePy clips
        clips = []
        target_width = None
        target_height = None
        
        for idx, video_tensor in enumerate(video_inputs):
            # Convert to MoviePy clip
            clip = image_tensor_to_moviepy_clip(video_tensor, fps=fps)
            
            # Get resolution of first video as target
            if idx == 0:
                target_width, target_height = clip.size
                clips.append(clip)
            else:
                # Resize subsequent videos to match first video's resolution
                if clip.size != (target_width, target_height):
                    clip = resize_clip_to_resolution(clip, target_width, target_height)
                clips.append(clip)
        
        # Concatenate all clips
        if len(clips) == 1:
            combined_clip = clips[0]
        else:
            combined_clip = concatenate_videoclips(clips, method="compose")
        
        # Convert back to IMAGE tensor
        result_tensor = moviepy_clip_to_image_tensor(combined_clip)
        
        return (result_tensor,)

