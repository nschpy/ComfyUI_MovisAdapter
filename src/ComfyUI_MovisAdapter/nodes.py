"""MoviePy Adapter nodes registration for ComfyUI."""

# Import all node classes
from .node_types.CombineVideos.combine_videos import MPACombineVideos
from .node_types.VideoTransition.video_transition import MPAVideoTransition
from .node_types.BrightnessEffect.brightness_effect import MPABrightnessEffect
from .node_types.ContrastEffect.contrast_effect import MPAContrastEffect
from .node_types.SpeedEffect.speed_effect import MPASpeedEffect
from .node_types.TextOverlay.text_overlay import MPATextOverlay


# Node class mappings
# Keys are the internal node identifiers used by ComfyUI
NODE_CLASS_MAPPINGS = {
    "MPA Combine Videos": MPACombineVideos,
    "MPA Video Transition": MPAVideoTransition,
    "MPA Brightness Effect": MPABrightnessEffect,
    "MPA Contrast Effect": MPAContrastEffect,
    "MPA Speed Effect": MPASpeedEffect,
    "MPA Text Overlay": MPATextOverlay,
}

# Node display name mappings
# Keys match NODE_CLASS_MAPPINGS, values are human-readable names shown in UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "MPA Combine Videos": "MPA Combine Videos",
    "MPA Video Transition": "MPA Video Transition",
    "MPA Brightness Effect": "MPA Brightness Effect",
    "MPA Contrast Effect": "MPA Contrast Effect",
    "MPA Speed Effect": "MPA Speed Effect",
    "MPA Text Overlay": "MPA Text Overlay",
}
