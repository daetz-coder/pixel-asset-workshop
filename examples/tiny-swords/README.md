# From Tiny Swords to six original units

[Chinese](README.zh.md) · [Project home](../../README.md) · [Pixel Frog's asset pack](https://pixelfrog-assets.itch.io/tiny-swords) · [Style profile](../../skills/reference-game-characters/references/tiny-swords-art.en.md)

The Blue Archer and Lancer idle frames provided the visual baseline. The first Warhammer Infantry sample established the shared body shape and materials for the Grenadier, Standard Bearer, Axe Infantry, Crossbow Infantry and Tower Shield Infantry.

## Comparison with the original

| Aspect | Tiny Swords reference | Original units in this project |
| --- | --- | --- |
| Camera and proportions | The Blue Archer and Lancer use a slightly overhead three-quarter view, large heads and short bodies. | The first Warhammer Infantry sample carries those proportions into the five other units. |
| Hands, feet and contact | Tiny cream-gold hands have dark outlines. Short dark feet show beneath the body. The Archer has a contact shadow. | The new samples use small hands and separate thin legs. They omit the shadow to expose feet and transparent edges for inspection. |
| Materials and colors | Slate and teal cloth, sage metal, pale mint highlights and cream-gold skin. | The generated sprites carry over the material contrast and blue faction colors. The team reviewed colors and pixel clusters visually. |
| Class silhouettes | The Archer reads through a pointed helmet, bow and quiver. The Lancer reads through a spear. | The Warhammer Infantry uses a wide-brim helmet and compact two-faced hammer. Each of the other five has its own equipment silhouette. |
| Size and timing | Each Blue Archer idle frame is 192 × 192. The author specifies 10 fps. | The original concepts are 1254 × 1254 transparent PNGs. The comparison aligns visible body heights. The video export samples at 10 fps before manual selection. |

The side-by-side places the original Archer's first idle frame on the left and the first Warhammer Infantry on the right. It aligns their foot baselines and scales the annotated bodies to 67 px before enlarging both by 4× with nearest-neighbor sampling. Equipment and helmet ornaments remain visible outside the body boxes. From the repository root, run with Pillow installed.

```sh
bash scripts/compare_tiny_swords.sh '/path/to/Tiny Swords (Free Pack)'
```

Open `work/tiny-swords/comparison/archer-vs-warhammer.png`. The comparison contains Pixel Frog's art and is generated locally. Reannotate the body boxes if your pack version uses a different canvas or pose. [Blue unit reference and frame sizes](../../skills/reference-game-characters/references/tiny-swords.en.md)

## Six characters from one generated video

| Top row, left to right | Bottom row, left to right |
| --- | --- |
| Warhammer Infantry · Grenadier · Standard Bearer | Axe Infantry · Crossbow Infantry · Tower Shield Infantry |
| Downward hammer strike · Overhand toss · Raise and unfurl flag | Axe sweep · Fire bolt · Raise shield and block |

![Actual SpriteFrame workspace with the generated clip and six imported crops](preview/blue-squad.png)

The screenshots show the bundled English workbench during extraction and frame curation. [Start SpriteFrame](../../workbench/README.md) · [Curation screenshot](preview/spriteframe-curate.png)

- **Input.** A 1280 × 720 first frame with three columns, two rows and a magenta key (`#FF00FF`). The submitted prompt sequences idle, walking and a skill. [First frame](../../assets/video-inputs/blue-units-3x2-reference.png) · [Exact submitted prompt](../../assets/video-inputs/blue-units-3x2-wan-prime-prompt.txt)
- **Video.** The generated Wan MP4 is 854 × 480 at 30 fps and lasts five seconds. [Actual Wan MP4](../../assets/video-inputs/blue-units-3x2-wan-prime-480p.mp4) · [Matching layout](wan-layout.json)
- **Output.** At 10 fps, the CLI exports 50 transparent PNGs per unit. The bundled SpriteFrame's native-frame mode retains 150 decoded frames per unit and opens them in the curation editor. The workbench flagged one Crossbow Infantry frame and three Tower Shield Infantry frames for edge contact. Review those frames before exporting an action. [CLI command](../../README.md#reproduce-the-example-offline) · [SpriteFrame export record](spriteframe-export.json)
- **Motion review.** The clip contains the hammer strike, bomb release, flag raise and shield sparks. Check the actual timing in the clip. A fixed cell can clip weapons that cross into another cell. Isolate projectiles manually and review equipment continuity, contact poses, keying edges and loop joins.

At the same settings with no retries, separate five-second clips would take six submissions and 30 generated seconds. The batch takes one submission and five generated seconds. Image generation, rework and provider pricing affect the total cost.

Use the walk config to reproduce composition. The prompts for separate idle, walk, skill and standalone effects batches are production inputs for new clips. [Walk batch config](batch-walk.json) · [Five-second prompt set](../../assets/video-inputs/blue-units-3x2-prompt.en.md)

## Export sprite sheets and GIFs

![Warhammer Infantry sprite sheet](preview/exports/warhammer-sheet.png)

![Warhammer Infantry GIF from the same frames](preview/exports/warhammer.gif)

Each sample selects 12 frames around the action, using one frame out of every two from the cleaned 10 fps sequence. The exporter crops each sequence to a shared canvas and preserves the foot anchor. The PNG stores the original alpha channel and the GIF uses binary transparency. [All six exports](https://daetz-coder.github.io/projects/pixel-asset-workshop/showcase/spriteframe.html#exports) · [Manifest](preview/exports/manifest.json)

```sh
python examples/tiny-swords/export_previews.py --frames work/tiny-swords/frames --out work/tiny-swords/exports
```

## Compare the original in Godot

[![Godot training ground with original and generated units](preview/training-ground.png)](https://daetz-coder.github.io/projects/pixel-asset-workshop/showcase/godot.html)

The training-ground recording shows the running scene at 10 fps. Tiny Swords terrain, scenery and upper-row sprites by [Pixel Frog](https://pixelfrog-assets.itch.io/tiny-swords). [Watch online](https://daetz-coder.github.io/projects/pixel-asset-workshop/showcase/godot.html) · [Training-ground MP4](preview/training-ground.mp4) · [Godot project](godot/project.godot)

Extract the PNGs to `work/tiny-swords/frames` using the project quick start, then run the training ground from the repository root with Godot 4.5 and a local Tiny Swords Free Pack. The field uses the pack’s grass, cliffs and scenery. The six original blue units idle on the upper row and the six generated units play the mixed-action clip below. Every column shares a horizontal anchor. Each row has a common foot line. The original sprites are shown at 1× and the video frames at 0.5× to bring their body sizes closer. Both use nearest-neighbor sampling. Space or Enter pauses and resumes, and Left and Right step one frame at a time. [Extraction command](../../README.md#reproduce-the-example-offline)

```sh
godot --path examples/tiny-swords/godot res://comparison.tscn -- --pack="/absolute/path/to/Tiny Swords (Free Pack)"
```

If the pack is already in `assets/references/tiny-swords/Tiny Swords (Free Pack)`, omit the `--pack` argument. Record the comparison locally with Godot Movie Maker by adding `--write-movie "$PWD/work/tiny-swords/comparison.avi" --fixed-fps 10 --quit-after 50` before the `--` separator. [Generated-only Godot capture](preview/godot-playback.mp4) · [Workflow video](preview/workflow-promo.mp4)

The 21.5-second walkthrough uses the actual SpriteFrame screenshots, the before and after keying comparison, the exported Warhammer sheet and the Godot training-ground recording. With Python and Pillow, FFmpeg, Node.js and npm installed, run `bash examples/tiny-swords/promo/render.sh` from the repository root to rebuild the video and poster. Set `REMOTION_CHROME` to use a specific browser executable. [Remotion composition](promo/showcase.jsx) · [Watch with optional Chinese subtitles](https://daetz-coder.github.io/projects/pixel-asset-workshop/showcase/godot.html#workflow-video)
