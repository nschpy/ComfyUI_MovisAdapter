#!/usr/bin/env python

"""Tests for `ComfyUI_MovisAdapter` package."""

import pytest
from unittest.mock import Mock
import numpy as np
import torch

from src.ComfyUI_MovisAdapter.nodes import (
    SaveVideo,
    VideoConcatenate,
    VideoEffects,
    ColorGrading,
    VideoToImages,
    ImagesToVideo,
)
from src.ComfyUI_MovisAdapter.video_types import VideoWrapper


@pytest.fixture
def mock_video_clip():
    """Create a mock VideoClip for testing."""
    mock_clip = Mock()
    mock_clip.duration = 10.0
    mock_clip.fps = 30.0
    mock_clip.size = (1920, 1080)
    mock_clip.w = 1920
    mock_clip.h = 1080
    return mock_clip


@pytest.fixture
def mock_video_wrapper(mock_video_clip):
    """Create a mock VideoWrapper for testing."""
    return VideoWrapper(mock_video_clip)


def test_images_to_video_node_types():
    """Test ImagesToVideo node types."""
    assert ImagesToVideo.RETURN_TYPES == ("VIDEO",)
    assert ImagesToVideo.CATEGORY == "video/moviepy/convert"
    input_types = ImagesToVideo.INPUT_TYPES()
    assert "images" in input_types["required"]
    assert "fps" in input_types["required"]


def test_save_video_node_types():
    """Test SaveVideo node types."""
    assert SaveVideo.RETURN_TYPES == ("STRING",)
    assert SaveVideo.CATEGORY == "video/moviepy/save"
    assert SaveVideo.OUTPUT_NODE is True
    input_types = SaveVideo.INPUT_TYPES()
    assert "video" in input_types["required"]
    assert "filename" in input_types["required"]
    assert "codec" in input_types["required"]


def test_video_concatenate_node_types():
    """Test VideoConcatenate node types."""
    assert VideoConcatenate.RETURN_TYPES == ("VIDEO",)
    assert VideoConcatenate.CATEGORY == "video/moviepy/edit"
    assert VideoConcatenate.INPUT_IS_LIST is True
    input_types = VideoConcatenate.INPUT_TYPES()
    assert "videos" in input_types["required"]
    assert "mode" in input_types["required"]
    assert "transition_type" in input_types["required"]


def test_video_effects_node_types():
    """Test VideoEffects node types."""
    assert VideoEffects.RETURN_TYPES == ("VIDEO",)
    assert VideoEffects.CATEGORY == "video/moviepy/edit"
    input_types = VideoEffects.INPUT_TYPES()
    assert "video" in input_types["required"]
    assert "effect_type" in input_types["required"]
    assert "intensity" in input_types["required"]
    assert "blur_radius" in input_types["optional"]


def test_color_grading_node_types():
    """Test ColorGrading node types."""
    assert ColorGrading.RETURN_TYPES == ("VIDEO",)
    assert ColorGrading.CATEGORY == "video/moviepy/edit"
    input_types = ColorGrading.INPUT_TYPES()
    assert "video" in input_types["required"]
    assert "brightness" in input_types["required"]
    assert "contrast" in input_types["required"]
    assert "saturation" in input_types["required"]
    assert "gamma" in input_types["required"]
    assert "hue_shift" in input_types["required"]


def test_video_to_images_node_types():
    """Test VideoToImages node types."""
    assert VideoToImages.RETURN_TYPES == ("IMAGE",)
    assert VideoToImages.CATEGORY == "video/moviepy/convert"
    input_types = VideoToImages.INPUT_TYPES()
    assert "video" in input_types["required"]
    assert "fps" in input_types["optional"]
    assert "start_time" in input_types["optional"]
    assert "end_time" in input_types["optional"]


def test_video_wrapper_properties(mock_video_clip):
    """Test VideoWrapper properties."""
    wrapper = VideoWrapper(mock_video_clip)
    assert wrapper.duration == 10.0
    assert wrapper.fps == 30.0
    assert wrapper.size == (1920, 1080)
    assert wrapper.w == 1920
    assert wrapper.h == 1080


def test_video_effects_none_effect(mock_video_wrapper):
    """Test VideoEffects with 'none' effect returns unchanged video."""
    node = VideoEffects()
    result = node.apply_effect(mock_video_wrapper, "none", 1.0)
    assert result[0] == mock_video_wrapper


def test_video_to_images_conversion(mock_video_clip):
    """Test VideoToImages basic conversion."""
    # Setup mock to return test frames
    test_frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    mock_video_clip.get_frame = Mock(return_value=test_frame)

    wrapper = VideoWrapper(mock_video_clip)
    node = VideoToImages()

    # Convert first second of video
    result = node.convert_to_images(wrapper, fps=5.0, start_time=0.0, end_time=1.0)

    # Should return a tensor
    assert isinstance(result[0], torch.Tensor)
    # Should have 5 frames (1 second at 5 fps)
    assert result[0].shape[0] == 5
    # Should preserve resolution
    assert result[0].shape[1:] == (1080, 1920, 3)


def test_images_to_video_conversion():
    """Test ImagesToVideo basic conversion."""
    # Create test images tensor [B, H, W, C] with values in [0, 1]
    batch_size = 10
    height, width, channels = 1080, 1920, 3
    test_images = torch.rand(batch_size, height, width, channels)

    node = ImagesToVideo()
    result = node.convert_to_video(test_images, fps=24.0)

    # Should return VideoWrapper
    assert isinstance(result[0], VideoWrapper)
    # Should have correct duration (10 frames at 24 fps = 10/24 seconds)
    assert abs(result[0].duration - (batch_size / 24.0)) < 0.01
    # Should have correct FPS
    assert result[0].fps == 24.0
    # Should preserve resolution
    assert result[0].size == (width, height)
