# MovisAdapter

MoviePy integration for ComfyUI - Professional video editing nodes for ComfyUI workflows.

> [!NOTE]
> This project provides a comprehensive set of custom nodes for video editing using MoviePy library, enabling video concatenation, effects, color grading, and more within ComfyUI.

## Quickstart

1. Install [ComfyUI](https://docs.comfy.org/get_started).
2. Install [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
3. Look up this extension in ComfyUI-Manager. If you are installing manually, clone this repository under `ComfyUI/custom_nodes`.
4. Install dependencies: `pip install -e .` (from the extension directory)
5. Restart ComfyUI.

## Features

### Video Loading & Saving
- **Load Video**: Load video files from disk with optional audio
- **Save Video**: Export videos with configurable codecs, bitrates, and presets

### Video Editing
- **Concatenate Videos**: Merge multiple videos with advanced transitions
  - Transition types: crossfade, fade to black/white, slide left/right, zoom in/out
  - Automatic FPS and resolution normalization

### Video Effects
- **Blur**: Gaussian blur with adjustable radius
- **Sharpen**: Enhance image sharpness
- **Mirror X/Y**: Horizontal and vertical mirroring
- **Speed Up/Slow Down**: Adjust playback speed
- **Noise**: Add film grain effect
- **Vignette**: Apply edge darkening

### Color Grading
- **Brightness**: Adjust overall luminosity
- **Contrast**: Enhance or reduce contrast
- **Saturation**: Control color intensity
- **Gamma**: Apply gamma correction
- **Hue Shift**: Rotate color spectrum

### Video Conversion
- **Video to Images**: Extract frames as IMAGE tensors for further processing in ComfyUI

## Develop

To install the dev dependencies and pre-commit (will run the ruff hook), do:

```bash
cd ComfyUI_MovisAdapter
pip install -e .[dev]
pre-commit install
```

The `-e` flag above will result in a "live" install, in the sense that any changes you make to your node extension will automatically be picked up the next time you run ComfyUI.

## Publish to Github

Install Github Desktop or follow these [instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) for ssh.

1. Create a Github repository that matches the directory name. 
2. Push the files to Git
```
git add .
git commit -m "project scaffolding"
git push
``` 

## Node Categories

All nodes are organized under `video/moviepy/` category:

- **video/moviepy/load**: LoadVideo
- **video/moviepy/edit**: VideoConcatenate, VideoEffects, ColorGrading
- **video/moviepy/convert**: VideoToImages
- **video/moviepy/save**: SaveVideo

## Usage Examples

### Basic Video Processing Workflow

1. **Load Video** → Set path to your video file
2. **Video Effects** → Apply blur, sharpen, or other effects
3. **Color Grading** → Adjust brightness, contrast, saturation
4. **Save Video** → Export the processed video

### Concatenate Multiple Videos

1. **Load Video** (×N) → Load multiple video clips
2. **Concatenate Videos** → Set mode to "transition", choose transition type
3. **Save Video** → Export final concatenated video

### Extract Frames for Further Processing

1. **Load Video** → Load source video
2. **Video to Images** → Convert to IMAGE frames
3. Use any ComfyUI image processing nodes
4. (Optional) Convert back to video using ComfyUI video nodes

## Technical Details

### Custom Data Types

- **VIDEO**: Custom wrapper around MoviePy's VideoClip for efficient video handling
- Supports both file paths (STRING) and VIDEO objects for flexibility
- Automatic parameter normalization (FPS, resolution) during concatenation

### Supported Transitions

- `none`: Simple concatenation
- `crossfade`: Smooth blend between clips
- `fade_black`: Fade through black
- `fade_white`: Fade through white
- `slide_left`: Slide transition to the left
- `slide_right`: Slide transition to the right
- `zoom_in`: Zoom-based transition
- `zoom_out`: Zoom-out transition

### Dependencies

- `moviepy`: Core video processing library
- `scipy`: For advanced image filters
- `numpy`: Array operations (included with MoviePy)
- `torch`: Tensor operations (provided by ComfyUI)

## Writing custom nodes

The implementation is located in [nodes.py](src/ComfyUI_MovisAdapter/nodes.py). To learn more about ComfyUI custom nodes, read the [docs](https://docs.comfy.org/essentials/custom_node_overview).


## Tests

This repo contains unit tests written in Pytest in the `tests/` directory. It is recommended to unit test your custom node.

- [build-pipeline.yml](.github/workflows/build-pipeline.yml) will run pytest and linter on any open PRs
- [validate.yml](.github/workflows/validate.yml) will run [node-diff](https://github.com/Comfy-Org/node-diff) to check for breaking changes

## Publishing to Registry

If you wish to share this custom node with others in the community, you can publish it to the registry. We've already auto-populated some fields in `pyproject.toml` under `tool.comfy`, but please double-check that they are correct.

You need to make an account on https://registry.comfy.org and create an API key token.

- [ ] Go to the [registry](https://registry.comfy.org). Login and create a publisher id (everything after the `@` sign on your registry profile). 
- [ ] Add the publisher id into the pyproject.toml file.
- [ ] Create an api key on the Registry for publishing from Github. [Instructions](https://docs.comfy.org/registry/publishing#create-an-api-key-for-publishing).
- [ ] Add it to your Github Repository Secrets as `REGISTRY_ACCESS_TOKEN`.

A Github action will run on every git push. You can also run the Github action manually. Full instructions [here](https://docs.comfy.org/registry/publishing). Join our [discord](https://discord.com/invite/comfyorg) if you have any questions!
