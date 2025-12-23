"""
Video effects for ComfyUI MoviePy integration.
"""

from moviepy.video.VideoClip import VideoClip
from moviepy.video.fx import MirrorX, MirrorY
import numpy as np
from scipy.ndimage import gaussian_filter


def apply_blur(clip: VideoClip, radius: int = 2, intensity: float = 1.0) -> VideoClip:
    """
    Apply blur effect to video.

    Args:
        clip: Input VideoClip
        radius: Blur radius
        intensity: Effect intensity (0.0 to 1.0+)

    Returns:
        VideoClip with blur effect
    """
    effective_radius = radius * intensity

    def blur_frame(frame):
        if effective_radius <= 0:
            return frame
        # Apply gaussian blur to each channel
        blurred = np.stack([gaussian_filter(frame[:, :, i], sigma=effective_radius) for i in range(frame.shape[2])], axis=2)
        return np.clip(blurred, 0, 255).astype(np.uint8)

    return clip.image_transform(blur_frame)


def apply_sharpen(clip: VideoClip, intensity: float = 1.0) -> VideoClip:
    """
    Apply sharpen effect to video.

    Args:
        clip: Input VideoClip
        intensity: Effect intensity (0.0 to 1.0+)

    Returns:
        VideoClip with sharpen effect
    """

    def sharpen_frame(frame):
        if intensity <= 0:
            return frame

        # Simple sharpening using unsharp mask
        blurred = np.stack([gaussian_filter(frame[:, :, i], sigma=1) for i in range(frame.shape[2])], axis=2)

        sharpened = frame + intensity * (frame - blurred)
        return np.clip(sharpened, 0, 255).astype(np.uint8)

    return clip.image_transform(sharpen_frame)


def apply_mirror_x(clip: VideoClip) -> VideoClip:
    """
    Apply horizontal mirror effect to video.

    Args:
        clip: Input VideoClip

    Returns:
        VideoClip with horizontal mirror effect
    """
    return MirrorX(clip)


def apply_mirror_y(clip: VideoClip) -> VideoClip:
    """
    Apply vertical mirror effect to video.

    Args:
        clip: Input VideoClip

    Returns:
        VideoClip with vertical mirror effect
    """
    return MirrorY(clip)


def apply_speed_up(clip: VideoClip, speed_factor: float = 1.5) -> VideoClip:
    """
    Speed up video playback.

    Args:
        clip: Input VideoClip
        speed_factor: Speed multiplier (>1.0 speeds up)

    Returns:
        VideoClip with adjusted speed
    """
    return clip.speedx(speed_factor)


def apply_slow_down(clip: VideoClip, speed_factor: float = 0.5) -> VideoClip:
    """
    Slow down video playback.

    Args:
        clip: Input VideoClip
        speed_factor: Speed multiplier (should be between 0.1 and 1.0)

    Returns:
        VideoClip with adjusted speed
    """
    # Ensure speed_factor is less than 1 for slow down
    if speed_factor > 1.0:
        speed_factor = 1.0 / speed_factor
    return clip.speedx(speed_factor)


def apply_noise(clip: VideoClip, noise_level: float = 0.1) -> VideoClip:
    """
    Add noise to video.

    Args:
        clip: Input VideoClip
        noise_level: Amount of noise (0.0 to 1.0)

    Returns:
        VideoClip with noise effect
    """

    def add_noise(frame):
        if noise_level <= 0:
            return frame

        noise = np.random.randn(*frame.shape) * noise_level * 255
        noisy_frame = frame + noise
        return np.clip(noisy_frame, 0, 255).astype(np.uint8)

    return clip.image_transform(add_noise)


def apply_vignette(clip: VideoClip, intensity: float = 1.0) -> VideoClip:
    """
    Apply vignette effect to video.

    Args:
        clip: Input VideoClip
        intensity: Vignette intensity (0.0 to 1.0+)

    Returns:
        VideoClip with vignette effect
    """
    w, h = clip.size

    # Create vignette mask
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)

    # Radial gradient from center
    radius = np.sqrt(X**2 + Y**2)
    vignette_mask = 1 - np.clip(radius * intensity * 0.7, 0, 1)
    vignette_mask = vignette_mask[:, :, np.newaxis]

    def apply_vignette_frame(frame):
        return np.clip(frame * vignette_mask, 0, 255).astype(np.uint8)

    return clip.image_transform(apply_vignette_frame)


EFFECT_FUNCTIONS = {
    "none": lambda clip, **kwargs: clip,
    "blur": apply_blur,
    "sharpen": apply_sharpen,
    "mirror_x": lambda clip, **kwargs: apply_mirror_x(clip),
    "mirror_y": lambda clip, **kwargs: apply_mirror_y(clip),
    "speed_up": apply_speed_up,
    "slow_down": apply_slow_down,
    "noise": apply_noise,
    "vignette": apply_vignette,
}


def apply_effect(clip: VideoClip, effect_type: str, **kwargs) -> VideoClip:
    """
    Apply an effect to a video clip.

    Args:
        clip: Input VideoClip
        effect_type: Type of effect (from EFFECT_FUNCTIONS keys)
        **kwargs: Additional parameters for the effect

    Returns:
        VideoClip with effect applied

    Raises:
        ValueError: If effect_type is not recognized
    """
    if effect_type not in EFFECT_FUNCTIONS:
        raise ValueError(f"Unknown effect type: {effect_type}")

    return EFFECT_FUNCTIONS[effect_type](clip, **kwargs)
