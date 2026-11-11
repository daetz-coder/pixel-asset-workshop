# Six blue units · Five-second 480p video prompts

[简体中文](blue-units-3x2-prompt.md) · [Tiny Swords case study](../../examples/tiny-swords/README.md)

Set the video to **5 seconds, 480p, landscape 16:9**. Copy one code block per submission. Use the six-unit reference for batches A through C and the blank magenta plate for batch D. [Six-unit first frame](blue-units-3x2-reference.png) · [Effects first frame](blue-units-3x2-fx-reference.png)

| Batch | Content |
| --- | --- |
| A | Idle loops for six units |
| B | In-place walk loops for six units |
| C | One attack or skill per unit, including the bomb and bolt release frames |
| D | Six standalone effects to trigger from game events |

## A · Idle loops

```text
Use the input image as the first frame of a five-second 480p landscape 16:9 2D pixel-art game animation. Use a fixed orthographic camera, a slightly overhead three-quarter view and a solid magenta #FF00FF background. Preserve the three-column, two-row layout, scale, right-facing orientation, helmets, clothes and equipment. Each cell holds only its reference character and has clear magenta space on every side. Pin both feet to their first-frame positions. Keep two separate short navy-black line feet, tiny cream-gold hands and hard square pixels. Show only the six characters, their equipment and the solid background.

Complete one calm breathing cycle from 0 to 2.5 seconds and repeat it from 2.5 to 5 seconds. From the reference pose, lower the torso slightly and rise slowly to the same pose. Match position, equipment angle and motion speed across the loop seam. Helmets and equipment retain their rigid silhouettes.

Top left, Warhammer Infantry. The shoulders and gripping hand dip slightly. The two-faced hammer dips with the hand and returns.
Top center, Grenadier. The bomb hand rises and falls slightly with the chest. The iron bomb remains at waist height with its fuse unlit.
Top right, Standard Bearer. Keep the pole upright and its lower tip steady. Let only the swallowtail flag tip sway once.
Bottom left, Axe Infantry. Draw the grip inward slightly and release it back. Preserve the crescent axe head.
Bottom center, Crossbow Infantry. Keep both hands on the lowered crossbow. Its stock rises and falls slightly with the breath.
Bottom right, Tower Shield Infantry. The shield rim dips and returns. Keep the shield at the unit's side.

Use distinct pixel poses on a flat background. No camera movement, walking, attacks, projectiles, effects, ground, shadows, text or motion blur.
```

## B · Walk loops

```text
Use the input image as the first frame of a five-second 480p landscape 16:9 2D pixel-art game walk cycle. Use a fixed orthographic camera, a slightly overhead three-quarter view and a solid magenta #FF00FF background. Preserve the three-column, two-row layout, scale, right-facing orientation, helmets, clothes and equipment. The body center bobs around its first-frame position. Use the first-frame feet as the ground line. All six units walk in place facing right within their cells. Lock the camera and character roots.

Complete one two-step cycle per second, for five cycles. Start in a near-neutral passing pose. The near foot steps forward to the right and lands, the far foot passes beneath the body, the far foot steps forward and lands, and the near foot passes back to the same phase. Each supporting foot contacts the same baseline and one foot always supports the body. Alternate two short navy-black line feet and leave visible magenta between them in key poses. Keep torso bob small and the proportions of helmets, torsos, hands and equipment consistent. Match cadence, stride and the loop seam across cycles.

Top left, Warhammer Infantry. Use a steady step. Carry the short hammer and let its head bob slightly on contact.
Top center, Grenadier. Swing the free hand slightly. Keep one iron bomb secure at the waist.
Top right, Standard Bearer. Hold the staff nearly vertical. Let the short swallowtail flag sway back with the steps.
Bottom left, Axe Infantry. Swing the shoulder and axe hand slightly. Keep the blade on the right.
Bottom center, Crossbow Infantry. Hold the crossbow low with both hands. Let the forearms bob gently on alternating contacts.
Bottom right, Tower Shield Infantry. Use the shortest stride. Lower the tower shield slightly on each contact and keep both short feet visible beneath or beside it.

Keep all feet, hands and equipment visible within their cells. Show only the six units and the solid background. No hopping, running with an airborne phase, one-foot sliding, root translation, camera movement, effects, ground, shadows, text or motion blur.
```

