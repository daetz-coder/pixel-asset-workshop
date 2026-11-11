# 像素素材工坊项目工作流

本项目以 Pixel Frog 的 Tiny Swords 原始精灵为画风基准，并参考其动画节奏。先用一个角色确认与原包的画风匹配，再分批制作同风格的独立角色图。用户确认角色后，交付合并参考图和可直接粘贴的视频生成提示词。用户将图和提示词一起输入视频模型，之后从视频中拆出游戏用的逐帧 PNG。

项目介绍与启动命令见 [中文版 README](README.zh.md) 和 [English README](README.md)，实测数据与原版对比见 [Tiny Swords 案例](examples/tiny-swords/README.zh.md)，本地参考图的分发约定见 [NOTICE](NOTICE.md)。

## 整套游戏画风与素材

使用 [reference-game-characters](skills/reference-game-characters/SKILL.md) 从参考图学习整套 2D 画风和制作各类素材。[Tiny Swords 画风档案](skills/reference-game-characters/references/tiny-swords-art.md) 记录跨类别规则，以及兵种、敌人、建筑、地形、资源、按钮、UI 和特效各自的参考与验收点。以下是角色和动画的项目约定。

## 本地参考素材

- Tiny Swords Free Pack 已解压到本地参考素材目录 `assets/references/tiny-swords/`。优先查看 `Units/Blue Units/` 下的 Idle、Run 和对应职业的攻击或施法动作。参考其轻俯视四分之三视角、大头短身比例、清晰轮廓、有限色阶和动作节奏。原包标注的动画速度为 10 fps，可作为预览起点。
- 本地兵种图 `assets/references/tiny-swords/units-board.png` 用于对照各兵种共有的手脚比例、服装色板和装备的轮廓差异。
- 资源包由 Pixel Frog 制作。当前免费包允许在个人和商业项目中使用及修改，原始素材和修改后的素材包均受作者页面的再分发限制。将此目录作为本地参考，提交和交付文件使用原创角色素材。[作者页面及许可](https://pixelfrog-assets.itch.io/tiny-swords)

## 概念图与确认

新增同画风角色时，使用 [reference-game-characters](skills/reference-game-characters/SKILL.md) 校准样图、生成新兵种并检查对照；本节记录 Tiny Swords 的项目约定和已确认素材。

1. **直接调用 GPT Image 生图。** 用户指定 GPT Image 2.6，具体后端版本以工具回执为准。第一张风格样图使用本地素材包最接近该职业的 Idle 原帧。后续同批角色使用用户确认的第一版战锤兵作为直接图像参考。概念图的角色像素由生图模型生成。裁帧、最近邻放大、排版和拆帧可使用本地工具。
2. **先对齐一张新兵种样图。** 新兵种靠独立的武器和头盔轮廓区分。将原帧和生成图以相同显示比例并排检查。腿和脚各用一条很短的深蓝黑细线表示，双脚之间留空。手沿用原包的几像素浅金小手和深色外轮廓。配色沿用蓝队的灰蓝、青蓝布料，鼠尾草绿和浅薄荷色金属，米金肤色及深蓝黑轮廓。用户确认画风和新兵种后，再延展到其余职业。
3. 每张图只包含一名原创角色的全身准备姿势。角色与装备完整入画。保留生图原始 PNG，并检查轮廓、透明边缘、握持姿势和原包显示比例下的识别度。
4. 展示每批的独立概念图，记录角色名、装备、主色及对应文件。等用户确认后，使用通过确认的版本进入合图阶段。

### 第一批 · 战锤兵、投弹兵、旗手

- [战锤兵](assets/concepts/warhammer-infantry.png) 是使用内置 ImageGen 生成的待机姿势。输入为用户提供的兵种图，以及本地蓝队枪兵和弓手各自的首张 Idle 原帧。原帧取角色周围区域并以最近邻放大 4 倍。
- 短柄双面锤和宽檐钢盔作为新兵种的识别特征。布料、金属、肤色和轮廓沿用蓝队配色。样图使用两个分开的深色短线表示腿脚，双手为浅金小块。图中省略投影，便于直接检查脚部轮廓。用户认可这个造型，并要求提高分辨率。
- 用户选定 1254 × 1254 的第一版战锤兵为本批基准。[高清试版](assets/concepts/warhammer-infantry-hd.png) 仅作存档。高清试版由 ImageGen 重新取景，再用最近邻整数放大 2 倍，导出为 2508 × 2508 的透明 PNG。
- 投弹兵和旗手均以第一版战锤兵为直接图像参考，使用内置 ImageGen 独立生成。三张图均为 1254 × 1254 的透明 PNG。下表是待确认的行序和动作。

| 建议行位 | 兵种 | 识别特征 | 动作草案 |
| --- | --- | --- | --- |
| 上 | [战锤兵](assets/concepts/warhammer-infantry.png) | 宽檐盔、短柄双面锤 | 举锤、向右下砸、收锤 |
| 中 | [投弹兵](assets/concepts/grenadier.png) | 包耳盔、圆铁弹 | 收手蓄力、向右抛投、收手归位 |
| 下 | [旗手](assets/concepts/standard-bearer.png) | 青色盔冠、燕尾短旗 | 举旗、展开旗面、落旗归位 |

<details>
<summary>投弹兵与旗手生图提示词</summary>

两次调用均传入第一版战锤兵和透明背景参数，分别在共用提示词后接上对应兵种描述。

```text
Use case: precise-object-edit. Make one new class for the same Tiny Swords blue faction by editing the attached approved first-version Warhammer Infantry pixel sprite. The attached image is the edit target and strict visual template for the entire set. Keep its right-facing slightly overhead three-quarter view, extremely oversized head, short round tunic, face, palette, outline thickness, big square pixel clusters, flat color steps, character size and placement within the square transparent canvas. Match the original muted sage and mint steel, dusty blue clothing, teal collar, warm cream skin, and deep navy outlines. Both hands are tiny cream pixel mitts with navy outlines. The feet must be exactly two separate, tiny, thin straight deep navy strokes extending beneath the tunic with a transparent gap, the same lengths and positions as in the source. Keep the same amount of transparent margin and the same small body height in the frame. One sprite in idle, one class-specific prop, true transparent background, clean empty space below the feet. Change the helmet silhouette and the equipment to the new class below. Keep the new equipment simple and clearly readable with the same coarse logical pixel size.

Blue-faction Grenadier, a ranged bomb thrower. Replace the hammer with one small circular charcoal-blue iron bomb, about the size of the face, cradled at waist level just to the right of the body, with one short cream unlit fuse at the top and a small sage reflection. The small right hand visibly supports the bomb, the tiny free hand remains on the left. Replace the brimmed kettle helmet with a rounded snug sage-steel sapper helmet with a narrow teal headband and a tiny ear flap. This silhouette is identified by the round bomb held low to the right and the close helmet. The ready pose is calm and grounded.

Blue-faction Standard Bearer, a support infantry unit. Replace the hammer with one upright compact standard held in the right hand to the right of the body. The slender deep navy staff rises only a little above the helmet and ends in a small rounded mint metal cap. The simple short teal and slate-blue pennant hangs from the upper pole toward screen right, with one small pale mint diamond marking. The tiny free hand remains at the left edge of the tunic. Replace the brimmed kettle helmet with a smooth sage-steel helmet with one small teal crest ridge. This silhouette is identified by the straight staff and compact outward pennant. Fit the flag and staff fully within the same transparent framing.
```

</details>

<details>
<summary>战锤兵生图提示词</summary>

```text
Use case: precise-object-edit. Generate exactly one new Tiny Swords blue-faction troop, the Warhammer Infantry, using the provided blue unit board and close-up idle sprites as the style and scale references. The board establishes the roster and color scheme. The Lancer and Archer close-ups establish the precise pixel anatomy. Use the close-ups to match the overhead three-quarter camera, tiny round body and large helmet, but create a distinct helmet and weapon silhouette for the new class.

Highest priority is the original troop anatomy. Directly beneath the blue tunic hem, draw two very short, thin charcoal-navy strokes for the legs and feet, each only one logical pixel wide and about four logical pixels long. Each leg and foot reads as a single dark line; a few transparent pixels separate the two strokes. The strokes hang freely below the body and are clearly visible against transparency. The ends have the same width as the lines. Omit a ground shadow on this sample so the lines can be checked. Use the exact hand vocabulary of the Archer and Lancer: tiny flat pale cream mitts with cool dark outlines, just a few logical pixels across, one simple shape per hand. A hand holds the hammer handle at the right of the body; the little free hand peeks out on the left. Keep hands the size of the reference hands.

Give the new unit a low rounded, flat-brimmed kettle helmet in muted sage steel, distinct from the pointed archer helmet, with a small warm buff face under the brim. The small cobalt and slate-blue padded tunic has a simple teal collar, as on the references. Its class reads through a short-handled rectangular two-faced warhammer with one large mint-steel head and a dark navy handle held at a relaxed upward diagonal on the right. The single hammer and asymmetrical idle silhouette distinguish the class from the sword, spear, bow and monk. Sample the actual reference colors by material: cream and golden tan for hands and face, pale mint and desaturated sage steel for helmet and hammer, dusty cobalt and teal for cloth, deep blue-black outlines and legs. Use the original broad pixel clusters, limited flat color steps and hard square pixel edges at the same logical pixels per body height as the Archer and Lancer.

Output one small centered full-body game sprite on a square transparent canvas, with room above the hammer and clear transparent space immediately below the two little dark line feet. The output contains only this one character in idle, facing right, plus the held hammer.
```

</details>

<details>
<summary>战锤兵高清版生图提示词</summary>

```text
Use case: identity-preserve. Produce a higher-resolution edition of exactly the attached approved 2D pixel-art Warhammer Infantry sprite. The image is the edit target and sole visual reference. Request a high-resolution square PNG (ideally 2048×2048 or larger). Frame the sprite closer so it fills about 82 percent of the available width, with clean transparent margins on every side and the entire hammer, helmet and feet inside the frame. Use roughly twice the source's effective logical pixel density along the stepped contour so the brim, round tunic, hands and angled hammer are defined with finer hard-edged square pixels. Keep the large color clusters and original color steps, especially the sage/mint metal and dusty blue and teal cloth. Replicate the pose, proportions, face, brim, double-faced hammer silhouette and both hand positions precisely. The tiny cream mitts and the two separate, very short thin dark-navy line legs are defining details. Preserve their size relative to the body and the transparent gap between the line legs. Use pure transparency behind and beneath the sprite. Keep visible, crisp retro pixel stair-steps and a simple flat palette. The output is just the one original character, at a higher pixel density with more of the frame devoted to it.
```

</details>

### 第二批 · 战斧兵、弩兵、塔盾兵

三张待机图均以第一版战锤兵为直接参考，分别由内置 ImageGen 生成。文件为 1254 × 1254 的透明 PNG，已确认用于六兵种合图。

| 兵种 | 识别特征 |
| --- | --- |
| [战斧兵](assets/concepts/axe-infantry.png) | 单刃月牙斧、带护颊的半盔 |
| [弩兵](assets/concepts/crossbow-infantry.png) | 护鼻盔、横持短弩 |
| [塔盾兵](assets/concepts/tower-shield-infantry.png) | 方圆钢盔、薄荷色镶边的蓝色塔盾 |

<details>
<summary>第二批生图提示词</summary>

三次调用均传入第一版战锤兵和透明背景参数，分别在共用提示词后接上对应兵种描述。

```text
Use case: precise-object-edit. Generate exactly one additional blue-faction unit for the same Tiny Swords pixel sprite set. The attached first-version Warhammer Infantry sprite is the edit target and strict style, size, framing and anatomy template. Keep the same right-facing slight overhead three-quarter idle pose, large helmet above a tiny rounded tunic, simple face, same coarse square pixel grid and broad flat color clusters, same navy outline thickness, same palette and character placement within the transparent square canvas. The shared materials are sage steel with mint highlights, dusty cobalt and teal cloth, warm cream skin, and deep blue-black outlines. The two tiny cream mitts should match the scale of those in the attached reference. Keep exactly two separate very short, narrow dark navy strokes as legs and feet, visibly protruding below the tunic, with a transparent gap between them and no ground shadow. Keep the source's generous margins and same head-to-foot size within the frame. Change only the equipment, the helmet silhouette and the minimal hand placement required by the prop. The entire new character and prop fit on one square transparent PNG.

New class: Blue Axe Infantry, a melee chopping unit. Replace the hammer with one compact one-handed battle axe carried diagonally upward on the right. Its head is visibly asymmetrical: a single broad crescent wedge on the screen-right side of the haft, with a thin pale mint cutting edge and dark sage rear. The slim short dusty-navy handle is gripped in the tiny right hand; left hand is free at the tunic edge. Give the unit a smooth sage half-helmet with a slightly angular brow and one short blue cheek guard. Use the reference's navy, teal, cream and sage palette. The axe blade, not added ornament, defines the new silhouette.

New class: Blue Crossbow Infantry, a ranged unit. Hold one compact medieval crossbow low across the front of the tunic pointing toward screen right, in idle. Make it read clearly as a crossbow: a short straight dusty navy stock, a single transverse sage steel bow with visibly separated short left and right tips and one fine dark taut string. Both tiny cream mitts grip the stock, with the two mitts clearly distinct at the original hand scale. The prop stays above the hem and leaves the entire leg gap exposed. Give the unit a low rounded sage helmet with one narrow vertical mint nasal guard and teal cloth at the back. The horizontal stock and transverse bow make this class immediately distinct from an archer or spearman.

New class: Blue Tower Shield Infantry, a dedicated defender. Hold one tall rectangular tower shield on the screen-right side of the body with a gently rounded upper edge, a dusty cobalt front, a thin muted sage steel rim, and one small pale mint rectangular boss. Angle the shield slightly in perspective and hold its lower edge above the level of the tunic hem so both short line legs remain fully visible and separate. The shield hand grips its inner edge, and the tiny cream free hand is visible on the left side of the body. Give the unit a squat, slightly squared sage steel helmet with a simple horizontal teal brow and small warm buff face. The tall shield is the sole equipment and defines the silhouette.
```

</details>

### 首张卫兵样图存档

- 输入使用本地 `Units/Blue Units/Warrior/Warrior_Idle.png` 的第一帧。该原帧画布为 192 × 192 像素，以最近邻放大 2 倍后直接传给 ImageGen。
- [橡果卫兵风格样图](assets/concepts/acorn-guard-tiny-swords-style.png) 是 ImageGen 直接输出的透明 PNG。用户指出腿脚形状不符合原包，同时要求新兵种采用不同的装备轮廓，并沿用原包的手部和配色。此样图仅作存档。
- 本地同尺寸对照 `assets/references/tiny-swords/warrior-style-comparison.png` 左侧为原包战士，右侧为生成样图。样图在画布中的站位略低，确认后以脚底为基准对齐锚点。

<details>
<summary>风格样图生图提示词</summary>

```text
Use case: precise-object-edit. The attached transparent PNG is the actual Tiny Swords Warrior idle sprite and is the sole style, scale and pose reference. Make a single new sibling guard unit by editing that sprite at the same logical pixel scale. Treat each existing square pixel block as a unit. Match the reference exactly in sprite footprint relative to canvas, foot position, slight overhead three-quarter view facing right, oversized fully enclosed helmet, tiny tucked body, hidden short legs, color count and clustered hand-placed shading, near-black cool outline and small dark oval contact shadow. Match the rough size of each existing pixel block. The helmet takes up nearly half the character's height. Change only three shapes and their local colors: replace the curled plume with a short blunt acorn-like copper finial over a smooth domed brass helmet, change the blue cloth to muted brick red, and replace the tall blue shield with a simple small round copper shield of comparable visual weight with one light central boss. Retain the reference sword silhouette, up-right angle and position, the black visor slit, and the same compact combat idle stance. Treat this as an in-game sprite edit with large flat color clusters, one sprite and a fully transparent square canvas with the same generous blank margins. Show the sprite at the same small scale within the canvas as the input.
```

</details>

### 首轮角色草案存档

| 行位 | 角色 | 识别特征 | 首轮动作 |
| --- | --- | --- | --- |
| 上 | [橡果卫兵](assets/concepts/acorn-guard.png) | 铜色橡果盔、红领巾、短剑和圆盾 | 蓄力、横斩、收剑归位 |
| 中 | [芦苇斥候](assets/concepts/reed-scout.png) | 沙色长耳、青绿轻甲、橙领巾和短弓 | 举弓、拉弦、放弦、收弓归位 |
| 下 | [月灯守望者](assets/concepts/moon-lantern-keeper.png) | 飞蛾触角、紫色披风和黄铜灯笼 | 提灯蓄力、发出一次光脉冲、落灯归位 |

这三张概念图由内置 ImageGen 于 2026-11-10 生成。用户指出画风偏离 Tiny Swords，图像仅存档。角色和动作仍是草案，随风格样图一起复核。

<details>
<summary>首轮概念图生图提示词</summary>

三次调用均请求透明背景。每次将共用提示词与对应的角色描述接在一起。

```text
Use case: stylized-concept. Create one original, game-ready-looking 2D pixel art unit concept for a whimsical medieval woodland tactics game. A single full-body sprite in neutral ready pose, orthographic three-quarter view slightly from above, facing screen right. Use the visual grammar of compact medieval RTS sprites: oversized head, short limbs and strong silhouette, deep aubergine one-logical-pixel outlines, crisp hand-placed square pixel clusters, a small controlled palette with two or three shades per material, warm upper-left lighting, simple bold readable equipment. Aim for about 64 to 80 logical pixels of sprite detail enlarged with sharp nearest-neighbor pixels. Single centered character, generous transparent padding all around, both feet and all equipment visible, truly transparent background. The whole image contains just this one pose, free of environmental elements, shadows on the ground, captions, frames and logos. Original design distinct from existing sprites.
```

```text
Character: Acorn Guard, a cheerful sturdy human squire in a hammered copper acorn-cap helmet with a small upright stem finial, rust red neckerchief and russet brown quilted tunic. Wields a compact pale mint-steel sword angled upward at the screen-right side and a round amber nut-shell buckler with a clear central boss at the screen-left side. Chunky boots and low grounded stance.

Character: Reed Scout, a small sand-furred anthropomorphic hare archer with two long upright ears, a teal headband and sea-green ranger jacket with a small burnt-orange scarf and brown boots. Holds a simple curved reedwood shortbow in a ready rest pose on the right, visibly separate from body contour. Alert lean posture and distinct pointed-ear silhouette.

Character: Moon Lantern Keeper, a small benevolent anthropomorphic moth mystic in a bell-shaped plum and lilac cloak with scalloped wing-like lower corners, two short feathery antennae, soft dusty-rose collar fluff and two small gold eyes inside a dark mask-like face. Holds a single hexagonal brass lantern with a warm amber interior toward screen right. Compact body, small grounded boots and simple cloak ornament.
```

</details>

## 视频参考图排版

- 多角色共用时长和分辨率时，使用仓库内 [wan-prime-video](skills/wan-prime-video/SKILL.md) 的 `compose_reference.py` 合成一张首帧，并生成逐格提示词与格位 JSON。每批提交一次 Wan 任务。成片与格位 JSON 可一起导入「逐帧」，也可通过 [本地拆帧 CLI](scripts/extract_frames.py) 提取角色序列。

- 横屏 720p 参考图为 `1280 × 720` PNG。三个角色可按一列三行排列。六个角色使用三列两行，每格一名。所有角色使用同一缩放比例与格内脚底锚点。预留装备挥动和投射物的空间，使动作完整留在各自格内。
- 参考图使用与角色和特效明显区分的纯色背景，供视频成品抠像使用。画面只保留角色和背景色，角色名与动作按对应格位写在提示词中。
- 确认后交付 `assets/video-inputs/<批次>-reference.png` 和同名 `<批次>-prompt.md`。参考图与提示词的顺序须一致。

### 蓝队六兵种交付

- [三列两行参考图](assets/video-inputs/blue-units-3x2-reference.png) 上排从左到右为战锤兵、投弹兵、旗手，下排为战斧兵、弩兵、塔盾兵。战锤兵使用第一版。参考图使用纯洋红 `#FF00FF` 作为抠像底色。
- [5 秒 480p 视频提示词](assets/video-inputs/blue-units-3x2-prompt.md) 使用横屏 16:9，分为待机、步行、攻击与技能、独立特效四批。前三批使用六兵种参考图，特效批使用[纯洋红特效底板](assets/video-inputs/blue-units-3x2-fx-reference.png)。逐格裁切坐标按视频实际输出宽高换算。
- 已实测的是另一条 [混合动作 Wan 成片](assets/video-inputs/blue-units-3x2-wan-prime-480p.mp4)，使用[实际提交提示词](assets/video-inputs/blue-units-3x2-wan-prime-prompt.txt)和[对应格位](examples/tiny-swords/wan-layout.json)。10 fps 可抽出六组各 50 帧，需继续按动作筛帧。

## 第一批 3 秒视频提示词草案存档

以下文字对应第一批蓝队兵种。交付时根据确认后的角色造型、行序和动作修改。

```text
用输入图片作为第 0 帧，生成一段 3 秒、1280×720、16:9 的 2D 像素角色动画。画面从上到下是三个固定的等高行带。每行一名独立角色，三个动作并行播放。固定正交镜头、纯色背景和各行脚底锚点。角色全身与装备始终在所属行内，保持参考图里的轮廓、比例、配色、朝向和清晰的像素边缘。

上行，战锤兵向右下砸一次。先把短柄双面锤举到头侧蓄力，再迅速砸向右下方，表现停顿和反弹，最后收锤回到待机姿势。

中行，投弹兵向右投弹一次。先将圆铁弹收至肩侧蓄力，再向右抛投，圆铁弹沿本行低弧线飞离。角色完成随手动作，回到空手待机姿势。

下行，旗手原地举旗一次。先稳住旗杆，再将燕尾短旗向上举起，旗面向右展开并轻摆，随后旗手将旗杆落回起始位置。

0.0–0.4 秒建立准备姿势，0.4–1.3 秒蓄力，1.3–1.8 秒完成锤击、抛投或举旗，1.8–3.0 秒完成随动与复位。每行各完成一次动作。画面只包含参考图的三名角色、各自的装备与动作效果，以及平整的纯色背景。
```

循环动作取首尾相位自然衔接的一轮。一次性动作完整保留准备、发力、随动和恢复阶段，裁掉多余的片尾静止帧。投射物和命中特效拆成独立素材层，在游戏中按脱手和命中事件播放。

## 拆帧与游戏导入

1. 保留源视频，按时间顺序抽帧。先以视频实际帧率检查关键姿势，再根据动作节奏挑帧。10 fps 是预览起点，锤击触地、圆铁弹脱手和旗面展开等关键姿势优先保留。
2. 用参考图的固定格位边界裁出各个角色，去除纯色背景并输出透明 PNG。检查压缩造成的残边、半透明噪点和特效截断。
3. 同一动作全程使用统一的画布尺寸、缩放、脚底锚点和命名。按角色和动作输出，例如 `<角色>/<动作>/0000.png`，并记录帧顺序、帧时长和是否循环。
4. 将序列帧以最近邻采样在目标游戏比例下预览，核对身份、手脚和装备连续性、锚点稳定性、动作完整性与循环接缝，再导入游戏。
