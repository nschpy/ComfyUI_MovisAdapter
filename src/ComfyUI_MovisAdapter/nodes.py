"""
ComfyUI custom nodes registration for MoviePy video processing.
"""

from .save_video import SaveVideo
from .concatenate_node import VideoConcatenate
from .effects_node import VideoEffects
from .color_grading_node import ColorGrading
from .video_to_images import VideoToImages
from .images_to_video import ImagesToVideo

# Prefix for custom nodes to make them easily searchable in ComfyUI
NODE_PREFIX = "MovisAdapter_"

# Node class mappings with prefix
NODE_CLASS_MAPPINGS = {
    f"{NODE_PREFIX}SaveVideo": SaveVideo,
    f"{NODE_PREFIX}VideoConcatenate": VideoConcatenate,
    f"{NODE_PREFIX}VideoEffects": VideoEffects,
    f"{NODE_PREFIX}ColorGrading": ColorGrading,
    f"{NODE_PREFIX}VideoToImages": VideoToImages,
    f"{NODE_PREFIX}ImagesToVideo": ImagesToVideo,
}

# Display name mappings with prefix
NODE_DISPLAY_NAME_MAPPINGS = {
    f"{NODE_PREFIX}SaveVideo": "MovisAdapter Save Video",
    f"{NODE_PREFIX}VideoConcatenate": "MovisAdapter Concatenate Videos",
    f"{NODE_PREFIX}VideoEffects": "MovisAdapter Video Effects",
    f"{NODE_PREFIX}ColorGrading": "MovisAdapter Color Grading",
    f"{NODE_PREFIX}VideoToImages": "MovisAdapter Video to Images",
    f"{NODE_PREFIX}ImagesToVideo": "MovisAdapter Images to Video",
}
