"""
ComfyUI custom nodes for MoviePy video processing.
"""

import os
from pathlib import Path
from typing import List, Tuple
import numpy as np
import torch
from moviepy.editor import VideoFileClip, concatenate_videoclips

from .video_types import VideoWrapper, normalize_video_params, resize_to_target, set_fps_if_needed
from .transitions import apply_transition
from .effects import apply_effect
from .color_grading import apply_color_grading


class LoadVideo:
    """
    Load a video file and return a VIDEO object.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                    },
                ),
                "audio": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "load_video"
    CATEGORY = "video/moviepy/load"

    def load_video(self, video_path: str, audio: bool) -> Tuple[VideoWrapper]:
        """Load video from file path."""
        if not video_path:
            raise ValueError("Video path cannot be empty")

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        try:
            clip = VideoFileClip(video_path, audio=audio)
            return (VideoWrapper(clip),)
        except Exception as e:
            raise RuntimeError(f"Failed to load video: {str(e)}")


class SaveVideo:
    """
    Save a VIDEO object to a file.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("VIDEO",),
                "filename": (
                    "STRING",
                    {
                        "default": "output.mp4",
                        "multiline": False,
                    },
                ),
                "codec": (["libx264", "libx265", "mpeg4"],),
                "bitrate": (
                    "STRING",
                    {
                        "default": "8000k",
                        "multiline": False,
                    },
                ),
                "audio_codec": (["aac", "mp3", "libvorbis"],),
                "preset": (["ultrafast", "fast", "medium", "slow"],),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)
    FUNCTION = "save_video"
    CATEGORY = "video/moviepy/save"
    OUTPUT_NODE = True

    def save_video(self, video: VideoWrapper, filename: str, codec: str, bitrate: str, audio_codec: str, preset: str) -> Tuple[str]:
        """Save video to file."""
        # Ensure output directory exists
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            video.clip.write_videofile(
                str(output_path), codec=codec, bitrate=bitrate, audio_codec=audio_codec, preset=preset, verbose=False, logger=None
            )
            return (str(output_path.absolute()),)
        except Exception as e:
            raise RuntimeError(f"Failed to save video: {str(e)}")


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


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "LoadVideo": LoadVideo,
    "SaveVideo": SaveVideo,
    "VideoConcatenate": VideoConcatenate,
    "VideoEffects": VideoEffects,
    "ColorGrading": ColorGrading,
    "VideoToImages": VideoToImages,
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadVideo": "Load Video",
    "SaveVideo": "Save Video",
    "VideoConcatenate": "Concatenate Videos",
    "VideoEffects": "Video Effects",
    "ColorGrading": "Color Grading",
    "VideoToImages": "Video to Images",
}
