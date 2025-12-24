"""Common utilities for MoviePy Adapter nodes."""

import torch
import numpy as np
from moviepy import ImageSequenceClip


def image_tensor_to_moviepy_clip(tensor: torch.Tensor, fps: float = 24.0) -> ImageSequenceClip:
    """
    Convert ComfyUI IMAGE tensor to MoviePy VideoClip.
    
    Args:
        tensor: torch.Tensor with shape [B, H, W, C] where B is number of frames
                Values should be in range [0.0, 1.0]
        fps: Frames per second for the video clip
        
    Returns:
        ImageSequenceClip: MoviePy video clip
    """
    if tensor is None or tensor.numel() == 0:
        raise ValueError("Input tensor is empty or None")
    
    if len(tensor.shape) != 4:
        raise ValueError(f"Expected tensor with shape [B, H, W, C], got {tensor.shape}")
    
    # Convert from torch tensor to numpy array
    # ComfyUI uses [0, 1] range, MoviePy expects [0, 255]
    frames_numpy = tensor.cpu().numpy()
    frames_numpy = (frames_numpy * 255).astype(np.uint8)
    
    # Convert to list of frames for ImageSequenceClip
    frames_list = [frame for frame in frames_numpy]
    
    # Create MoviePy clip
    clip = ImageSequenceClip(frames_list, fps=fps)
    
    return clip


def moviepy_clip_to_image_tensor(clip) -> torch.Tensor:
    """
    Convert MoviePy VideoClip to ComfyUI IMAGE tensor.
    
    Args:
        clip: MoviePy VideoClip or ImageSequenceClip
        
    Returns:
        torch.Tensor: Tensor with shape [B, H, W, C] where B is number of frames
                      Values in range [0.0, 1.0]
    """
    if clip is None:
        raise ValueError("Input clip is None")
    
    # Get frames from clip
    # iter_frames returns frames as numpy arrays in [0, 255] range
    frames_list = []
    for frame in clip.iter_frames():
        frames_list.append(frame)
    
    if not frames_list:
        raise ValueError("Clip contains no frames")
    
    # Stack frames into numpy array
    frames_numpy = np.stack(frames_list, axis=0)
    
    # Convert from [0, 255] to [0, 1] range for ComfyUI
    frames_numpy = frames_numpy.astype(np.float32) / 255.0
    
    # Convert to torch tensor
    tensor = torch.from_numpy(frames_numpy)
    
    return tensor


def resize_clip_to_resolution(clip, target_width: int, target_height: int):
    """
    Resize MoviePy clip to target resolution.
    
    Args:
        clip: MoviePy VideoClip
        target_width: Target width in pixels
        target_height: Target height in pixels
        
    Returns:
        Resized MoviePy VideoClip
    """
    if clip is None:
        raise ValueError("Input clip is None")
    
    if target_width <= 0 or target_height <= 0:
        raise ValueError(f"Invalid target resolution: {target_width}x{target_height}")
    
    # Use MoviePy's resize method
    resized_clip = clip.resize(newsize=(target_width, target_height))
    
    return resized_clip

