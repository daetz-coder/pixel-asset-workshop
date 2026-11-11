# Production and review by asset category

[简体中文](asset-families.md) · [Reference art skill](../SKILL.en.md)

Use same-category sprites for structure and scene screenshots for relative scale. Record shared rules, category constraints and the details that can vary.

| Category | References and specifications | Review |
| --- | --- | --- |
| Allied units and humanoid enemies | Idle frames from the same class or faction, faction comparisons and scenes showing units with buildings. Record facing, body height, feet, equipment bounds and faction color placement. [Character sprite workflow](character-sprites.en.md) | Check faction, class and weapon readability at game scale. Keep foot positions and relative heights stable. |
| Monsters and bosses | Source frames or previews with similar body types, movement and attack silhouettes. Define size, body shape, weak points and attacking limbs before selecting colors, poses and equipment. | Check silhouettes at small sizes and compare size and readability alongside allies. Check anticipation and impact cues in animation. |
| Buildings and facilities | Buildings with similar functions and scenes showing unit scale. Record projection, roof and wall materials, faction accents, entry direction, baseline, footprint and overhang. | Place the building on the target terrain. Check foundations, orientation, entry, occlusion and silhouette. Record the map footprint and canvas dimensions separately. |
| Terrain and tiles | Tile centers, straight edges, inner and outer corners, transitions, slopes, shorelines and shadows. Record tile size, joins and adjacency rules. | Build a map segment on the actual grid. Check repeated areas, corners, transitions, gaps, color jumps and elevation. |
| Props and resources | Resources with similar materials and uses. Record pickup silhouette, world scale, contact point and shadow. Add highlight, depletion or pickup states when needed. | Compare readability on typical terrain. Align the interaction region to the object and keep its anchor stable across states. |
| Buttons | Matching default and pressed states, plus focus, hover and disabled states as needed. Record borders, corner and edge regions, content area, icon size and hit box. | Assemble the control at minimum and wider sizes. Check edges, readable states, a stable hit box and aligned icons and text. |
| Panels, icons and HUD | Panels, borders, bar tracks and fills, icons and actual UI screenshots. Record screen-space palette, hierarchy, outlines, font sizes, alignment, padding, stretch direction and icon grid. | Check at target resolution. Test nine-slice or horizontal stretching, 0/50/100% bar fills, interaction states and contrast against the scene. |
| Effects and projectiles | Matching hits, fire, dust or water effects. Record trigger point, direction, coverage, timing, looping and color roles. | Preview at the correct location and time. Check alpha edges, effect bounds and layering with characters and the scene. |

## Asset structure

- **World space.** Use the game's grid, unit height or world units for scale. Allocate detail and contrast according to gameplay importance. Keep anchors and transparent margins in individual PNGs. Use consistent canvases and baselines across building states.
- **Tileable terrain.** List the modules and adjacencies required by the map. Align generated edges and test real tile placement. Keep repeating terrain, transitions and decorations separate for predictable joins.
- **Screen space.** Deliver UI art separately from layout, text and interaction. Assemble spaced nine-slice atlases in the correct order or import them as the engine expects. Preserve the corners, then tile or stretch edges and centers as needed. Check progress bar tracks and fills separately.
- **Effects.** Use the scene and gameplay event to determine size, color and duration. Separate projectiles, impacts and persistent effects as needed. Record anchors, frame order and frame times.

## Preview the set in context

Build a representative scene at the native or intended game scale. Include a relevant UI operation, such as a supply station in the scene and a heal command on the HUD. Review interaction and hierarchy, shared material colors and motifs, scale, and edges in world and screen space. Use a user-provided screenshot as a composite background or preview in the target engine. Record the review environment.
