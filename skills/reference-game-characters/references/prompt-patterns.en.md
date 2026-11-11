# Prompt templates for reference-based image generation

[简体中文](prompt-patterns.md) · [Reference art skill](../SKILL.en.md)

Fill the placeholders using the actual reference images. Number each image, describe its role and attach it to the request.

## Generate an asset from a style profile

```text
Use case: stylized-concept
Asset and gameplay use: [one original building / enemy / terrain module / UI skin / effect].
Image 1 is the primary category reference for [projection, geometry, footprint,
sprite anatomy, tile connectors, or UI frame and states].
Image 2, if present, is the world or UI context reference for [size, placement,
material colors, faction accent or surrounding contrast].
Shared art direction: [observed shape language, light, color roles, outline,
pixel density and level of detail].
Category locks: [parameters and structural parts established by the category references].
New design: [original silhouette, function, state and distinct motif].
Output: [individual PNGs or explicitly requested sheet; dimensions, part boundaries,
ground/contact pivot or UI content area, canvas padding and background].
```

Include the acceptance criteria in the prompt. Specify foundations, entry direction and roof projection for buildings, species silhouette and attack parts for monsters, joins and corners for tiles, and lighting changes, frame structure, icon area and target size for button states. Slice generated atlases at measured boundaries and check the assembled result.

## Calibrate a new character against a source pack

```text
Use case: stylized-concept
Asset type: one original full-body 2D game character sprite
Primary request: create [new class] that belongs visually in the attached reference set.
Input images: Image 1 is the original idle-frame style and anatomy reference.
[Image 2 is an optional roster/palette reference.]
View and pose: [observed view, facing and neutral ready pose].
Style locks: [observed head/body proportions, hands, feet, face, outline thickness,
pixel cluster size or other edge treatment, lighting and material color steps].
New identity: [distinct helmet/head silhouette, specific equipment and valid grip].
Palette by material: [sampled/observed cloth, metal, skin and outline colors].
Framing: [canvas/aspect], match reference body footprint and foot position,
generous clearance around the complete equipment. Exactly one character and one pose.
Background: true transparency, including gaps between limbs and props.
Constraints: preserve reference visual grammar while creating this new class;
no labels, scenery, UI, watermark or duplicate poses.
```

For a direct edit, use `precise-object-edit` and specify which image to edit and which parts can change. If the source frame supplies style only, give the new sprite its own character identity.

## Extend a roster from an approved original sprite

```text
Use case: precise-object-edit
Asset type: one additional full-body character for the same game roster
Input images: Image 1 is the approved original [seed name], the strict visual
template for this batch. [Other images and their specific roles, if needed.]
Primary request: create [new class] by changing [equipment and helmet silhouette].
Keep: [camera, facing, face, head/body ratio, tiny hand/foot shapes, outline,
logical pixel density, palette by material, lighting, body footprint and baseline].
Change only: [specific prop geometry, helmet and minimum required hand placement].
The class reads at game scale through [one or two silhouette features].
Output: one complete character in idle, equipment fully visible, same transparent
framing and margins as Image 1. Clear gaps between [relevant limbs/props].
```

## Targeted revision

Attach the candidate as the edit target. Attach an approved reference if it helps specify the features to preserve.

```text
Use case: precise-object-edit
Image 1 is the candidate to repair; Image 2 is the approved anatomy reference.
Repair only the feet in Image 1 to match Image 2: [specific observed correction].
Preserve the current helmet, prop silhouette, face, hands, palette, body placement,
canvas margins and transparency. Output the same single full-body idle character.
```

## Separate file dimensions from detail

For a larger file, use integer nearest-neighbor scaling. If the user wants more detail, regenerate and check the new pixel density. Keep the approved coarse-pixel reference for later batches unless the project adopts a new baseline.
