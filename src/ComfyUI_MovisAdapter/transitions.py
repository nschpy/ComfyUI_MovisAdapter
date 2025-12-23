"""
Video transition effects for ComfyUI MoviePy integration.
"""

from typing import List
from moviepy import concatenate_videoclips, CompositeVideoClip
from moviepy.video.VideoClip import VideoClip


def apply_crossfade(clips: List[VideoClip], duration: float) -> VideoClip:
    """
    Apply crossfade transition between clips.

    Args:
        clips: List of VideoClip objects
        duration: Transition duration in seconds

    Returns:
        Concatenated VideoClip with crossfade transitions
    """
    if len(clips) <= 1:
        return clips[0] if clips else None

    result_clips = []

    for i, clip in enumerate(clips):
        if i == 0:
            # First clip: fade out at the end
            result_clips.append(clip.crossfadeout(duration))
        elif i == len(clips) - 1:
            # Last clip: fade in at the start
            result_clips.append(clip.crossfadein(duration))
        else:
            # Middle clips: fade in and out
            result_clips.append(clip.crossfadein(duration).crossfadeout(duration))

    return concatenate_videoclips(result_clips, padding=-duration)


def apply_fade_black(clips: List[VideoClip], duration: float) -> VideoClip:
    """
    Apply fade to/from black transition between clips.

    Args:
        clips: List of VideoClip objects
        duration: Transition duration in seconds

    Returns:
        Concatenated VideoClip with fade to black transitions
    """
    result_clips = []

    for i, clip in enumerate(clips):
        # Fade out to black at the end
        clip_with_fade = clip.fadeout(duration, final_color=[0, 0, 0])

        if i < len(clips) - 1:
            result_clips.append(clip_with_fade)
        else:
            # Last clip doesn't need fade out
            result_clips.append(clip)

        # Add fade in from black for all clips except the first
        if i > 0:
            result_clips[-1] = result_clips[-1].fadein(duration, initial_color=[0, 0, 0])

    return concatenate_videoclips(result_clips)


def apply_fade_white(clips: List[VideoClip], duration: float) -> VideoClip:
    """
    Apply fade to/from white transition between clips.

    Args:
        clips: List of VideoClip objects
        duration: Transition duration in seconds

    Returns:
        Concatenated VideoClip with fade to white transitions
    """
    result_clips = []

    for i, clip in enumerate(clips):
        # Fade out to white at the end
        clip_with_fade = clip.fadeout(duration, final_color=[255, 255, 255])

        if i < len(clips) - 1:
            result_clips.append(clip_with_fade)
        else:
            # Last clip doesn't need fade out
            result_clips.append(clip)

        # Add fade in from white for all clips except the first
        if i > 0:
            result_clips[-1] = result_clips[-1].fadein(duration, initial_color=[255, 255, 255])

    return concatenate_videoclips(result_clips)


def apply_slide_left(clips: List[VideoClip], duration: float) -> VideoClip:
    """
    Apply slide left transition between clips.

    Args:
        clips: List of VideoClip objects
        duration: Transition duration in seconds

    Returns:
        Concatenated VideoClip with slide left transitions
    """
    if len(clips) <= 1:
        return clips[0] if clips else None

    result_clips = []

    for i in range(len(clips)):
        clip = clips[i]

        if i < len(clips) - 1:
            next_clip = clips[i + 1]

            # Create transition segment
            w, h = clip.size

            # Outgoing clip slides left
            outgoing = clip.subclip(clip.duration - duration, clip.duration)
            outgoing = outgoing.set_position(lambda t: (-w * t / duration, 0))

            # Incoming clip slides in from right
            incoming = next_clip.subclip(0, duration)
            incoming = incoming.set_position(lambda t: (w - w * t / duration, 0))

            # Composite the transition
            transition = CompositeVideoClip([outgoing, incoming], size=clip.size).set_duration(duration)

            # Add the main part of the clip (without transition)
            if clip.duration > duration:
                result_clips.append(clip.subclip(0, clip.duration - duration))
            result_clips.append(transition)

        # Add the last clip's remaining part
        if i == len(clips) - 1 and clip.duration > duration:
            result_clips.append(clip.subclip(duration, clip.duration))

    return concatenate_videoclips(result_clips)


