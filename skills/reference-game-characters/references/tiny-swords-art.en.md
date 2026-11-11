# Tiny Swords style profile

[简体中文](tiny-swords-art.md) · [Reference art skill](../SKILL.en.md)

The profile uses Pixel Frog's Tiny Swords as a reference. The reviewed Free Pack assets include blue and red archers and barracks, a monastery, a tower, ores, trees, terrain, two button states, a paper panel, icons, health bars and explosion effects. Paths below are relative to the local pack at `assets/references/tiny-swords/Tiny Swords (Free Pack)/` unless stated otherwise. [Asset pack](https://pixelfrog-assets.itch.io/tiny-swords) · [UI update](https://pixelfrog-assets.itch.io/tiny-swords/devlog/1158927/ui-elements-update)

## Shared visual rules

- The slightly overhead world view reveals the front and side of units, roofs and fronts of buildings, and the elevation between terrain surfaces, edges and cliffs. Screen-space UI uses front-facing frames and layered materials.
- Establish the silhouette first. Units use large heads and short bodies. Roofs, entrances and towers signal building functions. Trees and ore use distinct masses to signal resources.
- Use hard pixel edges and broad light and dark clusters. Units and interactive objects often use dark outlines. Terrain edges follow adjacency and elevation. Match outlines to the asset's use.
- Assign color by material and role. Ground and foliage use different greens, stone and walls use cool gray-green and warm highlights, and wood is warm. Units distinguish skin, cloth and metal through value. UI uses light paper, dark frames, gold trim and colored controls.
- Reuse faction colors across categories. In the reviewed blue and red archers and barracks, clothing, helmet details and metal accents correspond to roof edges, door frames and decorations. Stone walls and construction stay recognizable. Define color placements and variable materials for each category of a new faction.

## Reference index

| Category | Reference | Observed rules |
| --- | --- | --- |
| Allied units | `Units/Blue Units/Archer/Archer_Idle.png`, `Units/Blue Units/Lancer/Lancer_Idle.png`, project asset `assets/concepts/warhammer-infantry.png` | Slightly overhead, facing right, with a large head, short body, cream-gold hands and thin dark legs. Warhammer Infantry is the humanoid baseline. [Blue unit reference](tiny-swords.en.md) |
| Humanoid enemies | `Units/Red Units/Archer/Archer_Idle.png` and the blue counterpart, `Buildings/Red Buildings/Barracks.png` and the blue counterpart | Use corresponding color placements and silhouettes to distinguish factions at a common scale. |
| Monsters and bosses | Local `frontier-outpost-prepared/enemy-board.png`, Enemy Pack sprites or official previews | Select references by species, body type and movement. Use roster boards for silhouettes and relative colors and source frames for exact measurements. [Torch Goblin preview](https://pixelfrog-assets.itch.io/tiny-swords/devlog/1495843/new-character-torch-goblin) |
| Buildings | `Buildings/Blue Buildings/Barracks.png`, `Monastery.png`, `Tower.png` | Light walls, warm wood, cool faction details, dark edges, roofs, front entrances and contact shadows. Reference canvases are 192 × 256, 192 × 320 and 128 × 256 respectively. Check footprints on the map. |
| Terrain | `Terrain/Tileset/Tilemap_color1.png`, `Shadow.png`, `Water Foam.png` | The reviewed color1 sheet is 576 × 384 with grass tops, rock walls, straight edges and transitions. The pack specifies 64 × 64 terrain cells. Check flat areas, corners, elevation, shoreline and shadow layers. |
| Resources and props | `Terrain/Resources/Gold/Gold Stones/Gold Stone 1.png`, `Terrain/Resources/Wood/Trees/Tree1.png` | Ore uses warm yellow highlights and a compact silhouette. Trees use layers of green. Check readability, anchors and passable areas on terrain. Verify the tree sheet's frame grid before extracting. |
| Buttons | `UI Elements/UI Elements/Buttons/BigBlueButton_Regular.png` and `BigBlueButton_Pressed.png` | Both reviewed atlases are 320 × 320 spaced nine-slices. The default is brighter teal-blue. Pressed lighting and depth change while the clickable area and icon alignment stay consistent. |
| Panels, icons and HUD | `UI Elements/UI Elements/Papers/RegularPaper.png`, `Icons/Icon_01.png`, `Bars/SmallBar_Base.png`, `Bars/SmallBar_Fill.png` under the inner UI directory | The paper is a spaced nine-slice. The 64 × 64 icon uses large clusters and a dark outline. The small bar has ends, a middle and a separate fill. Use UI screenshots to verify font sizes, margins and layout. |
| Effects | `Particle FX/Explosion_01.png` | Warm clusters gather, then disperse into small particles. The reviewed sheet is 1536 × 192. Confirm frame boundaries, event points and playback speed in context. |

Measurements apply to the local files reviewed. Keep source images, extracted frames and previews containing them local. Record Monster Pack observations separately from measured Free Pack specifications. [Sources and distribution](../../../NOTICE.en.md)

## Enemy Pack observations

- Body silhouettes distinguish enemies in the shared camera. The stone turtle uses a raised shell and short protruding limbs, the boar a low arched back and long snout, the spider a round abdomen and radiating legs, and flying creatures distinct wings and airborne poses. Large club users signal size with a wide torso and weapon.
- Oversized masses, clear dark edges and material shading unify the roster. Stone shells use gray-green, beasts warm browns, spiders dark purples and flying insects yellow and black. Choose limb shapes and body proportions from relevant species.
- The frontier outpost's stoneback armadillo uses the turtle's rock colors and the boar's low quadruped stance. Segmented plates, a pointed muzzle and a curled tail create its own silhouette. Check its scale alongside allies and buildings.

## Extend the Field Medic into a set

The reviewed Field Medic reads through a rounded ear-cover helmet and a hand-carried case. The first Warhammer Infantry remains the approved body reference.

| Asset | Inputs and design | Review |
| --- | --- | --- |
| Field aid station | Blue Monastery materials and faction colors, Blue Barracks entry structure and the medic case's light emblem. Design a small facility with a roof, front entry and baseline. | Check doorway height, map footprint and roof occlusion. |
| Medical pickup | Ground resources for scale and contrast, medic case for the emblem. Create a short, compact transparent sprite. | Test readability and placement on grass and light ground. |
| Heal button and panel | Default and pressed blue buttons for frame, center and feedback. Use source icons for small silhouettes. Generate the icon, skins and panel parts separately. | Assemble at target size and test narrow and wide layouts, states, icon and text. |
| Scene preview | Place the station, medic and pickup on a road built from 64 × 64 tiles. Show the heal command in the HUD. | Check that the emblem reads across world and UI assets and review color and hierarchy in context. |

For a new enemy, study a similar creature or author preview first. Use its ground silhouette, equipment and attack cues to distinguish it from the blue roster. Review threat scale in the aid station scene.
