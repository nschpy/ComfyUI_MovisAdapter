"""
Color grading functions for ComfyUI MoviePy integration.
"""

from moviepy.video.VideoClip import VideoClip
import numpy as np
import colorsys


def adjust_brightness(frame: np.ndarray, brightness: float) -> np.ndarray:
    """
    Adjust brightness of a frame.

    Args:
        frame: Input frame (numpy array)
        brightness: Brightness adjustment (-1.0 to 1.0)

    Returns:
        Adjusted frame
    """
    if brightness == 0:
        return frame

    adjustment = brightness * 255
    return np.clip(frame.astype(np.float32) + adjustment, 0, 255).astype(np.uint8)


def adjust_contrast(frame: np.ndarray, contrast: float) -> np.ndarray:
    """
    Adjust contrast of a frame.

    Args:
        frame: Input frame (numpy array)
        contrast: Contrast adjustment (-1.0 to 1.0)

    Returns:
        Adjusted frame
    """
    if contrast == 0:
        return frame

    # Convert contrast range from [-1, 1] to [0, 2]
    factor = 1.0 + contrast

    # Apply contrast adjustment
    mean = np.mean(frame)
    adjusted = (frame.astype(np.float32) - mean) * factor + mean

    return np.clip(adjusted, 0, 255).astype(np.uint8)


def adjust_saturation(frame: np.ndarray, saturation: float) -> np.ndarray:
    """
    Adjust saturation of a frame.

    Args:
        frame: Input frame (numpy array)
        saturation: Saturation adjustment (-1.0 to 1.0)

    Returns:
        Adjusted frame
    """
    if saturation == 0:
        return frame

    # Convert to HSV
    frame_float = frame.astype(np.float32) / 255.0
    hsv = np.array([colorsys.rgb_to_hsv(r, g, b) for r, g, b in frame_float.reshape(-1, 3)])
    hsv = hsv.reshape(frame.shape)

    # Adjust saturation
    factor = 1.0 + saturation
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 1)

    # Convert back to RGB
    rgb = np.array([colorsys.hsv_to_rgb(h, s, v) for h, s, v in hsv.reshape(-1, 3)])
    rgb = rgb.reshape(frame.shape)

    return (rgb * 255).astype(np.uint8)


def adjust_gamma(frame: np.ndarray, gamma: float) -> np.ndarray:
    """
    Apply gamma correction to a frame.

    Args:
        frame: Input frame (numpy array)
        gamma: Gamma value (0.1 to 3.0, 1.0 is neutral)

    Returns:
        Adjusted frame
    """
    if gamma == 1.0:
        return frame

    # Normalize to [0, 1]
    frame_float = frame.astype(np.float32) / 255.0

    # Apply gamma correction
    corrected = np.power(frame_float, 1.0 / gamma)

    return (corrected * 255).astype(np.uint8)


def adjust_hue(frame: np.ndarray, hue_shift: float) -> np.ndarray:
    """
    Shift hue of a frame.

    Args:
        frame: Input frame (numpy array)
        hue_shift: Hue shift in degrees (-180 to 180)

    Returns:
        Adjusted frame
    """
    if hue_shift == 0:
        return frame

    # Convert to HSV
    frame_float = frame.astype(np.float32) / 255.0
    hsv = np.array([colorsys.rgb_to_hsv(r, g, b) for r, g, b in frame_float.reshape(-1, 3)])
    hsv = hsv.reshape(frame.shape)

    # Shift hue (hue is in [0, 1] range in colorsys)
    hue_shift_normalized = (hue_shift / 360.0) % 1.0
    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift_normalized) % 1.0

    # Convert back to RGB
    rgb = np.array([colorsys.hsv_to_rgb(h, s, v) for h, s, v in hsv.reshape(-1, 3)])
    rgb = rgb.reshape(frame.shape)

    return (rgb * 255).astype(np.uint8)


def apply_color_grading(
    clip: VideoClip, brightness: float = 0.0, contrast: float = 0.0, saturation: float = 0.0, gamma: float = 1.0, hue_shift: float = 0.0
) -> VideoClip:
    """
    Apply color grading to a video clip.

    All adjustments are applied in a single pass for efficiency.

    Args:
        clip: Input VideoClip
        brightness: Brightness adjustment (-1.0 to 1.0, 0.0 is neutral)
        contrast: Contrast adjustment (-1.0 to 1.0, 0.0 is neutral)
        saturation: Saturation adjustment (-1.0 to 1.0, 0.0 is neutral)
        gamma: Gamma correction (0.1 to 3.0, 1.0 is neutral)
        hue_shift: Hue shift in degrees (-180 to 180, 0 is neutral)

    Returns:
        VideoClip with color grading applied
    """
    # Check if any adjustment is needed
    if brightness == 0.0 and contrast == 0.0 and saturation == 0.0 and gamma == 1.0 and hue_shift == 0.0:
        return clip

    def color_grade_frame(frame):
        """Apply all color grading adjustments to a single frame."""
        result = frame.copy()

        # Apply adjustments in order
        if brightness != 0.0:
            result = adjust_brightness(result, brightness)

        if contrast != 0.0:
            result = adjust_contrast(result, contrast)

        if gamma != 1.0:
            result = adjust_gamma(result, gamma)

        if saturation != 0.0 or hue_shift != 0.0:
            # Both saturation and hue require HSV conversion
            # so we do them together for efficiency
            frame_float = result.astype(np.float32) / 255.0

            # Convert to HSV
            hsv = np.zeros_like(frame_float)
            for i in range(frame_float.shape[0]):
                for j in range(frame_float.shape[1]):
                    r, g, b = frame_float[i, j]
                    h, s, v = colorsys.rgb_to_hsv(r, g, b)

                    # Apply saturation
                    if saturation != 0.0:
                        s = np.clip(s * (1.0 + saturation), 0, 1)

                    # Apply hue shift
                    if hue_shift != 0.0:
                        h = (h + hue_shift / 360.0) % 1.0

                    # Convert back to RGB
                    r, g, b = colorsys.hsv_to_rgb(h, s, v)
                    hsv[i, j] = [r, g, b]

            result = (hsv * 255).astype(np.uint8)

        return result

    return clip.fl_image(color_grade_frame)