## C · Attacks and skills

```text
Use the input image as the first frame of a five-second 480p landscape 16:9 2D pixel-art combat animation. Use a fixed orthographic camera, a slightly overhead three-quarter view and a solid magenta #FF00FF background. Lock the three-column, two-row layout, scale, identities and right-facing direction. Columns divide at one third and two thirds of the width and rows divide at half the height. Anchor each root at the first-frame ground point between its feet. The body may lean and the support foot stays in place. Preserve head and body proportions, hard square pixels, tiny cream-gold hands and two short navy-black feet.

Hold the reference ready poses from 0 to 0.35 seconds. Each cell performs one action at the times below and reaches a stable end pose before 3 seconds. Hold it to the end. Give each class its own anticipation, direction of force and finishing silhouette.

Top left, Warhammer Infantry. Overhead smash. From 0.35 to 1.10 seconds, bend the knees and raise the hammer above the helmet. Around 1.25 seconds, strike down and right on a nearly vertical path. Bring the hammerhead to foot-baseline height with the handle tilted downward. Hold low for about 0.10 seconds, rebound briefly and lift back to ready. Show the overhead peak, contact near the feet and rebound.
Top center, Grenadier. One-handed overhand throw. From 0.35 to 0.80 seconds, draw one iron bomb behind the right shoulder and lean back slightly. Around 0.90 seconds, reach up and forward over the shoulder and release one round iron bomb. Show a short arc inside the same cell and at least one frame with the bomb fully detached and surrounded by magenta. End the visible trajectory in the right-hand clearance inside that cell. Follow through and recover with both hands empty.
Top right, Standard Bearer. Vertical rally. From 0.60 to 1.50 seconds, drive the original pole straight up and keep the pole and finial visible. Around 1.60 seconds, unfurl the flag sideways to reveal the swallowtail and diamond. Hold about 0.35 seconds, then lower the pole straight back.
Bottom left, Axe Infantry. Waist-high sweep. From 0.35 to 0.65 seconds, draw the crescent axe back at waist height and counter-rotate the shoulders. Around 0.75 seconds, sweep horizontally to the right above the knees and extend the handle and forearm. Turn back and recover. Keep the single crescent blade silhouette throughout.
Bottom center, Crossbow Infantry. Level shot. From 0.35 to 1.10 seconds, raise the crossbow with both hands, brace it and aim to the right. Around 1.20 seconds, release the string and shoot one short bolt straight from the front, with slight recoil in the hands and torso. Show at least one frame with the bolt fully detached and surrounded by magenta. End its visible path inside the cell's right margin. Lower the empty crossbow.
Bottom right, Tower Shield Infantry. Impact block. From 0.55 to 1.15 seconds, lower the stance, plant both feet and raise the shield toward front right to cover the right half of the torso. Around 1.45 seconds, recoil one small pixel step left at the shield edge and press the shoulder back briefly. Keep both feet planted. Brace for about 0.35 seconds, then lower the shield to the side.

Show the six characters, their original equipment, one iron bomb and one crossbow bolt. Keep all silhouettes and projectiles within the originating cells with magenta space around them. Show impact through poses. No dust, slashes, explosions, magic, targets, text, shadows, camera movement, blur or ghosting.
```

## D · Standalone effects

