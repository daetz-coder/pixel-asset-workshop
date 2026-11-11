# Character sprite workflow

[简体中文](character-sprites.md) · [Reference art skill](../SKILL.en.md)

This workflow covers soldiers, civilians, humanoid enemies and monsters. Start with an idle frame from the same faction or body type. Use a roster image to identify shared colors and class differences. For a new faction or species, study its own body proportions, hands, feet, outlines, palette and motion cues.

## Inputs and generation

- Use an approved original sprite as the reference for related units. The first Warhammer Infantry is the blue faction baseline in this project. [Field Medic asset record](../../../assets/character-runs/blue-field-medic/manifest.json)
- Generate one full-body character in a ready pose with complete equipment. Match camera, facing, body size, foot anchor, lighting, materials and pixel density. Give new classes their own equipment and silhouettes and adjust the grip as needed.
- Inspect source frames before cropping. Verify frame sizes and boundaries for each sprite sheet. Record the actual image inputs, character baseline and prompt.

## Extract and compare frames

`sprite_reference.py` requires Python 3.10+ and Pillow 10+. You can run Python with `uv run --with pillow python`. Set `SKILL_DIR` to the skill directory.

```bash
python "$SKILL_DIR/scripts/sprite_reference.py" inspect sprite.png
python "$SKILL_DIR/scripts/sprite_reference.py" extract sheet.png \
  --frame-size 192 192 --index 0 --scale 4 --out idle-reference.png
python "$SKILL_DIR/scripts/sprite_reference.py" compare original-idle.png candidate.png \
  --reference-body-box 58 47 60 80 --candidate-body-box 320 390 470 606 \
  --body-height 80 --zoom 4 --out comparison.png
```

Frame indices start at zero and advance by row. Optionally use `--crop X Y W H` to crop inside the selected frame. Annotate body boxes with their bottom at the feet and exclude long equipment, projecting ornaments and shadows. Replace sample coordinates with your own. `--body-height` sets the body height before preview enlargement. Use `--zoom 1` to see the target size, or enlarge with nearest-neighbor sampling to inspect edges. Outputs are saved separately. The alpha threshold controls preview bounds and preserves the source transparency.

Check equipment readability, hands, feet, pose, grip, pixel density, alpha edges and baseline at the intended scale. Place units at their world scale. Size monsters by body type and threat, and check faction readability and the limbs used for key actions. For animation, separate character motion, projectiles and impacts, and preserve anchor and character identity across frames.