def apply_slide_right(clips: List[VideoClip], duration: float) -> VideoClip:
    """
    Apply slide right transition between clips.

    Args:
        clips: List of VideoClip objects
        duration: Transition duration in seconds

    Returns:
        Concatenated VideoClip with slide right transitions
    """
    if len(clips) <= 1:
        return clips[0] if clips else None

    result_clips = []

    for i in range(len(clips)):
        clip = clips[i]

        if i < len(clips) - 1:
            next_clip = clips[i + 1]

            # Create transition segment
            w, h = clip.size

            # Outgoing clip slides right
            outgoing = clip.subclip(clip.duration - duration, clip.duration)
            outgoing = outgoing.set_position(lambda t: (w * t / duration, 0))

            # Incoming clip slides in from left
            incoming = next_clip.subclip(0, duration)
            incoming = incoming.set_position(lambda t: (-w + w * t / duration, 0))

            # Composite the transition
            transition = CompositeVideoClip([outgoing, incoming], size=clip.size).set_duration(duration)

            # Add the main part of the clip (without transition)
            if clip.duration > duration:
                result_clips.append(clip.subclip(0, clip.duration - duration))
            result_clips.append(transition)

        # Add the last clip's remaining part
        if i == len(clips) - 1 and clip.duration > duration:
            result_clips.append(clip.subclip(duration, clip.duration))

    return concatenate_videoclips(result_clips)


def apply_zoom_in(clips: List[VideoClip], duration: float) -> VideoClip:
    """
    Apply zoom in transition between clips.

    Args:
        clips: List of VideoClip objects
        duration: Transition duration in seconds

    Returns:
        Concatenated VideoClip with zoom in transitions
    """
    result_clips = []

    for i, clip in enumerate(clips):
        if i < len(clips) - 1:
            # Add main part without transition
            if clip.duration > duration:
                result_clips.append(clip.subclip(0, clip.duration - duration))

            # Zoom in transition (simplified to crossfade for now)
            transition_clip = clip.subclip(max(0, clip.duration - duration), clip.duration)
            result_clips.append(transition_clip.crossfadeout(duration))

            # Next clip fades in
            next_clip = clips[i + 1]
            result_clips.append(next_clip.crossfadein(duration))
        elif i == len(clips) - 1:
            # Last clip
            result_clips.append(clip)

    return concatenate_videoclips(result_clips, padding=-duration)


def apply_zoom_out(clips: List[VideoClip], duration: float) -> VideoClip:
    """
    Apply zoom out transition between clips.

    Args:
        clips: List of VideoClip objects
        duration: Transition duration in seconds

    Returns:
        Concatenated VideoClip with zoom out transitions
    """
    result_clips = []

    for i, clip in enumerate(clips):
        if i < len(clips) - 1:
            # Add main part without transition
            if clip.duration > duration:
                result_clips.append(clip.subclip(0, clip.duration - duration))

            # Zoom out transition (just use crossfade for simplicity)
            transition_clip = clip.subclip(max(0, clip.duration - duration), clip.duration)
            result_clips.append(transition_clip.crossfadeout(duration))

            # Next clip fades in
            next_clip = clips[i + 1]
            result_clips.append(next_clip.crossfadein(duration))
        elif i == len(clips) - 1:
            # Last clip
            result_clips.append(clip)

    return concatenate_videoclips(result_clips, padding=-duration)


TRANSITION_FUNCTIONS = {
    "none": lambda clips, duration: concatenate_videoclips(clips),
    "crossfade": apply_crossfade,
    "fade_black": apply_fade_black,
    "fade_white": apply_fade_white,
    "slide_left": apply_slide_left,
    "slide_right": apply_slide_right,
    "zoom_in": apply_zoom_in,
    "zoom_out": apply_zoom_out,
}


def apply_transition(clips: List[VideoClip], transition_type: str, duration: float) -> VideoClip:
    """
    Apply a transition between video clips.

    Args:
        clips: List of VideoClip objects
        transition_type: Type of transition (from TRANSITION_FUNCTIONS keys)
        duration: Transition duration in seconds

    Returns:
        Concatenated VideoClip with transitions applied

    Raises:
        ValueError: If transition_type is not recognized
    """
    if transition_type not in TRANSITION_FUNCTIONS:
        raise ValueError(f"Unknown transition type: {transition_type}")

    return TRANSITION_FUNCTIONS[transition_type](clips, duration)
