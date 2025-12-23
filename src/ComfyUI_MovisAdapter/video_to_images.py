"""
Video to images conversion node for ComfyUI MoviePy integration.
"""

from typing import Tuple
import numpy as np
import torch  # type: ignore
from .video_types import VideoWrapper


class VideoToImages:
    """
    Convert a video clip to a sequence of image frames.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("VIDEO",),
            },
            "optional": {
                "fps": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": 0.0,
                        "max": 120.0,
                        "step": 0.1,
                    },
                ),
                "start_time": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": 0.0,
                        "max": 10000.0,
                        "step": 0.1,
                    },
                ),
                "end_time": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": 0.0,
                        "max": 10000.0,
                        "step": 0.1,
                    },
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "convert_to_images"
    CATEGORY = "video/moviepy/convert"

    def convert_to_images(
        self, video: VideoWrapper, fps: float = 0.0, start_time: float = 0.0, end_time: float = 0.0
    ) -> Tuple[torch.Tensor]:
        """Convert video to image frames."""
        clip = video.clip

        # Use video FPS if not specified
        target_fps = fps if fps > 0 else clip.fps

        # Use full duration if end_time not specified
        actual_end_time = end_time if end_time > 0 else clip.duration

        # Clamp times to valid range
        start_time = max(0.0, min(start_time, clip.duration))
        actual_end_time = max(start_time, min(actual_end_time, clip.duration))

        # Extract frames
        frames = []
        duration = actual_end_time - start_time
        num_frames = int(duration * target_fps)

        for i in range(num_frames):
            t = start_time + (i / target_fps)
            if t >= actual_end_time:
                break

            frame = clip.get_frame(t)
            # Convert from [H, W, C] with values in [0, 255] to [H, W, C] with values in [0, 1]
            frame_normalized = frame.astype(np.float32) / 255.0
            frames.append(frame_normalized)

        if not frames:
            raise ValueError("No frames extracted from video")

        # Stack frames into a batch tensor [B, H, W, C]
        frames_array = np.stack(frames, axis=0)
        frames_tensor = torch.from_numpy(frames_array)

        return (frames_tensor,)
