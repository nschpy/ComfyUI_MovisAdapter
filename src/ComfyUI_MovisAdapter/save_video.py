"""
Save video node for ComfyUI MoviePy integration.
"""

from pathlib import Path
from typing import Tuple
from .video_types import VideoWrapper


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
            video.clip.write_videofile(str(output_path), codec=codec, bitrate=bitrate, audio_codec=audio_codec, preset=preset, logger=None)
            return (str(output_path.absolute()),)
        except Exception as e:
            raise RuntimeError(f"Failed to save video: {str(e)}")
