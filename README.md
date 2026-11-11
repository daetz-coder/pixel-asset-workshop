# Pixel Asset Workshop

[Chinese](README.zh.md) · [Tiny Swords case study](examples/tiny-swords/README.md) · [Live showcase](https://daetz-coder.github.io/projects/pixel-asset-workshop/) · [Contributing](CONTRIBUTING.md)

Extract reusable art direction from a reference game, create original characters and scenery, and animate several characters in a single video. Export each character as a separate transparent PNG sequence. The workflow is intended for indie teams expanding a roster, testing an art direction, or producing repeated animation batches.

[![Godot training-ground screenshot with the original Tiny Swords units above the generated units](examples/tiny-swords/preview/training-ground.png)](https://daetz-coder.github.io/projects/pixel-asset-workshop/showcase/godot.html)

The five-second Godot 4.5.1 recording shows the original Tiny Swords units idling above the six generated units. Tiny Swords art by [Pixel Frog](https://pixelfrog-assets.itch.io/tiny-swords). [Play the recording](https://daetz-coder.github.io/projects/pixel-asset-workshop/showcase/godot.html) · [MP4 file](examples/tiny-swords/preview/training-ground.mp4) · [Run the Godot comparison](examples/tiny-swords/README.md#compare-the-original-in-godot)

[Watch the 21.5-second workflow walkthrough](https://daetz-coder.github.io/projects/pixel-asset-workshop/showcase/godot.html#workflow-video)

| Stage | Workflow | Output |
| --- | --- | --- |
| 1. Learn the style | Record camera angle, body proportions, pixel scale and material colors. Calibrate one sprite, then apply the rules to characters, buildings, terrain and UI. | Style profile, side-by-side comparison and an approved sample |
| 2. Generate and compose | Create a transparent PNG for each character. Pack compatible sprites into a shared first frame with a common foot baseline and a motion prompt for each cell. | First-frame PNG, per-cell prompts and layout JSON |
| 3. Generate video and extract frames | Submit one clip per batch, using Wan3.0 Video Prime as an example. Map the layout to the actual video size, sample frames, key out the background and review the results. | RGBA PNG sequences with sampling and edge-contact metadata |

The included example uses **six units, one five-second Wan clip and 300 candidate frames**. At the same duration and resolution, batching takes one submission for the six units. Pricing and retries determine the actual cost. Start with idle or walk cycles. Wide swings, projectiles and large effects may need more space per character.

## Exported sprites

The Warhammer Infantry sprite sheet and GIF use the same 12 frames. Read the sheet from left to right, then top to bottom. The GIF displays each frame for 200 ms.

[![Warhammer Infantry sprite sheet with 12 poses](examples/tiny-swords/preview/exports/warhammer-sheet.png)](examples/tiny-swords/preview/exports/warhammer-sheet.png)

![Warhammer Infantry hammer strike GIF](examples/tiny-swords/preview/exports/warhammer.gif)

[All six PNG sheets and GIFs](https://daetz-coder.github.io/projects/pixel-asset-workshop/showcase/spriteframe.html#exports) · [Frame coordinates, anchors and durations](examples/tiny-swords/preview/exports/manifest.json)

## Reproduce the example offline

Install Python 3.10+ and FFmpeg with ffprobe. Install ImageMagick 7 (`magick`) to compose new first frames or validate a Wan request locally. Run the following from the repository root.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt

python scripts/extract_frames.py \
  --video assets/video-inputs/blue-units-3x2-wan-prime-480p.mp4 \
  --layout examples/tiny-swords/wan-layout.json \
  --fps 10 --despill-magenta --out work/tiny-swords/frames
```

Use `--despill-magenta` for this magenta-keyed clip to reduce compression spill at the sprite edges. The output lives in `work/tiny-swords/frames/`, with paths such as `r01c01/attack/0000.png`. The `manifest.json` records the names, cells, fixed canvases, foot anchors, and empty or edge-touching frames. The historical layout uses the `attack` label for a clip that mixes idle, walking and skills. Review the 50 frames in each sequence and split them by action before importing them into a game.

## Create a batch with your own sprites

1. Build a style profile and compare one new sprite with a reference at the same body scale. Once the sample is approved, generate the remaining transparent PNGs. GPT Image or another image generator with reference-image support can handle this step. [Reference art skill](skills/reference-game-characters/SKILL.en.md) · [Tiny Swords comparison](examples/tiny-swords/README.md#comparison-with-the-original)
2. Copy the sample config and change the paths, names and motions. Image paths are relative to the config file. Characters fill the grid left to right, then top to bottom. [Walk batch config](examples/tiny-swords/batch-walk.json)

   ```sh
   python skills/wan-prime-video/scripts/compose_reference.py \
     --config examples/tiny-swords/batch-walk.json \
     --output work/tiny-swords/walk.png
   ```

   This produces `walk.png`, `walk-prompt.txt` and `walk-layout.json` for a new walk batch.
3. Submit the first frame and prompt in a video model's interface or use the Wan runner. After generation, pair the new MP4 with its own layout JSON for command-line extraction or visual review in SpriteFrame. [Wan skill](skills/wan-prime-video/SKILL.md) · [Integrations and layout format](docs/integrations.en.md) · [SpriteFrame on GitHub](https://github.com/daetz-coder/SpriteFrame)

## Resources

| Resource | Use |
| --- | --- |
| [Live showcase](https://daetz-coder.github.io/projects/pixel-asset-workshop/) | Open `index.html` from a local checkout to browse the workflow, SpriteFrame captures and Godot playback |
| [Tiny Swords case study](examples/tiny-swords/README.md) | Get the tested clip and layout, and reproduce the original-versus-generated review |
| [Reference art skill](skills/reference-game-characters/SKILL.en.md) | Reuse art direction, prompts and reference-frame comparison tools |
| [Wan batch skill](skills/wan-prime-video/SKILL.md) | Compose the first frame, prompt and layout, with optional Wan submission |
| [Frame extraction CLI](scripts/extract_frames.py) | Reproduce the export locally without a model account |
| [Integration guide](docs/integrations.en.md) | Use SpriteFrame, swap video providers or automate the workflow |

To use a skill in a tool that supports Agent Skills, copy its entire directory into that tool's skills directory. You can also run the scripts directly.

## Contributing

Bug reports and pull requests are welcome. For a cropping or frame extraction issue, include the command, the layout JSON and the affected frame numbers. [Open an issue](https://github.com/daetz-coder/pixel-asset-workshop/issues/new/choose) · [Contributing guide](CONTRIBUTING.md) · [Offline workflow checks](https://github.com/daetz-coder/pixel-asset-workshop/actions/workflows/ci.yml)

## Sources and distribution

Pixel Frog's Tiny Swords is the style reference. The training-ground video and screenshot show the pack in the running Godot scene. Obtain the pack from the author to reproduce the comparison locally. The exported sheets and GIFs contain this project's generated characters. [Pixel Frog's asset pack](https://pixelfrog-assets.itch.io/tiny-swords) · [Sources and distribution](NOTICE.en.md) · [First release checklist](docs/release.en.md)
