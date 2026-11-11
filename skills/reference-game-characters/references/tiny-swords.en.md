# Tiny Swords blue faction reference

[简体中文](tiny-swords.md) · [Reference art skill](../SKILL.en.md)

This project example covers blue humanoid sprites, their dimensions and a reference prompt. Use the actual project files when adapting the skill to another game. [Complete style profile](tiny-swords-art.en.md)

## Inputs and approved baseline

The local Free Pack is under `assets/references/tiny-swords/Tiny Swords (Free Pack)/`.

| Input | Use |
| --- | --- |
| `Units/Blue Units/Archer/Archer_Idle.png` | Small hands, dark feet and native pixel scale. Six frames of 192 × 192. |
| `Units/Blue Units/Lancer/Lancer_Idle.png` | Armor, hand shapes and weapon grip. Twelve frames of 320 × 320. |
| `assets/references/tiny-swords/units-board.png` | Shared blue faction colors and class silhouettes. |
| `assets/concepts/warhammer-infantry.png` | Approved first Warhammer Infantry, a 1254 × 1254 transparent PNG and the reference for the remaining classes. |

Recheck the sheets if using a different pack version. Use the matching Run, Attack or Defence sheets for motion. The author's 10 fps, or 100 ms per frame, is a starting point for previews.

The six-unit composition uses the approved first Warhammer Infantry. The HD Warhammer and the Acorn Guard, Reed Scout and Moon Lantern Keeper are archived alternatives.

## Blue faction visual rules

- Face right in a slightly overhead three-quarter view. Use a large helmet and a very short round body.
- Draw each leg and foot as one thin, short navy-black stroke with transparency between them. Keep both visible beside or beneath equipment.
- Use tiny cream-gold hands with dark outlines. Keep gripping and free hands at the same scale.
- Use slate and teal cloth, sage steel, pale mint metal highlights, cream-gold skin and navy-black outlines.
- Use coarse square clusters, limited shading steps and clear silhouettes. The project's calibration samples omit ground shadows to make the feet easier to inspect.
- Distinguish classes through helmet and equipment shape while preserving the shared anatomy and palette. Keep all limbs and equipment within the frame.

Compare visible body height when checking scale. The 1254 × 1254 generation canvas describes the file size. Use the source frames to establish logical pixel scale.

Color samples from the local Archer idle frame are `#161C2E` for outlines, `#485884` and `#4697AC` for cloth, `#688C8A`, `#9CBEAA` and `#D4EDC2` for steel, and `#C8A876` and `#EFE1AB` for skin. Review generated colors visually.

## Extract source frames locally

Run from the project root with `SKILL_DIR` set to the skill directory.

```bash
python "$SKILL_DIR/scripts/sprite_reference.py" extract \
  'assets/references/tiny-swords/Tiny Swords (Free Pack)/Units/Blue Units/Archer/Archer_Idle.png' \
  --frame-size 192 192 --index 0 --scale 4 \
  --out assets/references/tiny-swords/prepared/archer-idle-x4.png

python "$SKILL_DIR/scripts/sprite_reference.py" extract \
  'assets/references/tiny-swords/Tiny Swords (Free Pack)/Units/Blue Units/Lancer/Lancer_Idle.png' \
  --frame-size 320 320 --index 0 --scale 4 \
  --out assets/references/tiny-swords/prepared/lancer-idle-x4.png
```

Compare the first Archer idle frame to the approved Warhammer. The body boxes were annotated for these two files. The Archer's box excludes its crest and shadow. The Warhammer's box excludes the hammerhead. Update the boxes for new inputs. The comparison aligns native body heights and then enlarges both sprites by 4×.

```bash
python "$SKILL_DIR/scripts/sprite_reference.py" compare \
  assets/references/tiny-swords/prepared/archer-idle-x4.png \
  assets/concepts/warhammer-infantry.png \
  --reference-body-box 292 248 168 268 --candidate-body-box 326 391 464 604 \
  --body-height 67 --zoom 4 \
  --out assets/references/tiny-swords/archer-warhammer-skill-comparison.png
```

Keep the pack, extracted frames and comparisons containing source frames in the ignored `assets/references/tiny-swords/` directory.

## First Warhammer sample prompt

Use this prompt when a new project requests generation and has yet to approve a reference sprite. Attach the Archer and Lancer frames and any roster board. Enable native transparency.

```text
Use case: stylized-concept. Generate exactly one original Warhammer Infantry
for a roster matching the attached Tiny Swords blue-faction references.
Image 1 (Archer idle) and Image 2 (Lancer idle) establish the camera, anatomy,
pixel clusters, hands and palette. Image 3, if attached, is the roster reference.
Keep the right-facing slightly overhead three-quarter view, oversized helmet,
tiny round blue tunic, coarse square pixel clusters and deep navy outlines.
Directly below the tunic, use exactly two separate very short thin navy strokes
for legs and feet, with transparency between them. Hands are tiny warm cream
pixel mitts with navy outlines, matching the reference hand scale.
Give this new class a low rounded flat-brimmed sage kettle helmet and one compact
short-handled two-faced mint-steel warhammer held diagonally upward on screen right.
The right hand grips the handle; the tiny left hand peeks out at the tunic edge.
Use dusty blue and teal cloth, sage and mint metal, cream/golden skin and blue-black
outlines. Keep the same logical pixels per body height as the reference sprites.
One full-body idle character, square transparent canvas, generous clear margins,
all equipment and both line feet visible. Omit the ground shadow for foot inspection.
```

The project requested GPT Image 2.6. Use the model selection supported by the tool and record its reported backend.

## Six-unit roster

| File under `assets/concepts/` | Identifying silhouette |
| --- | --- |
| `warhammer-infantry.png` | Wide brim and compact two-faced hammer. This is the approved baseline. |
| `grenadier.png` | Rounded ear-cover helmet and a round bomb with short fuse. |
| `standard-bearer.png` | Teal crest and straight staff with a short swallowtail flag. |
| `axe-infantry.png` | Half-helmet with cheek guard and a single crescent blade. |
| `crossbow-infantry.png` | Nasal guard and a short crossbow held with both hands. |
| `tower-shield-infantry.png` | Rounded square helmet and a mint-rimmed blue tower shield that leaves both feet visible. |

To add a class, attach the first Warhammer and change the class-specific portion of the batch prompt. Reuse the approved six images for the existing composition. The top row is Warhammer, Grenadier and Standard Bearer. The bottom row is Axe, Crossbow and Tower Shield. Use magenta `#FF00FF` for the composite and keep the concepts transparent. [Wan batch skill](../../wan-prime-video/SKILL.md)

## Sources and distribution

The current Free Pack allows use and modification in personal and commercial projects and restricts redistribution, resale and repackaging, including modified assets. The separately listed older CC0 pack has its own terms. Keep original pack images, extracted frames and comparisons containing them local. Record the provenance of generated assets. [Author terms](https://pixelfrog-assets.itch.io/tiny-swords) · [Project notice](../../../NOTICE.en.md)