```text
Use the solid magenta input as the first frame of a five-second 480p landscape 16:9 2D pixel-art effects sheet. Lock the orthographic camera and keep the background at uniform #FF00FF. Divide the canvas into an invisible three-column, two-row grid. Use each cell center as its effect origin. Play one effect once in each cell. Each effect occupies at most 80 output pixels in width and height, with ample clear magenta around it. Use a few hard-edged pixel clusters and the colors below. Show only the effects and the solid background.

Keep the first 0.5 seconds empty. Use these onset times and approximate durations. After each effect ends, its cell returns to solid magenta. All six cells are empty after 4 seconds.

Top left, hammer ground contact. Start at 0.70 seconds and last 0.35 seconds. Flash a tiny cream contact cluster, then spread low taupe dust left and right along the ground line. Scatter a few square particles. Keep it wide and flat.
Top center, iron bomb burst. Start at 1.10 seconds and last 0.55 seconds. Flash a bright cream-yellow core, expand briefly into uneven orange-yellow flame clusters, then dissolve into a few dark blue-gray smoke blocks.
Top right, rally command. Start at 1.45 seconds and last 0.65 seconds. Expand a flat mint-teal ellipse from the origin. Lift three tiny cyan-white pixels. Let the ring and pixels disappear in sequence.
Bottom left, axe sweep. Start at 1.90 seconds and last 0.25 seconds. Sweep a slender mint and cream crescent through the origin from left to right. Use a bright leading edge and break the trailing edge into two or three short pixels that vanish quickly.
Bottom center, bolt impact. Start at 2.30 seconds and last 0.25 seconds. Flash a small cluster of sharp cream fragments, then scatter three or four pale teal particles rightward along the shot line and let them disappear.
Bottom right, shield block. Start at 2.70 seconds and last 0.30 seconds. Flash a cool-white contact pixel and rebound three or four short hard-edged gold sparks up and right. Keep it compact.

Show distinct onset, peak and decay poses. End by shrinking and removing pixel clusters. No characters, weapons, projectiles, ground, grid lines, text, camera shake, gradients, glow, blur or magenta particles.
```

## Extraction and game anchors

- Round the one-third and two-thirds column boundaries and the half-height row boundary using the actual video dimensions. At 854 × 480, columns use `0, 285, 569, 854` and rows use `0, 240, 480`. Character root coordinates use x positions `127, 412, 696` and y positions `166, 406`. Scale x by `W/854` and y by `H/480` for other sizes, then round.
- For idle and walking, take one continuous cycle and remove duplicate seam frames. Confirm near-foot contact, far-foot passing, far-foot contact and near-foot passing in the walk. Keep the canvas foot anchor fixed and let game movement provide translation.
- For attacks, select anticipation, force, contact or release, follow-through and recovery from source frames. Use about 10 fps for the first preview, then check brief release poses at source rate. Trim redundant end holds. The Grenadier finishes empty-handed and needs a separate reload action to regain a bomb.
- Extract the detached bomb and bolt as separate sprites and remove them from the character sequence. Spawn them at the release point or crossbow muzzle. Let the game control trajectories and hits.
- Crop effects individually, retain onset, peak and decay, and record each origin. Attach hammer dust to the ground impact and the axe sweep to its blade path. Trigger the bomb and bolt effects at their actual hit points. Start the rally ring at the flag bearer's feet when the flag unfurls. Trigger sparks on the shield contact point. The prompt times are sampling guides.

## Review of the local three-second trial

The earlier local trial was 854 × 480 at 30 fps with 90 frames. The motion review used the local Blue Warrior's Idle, Run, Attack and Guard, the Archer's Shoot and Arrow, and the Monk's Heal_Effect as references.

| Observation | Implication |
| --- | --- |
| Opening and closing poses held nearly still, with no complete breathing or alternating walk cycle. | Use it for partial combat poses and generate dedicated idle and walk cycles. |
| At about 1.33–1.80 seconds, both hammer and axe extended horizontally. The hammer failed to reach the foot line. | Distinguish the overhead drop to foot height from the waist-high sweep. |
| At about 1.60 seconds, the bomb reached the shield unit and the bolt had crossed its cell boundary. By about 1.80 seconds, the bolt was beyond the shield. | Keep both visible trajectories inside their source cells for clean crops. |
| The flagpole tilted behind the helmet and then to the right. Shield poses changed little and lacked contact feedback. Feet tilted or shifted during hammer and axe swings. | Use a vertical flag raise and hold, readable shield occlusion and recoil, and planted support feet. |
| Around 2.00 seconds, the Grenadier held a bomb again without a clear reload. The old prompt excluded explosions, dust and particles. | Finish empty-handed and generate contact effects separately for game events. |
| Top-left background samples drifted from RGB `(237, 19, 229)` to `(226, 19, 222)`. The lower-right cell had a generation label near the shield unit's feet. | Check key color uniformity and compressed edges, sample the actual background, and use output settings that leave the asset area clear. |
