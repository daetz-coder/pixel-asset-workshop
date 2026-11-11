# AliWenSkill · Pixel Art Production Workflow

[简体中文](README.md) · [Tiny Swords case study](examples/tiny-swords/README.md) · [Contributing](CONTRIBUTING.md)

Learn a game's visual language, use it to design original assets for your own game, and produce sprite animation drafts in batches.

1. **Learn the style.** Record camera angle, proportions, pixel scale and material colors. Review one original sprite next to a reference at the same body scale, then extend the rules to your roster, terrain, buildings or UI.
2. **Generate and pack.** Make each sprite as its own transparent PNG. Pack compatible characters into one keyed first frame and write one motion instruction per cell. Save a matching layout JSON.
3. **Generate video and extract frames.** Submit one clip per batch, using Wan3.0 Video Prime as an example. Crop the actual clip with the saved layout, key out the background and curate the transparent PNG sequences.

The checked-in case uses six original units, one five-second Wan clip and six sequences of 50 candidate frames at 10 fps. Batching reduces submissions at the same duration and resolution; actual costs also depend on retries and pricing. Crowded cells reduce available motion space.

## Reproduce the example offline

Install Python 3.10+ and FFmpeg with ffprobe. ImageMagick 7 is also needed to compose new first frames.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/extract_frames.py \
  --video assets/video-inputs/blue-units-3x2-wan-prime-480p.mp4 \
  --layout examples/tiny-swords/wan-layout.json \
  --fps 10 --out work/tiny-swords/frames
```

Check `manifest.json` in the output for each cell's anchor, crop, and empty or edge-touching frames. This demo mixes idle, walking and skills in one clip; review and split it before using it in a game.

Use the [style reference skill](skills/reference-game-characters/SKILL.md) to design new sprites, the [Wan skill](skills/wan-prime-video/SKILL.md) to pack and optionally submit a batch, and [the integration guide](docs/integrations.md) to connect another provider or a visual review tool. No API key is required to reproduce the included clip's extraction.

[Tiny Swords by Pixel Frog](https://pixelfrog-assets.itch.io/tiny-swords) is the style reference. Obtain it from the author to reproduce the local side-by-side; the source pack and comparisons containing its frames are kept out of the release. See [NOTICE](NOTICE.md) for distribution boundaries.
