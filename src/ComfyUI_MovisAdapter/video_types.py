"""
Video types and utilities for ComfyUI MoviePy integration.
"""

from typing import Optional, Tuple
from moviepy.video.VideoClip import VideoClip


class VideoWrapper:
    """
    Wrapper class for MoviePy VideoClip to use as custom data type in ComfyUI.

    This class wraps a MoviePy VideoClip and provides utilities for
    video manipulation and normalization.
    """

    def __init__(self, clip: VideoClip):
        """
        Initialize VideoWrapper with a MoviePy clip.

        Args:
            clip: MoviePy VideoClip object
        """
        if not isinstance(clip, VideoClip):
            raise TypeError(f"Expected VideoClip, got {type(clip)}")
        self.clip = clip

    @property
    def duration(self) -> float:
        """Get video duration in seconds."""
        return self.clip.duration

    @property
    def fps(self) -> float:
        """Get video FPS."""
        return self.clip.fps

    @property
    def size(self) -> Tuple[int, int]:
        """Get video size (width, height)."""
        return self.clip.size

    @property
    def w(self) -> int:
        """Get video width."""
        return self.clip.w

    @property
    def h(self) -> int:
        """Get video height."""
        return self.clip.h

    def __repr__(self) -> str:
        """String representation of VideoWrapper."""
        return f"VideoWrapper(duration={self.duration:.2f}s, fps={self.fps}, size={self.size})"


def normalize_video_params(clips: list[VideoWrapper], target_fps: Optional[float] = None) -> Tuple[float, Tuple[int, int]]:
    """
    Determine normalized FPS and resolution for a list of video clips.

    Args:
        clips: List of VideoWrapper objects
        target_fps: Optional target FPS. If None, uses the FPS of the first clip.

    Returns:
        Tuple of (fps, (width, height))
    """
    if not clips:
        raise ValueError("Cannot normalize empty list of clips")

    # Determine FPS
    fps = target_fps if target_fps is not None else clips[0].fps

    # Determine resolution (use max width and height)
    max_width = max(clip.w for clip in clips)
    max_height = max(clip.h for clip in clips)

    return fps, (max_width, max_height)


def resize_to_target(clip: VideoClip, target_size: Tuple[int, int]) -> VideoClip:
    """
    Resize a clip to target size if needed.

    Args:
        clip: MoviePy VideoClip
        target_size: Target (width, height)

    Returns:
        Resized VideoClip or original if size matches
    """
    if clip.size == target_size:
        return clip

    return clip.resize(newsize=target_size)


def set_fps_if_needed(clip: VideoClip, target_fps: float) -> VideoClip:
    """
    Set FPS of a clip if it differs from target.

    Args:
        clip: MoviePy VideoClip
        target_fps: Target FPS

    Returns:
        VideoClip with target FPS
    """
    if clip.fps == target_fps:
        return clip

    return clip.set_fps(target_fps)
