"""
Images to video conversion node for ComfyUI MoviePy integration.
"""

from typing import Tuple
import numpy as np
import torch  # type: ignore
from moviepy.video.VideoClip import VideoClip  # type: ignore

from .video_types import VideoWrapper


class ImagesToVideo:
    """
    Convert a sequence of images to a video clip.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "fps": (
                    "FLOAT",
                    {
                        "default": 24.0,
                        "min": 1.0,
                        "max": 120.0,
                        "step": 0.1,
                    },
                ),
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "convert_to_video"
    CATEGORY = "video/moviepy/convert"

    def convert_to_video(self, images: torch.Tensor, fps: float) -> Tuple[VideoWrapper]:
        """
        Convert images to video clip.

        Args:
            images: torch.Tensor with shape [B, H, W, C] where values are in [0, 1]
            fps: Frames per second for the output video

        Returns:
            VideoWrapper containing the created video clip
        """
        if images is None or images.numel() == 0:
            raise ValueError("No images provided")

        # Convert torch tensor to numpy
        # Shape: [B, H, W, C] with values in [0, 1]
        images_np = images.cpu().numpy()

        # Get batch size and image dimensions
        batch_size, height, width, channels = images_np.shape

        if batch_size == 0:
            raise ValueError("Empty image batch")

        # Convert each frame from [H, W, C] with values in [0, 1] to [H, W, C] with values in [0, 255]
        frames = []
        for i in range(batch_size):
            frame = images_np[i]  # [H, W, C]
            # Convert from [0, 1] to [0, 255] and ensure uint8
            frame_uint8 = (np.clip(frame, 0.0, 1.0) * 255.0).astype(np.uint8)
            frames.append(frame_uint8)

        # Calculate duration based on number of frames and fps
        duration = batch_size / fps

        # Create VideoClip from image sequence using make_frame
        def make_frame(t):
            """Return frame at time t."""
            frame_index = int(t * fps)
            # Clamp to valid range
            frame_index = max(0, min(frame_index, batch_size - 1))
            return frames[frame_index]

        # Create VideoClip with the make_frame function
        clip = VideoClip(frame_function=make_frame, duration=duration)
        clip = clip.with_fps(fps)

        return (VideoWrapper(clip),)
