"""TextOverlay node - Adds text overlay to video clips."""

from moviepy import TextClip, CompositeVideoClip
from ...common import image_tensor_to_moviepy_clip, moviepy_clip_to_image_tensor


class MPATextOverlay:
    """
    Adds text overlay to a video clip.
    
    This node adds text on top of the video at specified positions.
    Supports all TextClip properties including fonts, colors, alignment,
    margins, strokes, and more.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IMAGE": ("IMAGE",),
                "text": ("STRING", {
                    "default": "Sample Text",
                    "multiline": True,
                    "display": "text"
                }),
                "position": (["top", "center", "bottom"], {
                    "default": "center"
                }),
                "fps": ("FLOAT", {
                    "default": 24.0,
                    "min": 1.0,
                    "max": 120.0,
                    "step": 0.1,
                    "display": "number"
                }),
                "font": ("STRING", {
                    "default": "",
                    "display": "text"
                }),
                "font_size": ("INT", {
                    "default": 50,
                    "min": 1,
                    "max": 500,
                    "step": 1,
                    "display": "number"
                }),
                "margin": ("STRING", {
                    "default": "16,16",
                    "display": "text",
                    "tooltip": "Margin as 'horizontal,vertical' or 'left,top,right,bottom'. Empty for no margin."
                }),
                "color": ("STRING", {
                    "default": "black",
                    "display": "text",
                    "tooltip": "Text color: color name, hex (#RRGGBB), or RGB tuple as 'R,G,B'"
                }),
                "bg_color": ("STRING", {
                    "default": "",
                    "display": "text",
                    "tooltip": "Background color: color name, hex (#RRGGBB), or RGB tuple as 'R,G,B'. Empty for transparent."
                }),
                "stroke_color": ("STRING", {
                    "default": "",
                    "display": "text",
                    "tooltip": "Stroke color: color name, hex (#RRGGBB), or RGB tuple as 'R,G,B'. Empty for no stroke."
                }),
                "stroke_width": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 50,
                    "step": 1,
                    "display": "number"
                }),
                "method": (["label", "caption"], {
                    "default": "caption",
                    "display": "dropdown"
                }),
                "text_align": (["left", "center", "right"], {
                    "default": "left",
                    "display": "dropdown"
                }),
                "horizontal_align": (["left", "center", "right"], {
                    "default": "center",
                    "display": "dropdown"
                }),
                "vertical_align": (["top", "center", "bottom"], {
                    "default": "center",
                    "display": "dropdown"
                }),
                "interline": ("FLOAT", {
                    "default": 4.0,
                    "min": 0.0,
                    "max": 50.0,
                    "step": 0.1,
                    "display": "number"
                }),
                "transparent": ("BOOLEAN", {
                    "default": True,
                    "display": "boolean"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("video_with_text",)
    FUNCTION = "add_text_overlay"
    CATEGORY = "MPA/video"
    
    def _parse_margin(self, margin_str):
        """Parse margin string to tuple or None."""
        if not margin_str or margin_str.strip() == "":
            return None
        
        try:
            parts = [p.strip() for p in margin_str.split(',')]
            if len(parts) == 2:
                return (int(parts[0]), int(parts[1]))
            elif len(parts) == 4:
                return (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
            else:
                return (None, None)
        except (ValueError, IndexError):
            pass
        
        return None
    
    def _parse_color(self, color_str):
        """Parse color string to appropriate format."""
        if not color_str or color_str.strip() == "":
            return None
        
        color_str = color_str.strip()
        
        # Check if it's a tuple format "R,G,B" or "R,G,B,A"
        if ',' in color_str:
            try:
                parts = [int(p.strip()) for p in color_str.split(',')]
                if len(parts) == 3:
                    return tuple(parts)
                elif len(parts) == 4:
                    return tuple(parts)
            except ValueError:
                pass
        
        # Return as-is (color name or hex)
        return color_str
    
    def add_text_overlay(
        self, IMAGE, text, position, fps,
        font="", font_size=50, size="", margin="",
        color="black", bg_color="", stroke_color="", stroke_width=0,
        method="caption", text_align="left", horizontal_align="center",
        vertical_align="center", interline=4.0, transparent=True
    ):
        """
        Add text overlay to video with full TextClip property support.
        
        Args:
            IMAGE: Input video as IMAGE tensor
            text: Text string to display
            position: Position of text ("top", "center", or "bottom")
            fps: Frames per second for the video
            font: Path to font file (empty for default)
            font_size: Font size in points
            size: Size as 'width,height' or 'width,None' (empty for auto)
            margin: Margin as 'h,v' or 'left,top,right,bottom' (empty for none)
            color: Text color (color name, hex, or 'R,G,B' tuple)
            bg_color: Background color (empty for transparent)
            stroke_color: Stroke color (empty for no stroke)
            stroke_width: Stroke width in pixels
            method: 'label' (auto-size) or 'caption' (fixed size with wrapping)
            text_align: Text alignment within lines ('left', 'center', 'right')
            horizontal_align: Horizontal alignment of text block ('left', 'center', 'right')
            vertical_align: Vertical alignment of text block ('top', 'center', 'bottom')
            interline: Line spacing
            transparent: Whether to support transparency
            
        Returns:
            Tuple containing the video with text overlay as IMAGE tensor
        """
        # Convert IMAGE tensor to MoviePy clip
        video_clip = image_tensor_to_moviepy_clip(IMAGE, fps=fps)
        
        # Get video dimensions
        video_width, video_height = video_clip.size
        
        # Build TextClip parameters
        text_clip_params = {}
        
        # Text source
        text_clip_params['text'] = text
        
        # Font
        if font and font.strip():
            text_clip_params['font'] = font
        
        # Font size
        if font_size and font_size > 0:
            text_clip_params['font_size'] = font_size
        
        # Size
        text_clip_params['size'] = (video_width, video_height)
        
        # Margin
        parsed_margin = self._parse_margin(margin)
        if parsed_margin:
            text_clip_params['margin'] = parsed_margin
        
        # Color
        parsed_color = self._parse_color(color)
        if parsed_color:
            text_clip_params['color'] = parsed_color
        
        # Background color
        parsed_bg_color = self._parse_color(bg_color)
        if parsed_bg_color:
            text_clip_params['bg_color'] = parsed_bg_color
        
        # Stroke
        parsed_stroke_color = self._parse_color(stroke_color)
        if parsed_stroke_color and stroke_width > 0:
            text_clip_params['stroke_color'] = parsed_stroke_color
            text_clip_params['stroke_width'] = stroke_width
        
        # Method
        text_clip_params['method'] = method
        
        # Text alignment
        text_clip_params['text_align'] = text_align
        
        # Horizontal and vertical alignment
        text_clip_params['horizontal_align'] = horizontal_align
        text_clip_params['vertical_align'] = vertical_align
        
        # Interline
        if interline is not None:
            text_clip_params['interline'] = interline
        
        # Transparency
        text_clip_params['transparent'] = transparent
        
        # Create text clip
        text_clip = TextClip(**text_clip_params).with_duration(video_clip.duration)
        
        # Calculate position based on selected position and alignment settings
        # Position parameter controls vertical placement, horizontal_align controls horizontal
        if position == "top":
            v_pos = 20  # Small margin from top
        elif position == "center":
            v_pos = 'center'
        elif position == "bottom":
            text_height = text_clip.size[1]
            v_pos = video_height - text_height - 20  # Small margin from bottom
        else:
            # Fallback: use vertical_align setting
            v_pos = vertical_align if vertical_align != 'center' else 'center'
        
        # Horizontal position uses horizontal_align setting
        h_pos = horizontal_align if horizontal_align != 'center' else 'center'
        text_position = (h_pos, v_pos)
        
        # Set text position
        text_clip = text_clip.with_position(text_position)
        
        # Composite text over video
        final_clip = CompositeVideoClip([video_clip, text_clip])
        
        # Convert back to IMAGE tensor
        result_tensor = moviepy_clip_to_image_tensor(final_clip)
        
        return (result_tensor,)

