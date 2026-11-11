# Learn a game's visual style and create matching assets

[简体中文](SKILL.md)

Extract a reusable style profile from reference images, then create original assets using that profile. Share color, shape, lighting and pixel treatment across the set. Use category-specific structures and scales so each asset works in the game.

## Choose the scope

- **Learn a complete style.** Inventory the source pack or screenshots. Pick representative images for each category with evidence and record the reference index and coverage. With only partial references, mark which rules have direct evidence, which are inferred, and which need more material.
- **Expand a style profile.** Read the existing profile and approval history, then add evidence for missing categories. For a single asset, gather evidence for its category and reuse any approved baseline.
- **Produce matching assets.** Combine shared visual rules with the rules for the target category. For mixed batches, use a same-category reference for each asset and preview the set in one representative scene.

Read the current project's `AGENTS.md` and style profile first. Use the following guides according to the requested asset. [Tiny Swords style profile](references/tiny-swords-art.en.md) · [Blue units](references/tiny-swords.en.md) · [Character sprite workflow](references/character-sprites.en.md) · [Asset categories and review criteria](references/asset-families.en.md)

## 1. Collect references and document the style

1. Collect representative units, enemies, buildings, terrain, resources, effects and UI as needed. Use scene screenshots for proportions, layering and context, and source sprites for colors, alpha edges, grids and states. Record paths, frame indices and crop boxes.
2. Compare references within and across categories. Record camera, shapes, lighting, color clusters, material colors, outlines and detail density. Faction colors can appear on clothing and roofs, while UI retains its own screen-space materials and contrast.
3. For each category, record fixed and variable rules for shape, camera, proportions, palette, outputs, use and acceptance checks. Track canvas dimensions, logical pixels and display sizes separately. Mark values as measured, estimated or chosen for the new design. Use an approved same-category example when one exists.
4. Save the profile using the project's conventions or `assets/art-direction/<style-id>/style-profile.md`. Include shared rules, category rules, sources and coverage, approved baselines, world and UI scales, and missing evidence. Trace concrete values to references or document the design decision.

For a style analysis request, deliver the profile and its reference index.

## 2. Generate and extend

- Read the available `imagegen` skill before generating bitmaps. Use built-in GPT Image by default. Inspect and attach the actual images, and identify which reference controls the category's structure and which establishes palette or scene context.
- Make one representative sample for a new category, or reuse an approved example. Character art can establish world context. Use building references for buildings, real button states for buttons, and terrain references for tile joins.
- Include shared rules, category constraints and the new design in the prompt. Request native transparency for individual sprites. Save the exact prompts, inputs and original outputs. [Prompt templates](references/prompt-patterns.en.md)
- Generate original silhouettes and structures. Attach the approved sample again for each related asset to limit drift and follow the project's approval workflow.
- Use local tools to crop, align, sample, assemble and validate images. Use the requested generator for bitmap artwork. For interactive UI, deliver skins and icons and implement text, focus and layout in UI components.
- Record the requested model version and the backend version reported by the tool. If image generation is unavailable, deliver the finished profile, references and prompts with the generation status.

## 3. Review at the intended scale

Review against the same asset category and in its intended context. Check units and buildings at a common world scale and baseline. Check UI at its actual control size.

- Inspect silhouettes, alpha edges, pixel grids, size, offsets and cropping. The helper reports alpha, color samples and bounds, extracts sprite sheet frames and creates body-aligned comparisons. [sprite_reference.py](scripts/sprite_reference.py)
- Check the category's structure. Review equipment and feet for characters, footprints and entrances for buildings, joins for tiles, state changes for buttons, stretch regions and content areas for panels, and event points and edges for effects.
- Combine mixed categories in a representative scene. Check scale, faction colors, readability of resources and enemies against the background, and UI interaction and reading order.
- For revisions, attach the candidate and its baseline. Describe the issue and the parts to preserve. Record review conditions and mark estimates or unverified items.

## 4. Deliver and record

Deliver the requested individual assets and the required tile, state or scene previews. Follow project naming. General batches can store prompts, comparisons and a `manifest.json` under `assets/art-runs/<batch>/`. Existing character batches use `assets/concepts/` and `assets/character-runs/`.

Record category, use, outputs, raw generations, references, provenance, prompts, tools, dimensions, anchors or slice settings, and status. Record review and user approval separately. Animation work can continue with `sprite-motion-prompts` or `wan-prime-video`.

The original research notes document the early character workflow. [Research notes in Chinese](references/research.md)
