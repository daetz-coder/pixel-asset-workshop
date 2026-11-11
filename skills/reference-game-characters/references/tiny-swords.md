# Tiny Swords 蓝队示例

[English](tiny-swords.en.md)

整套资源的建筑、地形、UI、敌人和特效见 [Tiny Swords 画风档案](tiny-swords-art.md)。本页提供蓝队人形分支的参考图、尺寸和生图提示词。

这是本 skill 的项目示例，不是其他游戏的默认人体和色板。路径相对使用者的项目根目录；在新项目中先定位实际素材，不能假定这些文件已随 skill 安装。

## 输入与已有选择

本项目已下载的原包根目录是 `assets/references/tiny-swords/Tiny Swords (Free Pack)/`。

| 输入 | 用途 |
| --- | --- |
| `Units/Blue Units/Archer/Archer_Idle.png` | 小手、深色腿脚、原生像素比例；192×192 单帧，共 6 帧 |
| `Units/Blue Units/Lancer/Lancer_Idle.png` | 盔甲、手部、武器握持；320×320 单帧，共 12 帧 |
| `assets/references/tiny-swords/units-board.png` | 蓝队共用配色与职业轮廓 |
| `assets/concepts/warhammer-infantry.png` | 本项目用户确认的第一版战锤兵，1254×1254 透明 PNG；后续兵种主要参考 |

帧尺寸来自本项目当前文件尺寸与原帧核对，换版本后重新确认，尤其不能把 Lancer 也按 Archer 的 192 像素切帧。需要动作时另查看对应 Run、Attack/Defence；原包作者标注 10 fps / 100 ms，只作为动作预览起点。

本项目已确认第一版战锤兵作基准，并确认六兵种用于合图。直接复用这些确认；`warhammer-infantry-hd.png`、橡果卫兵、芦苇斥候和月灯守望者均为存档，不替换批次基准。

## 蓝队风格约束

- 朝右、轻俯视四分之三视角，大头盔、极短圆身。
- 双腿和双脚各合为一条很短的深蓝黑细线，两条分离，中间透明；不加粗靴子，也不让盾牌盖住脚。
- 手为几像素大小的米金小块，深色外轮廓，握武器的手与空手都维持此尺度。
- 灰蓝和青蓝布料、鼠尾草绿钢铁、浅薄荷金属高光、米金皮肤、深蓝黑描边。
- 粗方像素块、有限明暗色阶、明确轮廓。校准图省略地面投影，方便查脚部；这项约定来自本项目。
- 新职业靠头盔和装备轮廓区分，保留共同人体与色板。全身、手脚和装备完整入画。

原生显示尺寸需按实际身体高度校准；1254×1254 是生成 PNG 的文件尺寸，不能当作原包精灵的逻辑分辨率。

从本地 Archer 首帧实取的提示词色板参考：描边 `#161C2E`，布料 `#485884` / `#4697AC`，钢铁 `#688C8A` / `#9CBEAA` / `#D4EDC2`，皮肤 `#C8A876` / `#EFE1AB`。这些是材质参照，生成结果需目测检查，不假定模型会逐像素复现色值。

## 可执行的原帧提取示例

在项目根目录，令 `SKILL_DIR` 指向本 skill 的实际目录：

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

下面以弓手第一帧和已有战锤兵实测对照。身体框是对这两个文件目测标注的范围：弓手不计盔顶羽饰和地面阴影，战锤兵不计锤头；换图后需要重新标注。先还原到原包主体高度，再一起放大 4 倍。

```bash
python "$SKILL_DIR/scripts/sprite_reference.py" compare \
  assets/references/tiny-swords/prepared/archer-idle-x4.png \
  assets/concepts/warhammer-infantry.png \
  --reference-body-box 292 248 168 268 --candidate-body-box 326 391 464 604 \
  --body-height 67 --zoom 4 \
  --out assets/references/tiny-swords/archer-warhammer-skill-comparison.png
```

原包、裁帧和含原帧对照仅本地参考，保存在项目已忽略的 `assets/references/tiny-swords/`，不复制到可分发的 skill 文件夹或交付压缩包。

## 新项目首个战锤兵样图提示词

仅在尚无已确认基准且用户要求生成时使用。实际附 Archer、Lancer 单帧和可用角色表，开启工具透明背景参数。

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

本项目用户要求 GPT Image 2.6；调用能力及后端版本以工具回执为准，不在 skill 中写死并不存在的模型选择参数。

## 已有六兵种扩展方向

| 文件名（`assets/concepts/` 下） | 识别轮廓 |
| --- | --- |
| `warhammer-infantry.png` | 宽檐盔、短柄双面锤，固定批次基准 |
| `grenadier.png` | 包耳圆盔、圆铁弹与短引线 |
| `standard-bearer.png` | 小青色盔冠、直杆燕尾短旗 |
| `axe-infantry.png` | 半盔和护颊、单刃月牙斧 |
| `crossbow-infantry.png` | 护鼻盔、横持短弩，两手分明 |
| `tower-shield-infantry.png` | 方圆钢盔、薄荷镶边蓝塔盾，盾底不挡脚 |

扩展其他兵种时附第一版战锤兵，并使用通用批次提示词，只换职业段落。不要为了演示 skill 自动重做已通过的六张图。

如用户要求六角色视频输入：沿用上排战锤兵/投弹兵/旗手、下排战斧兵/弩兵/塔盾兵的 3×2 顺序；仅在合图阶段用纯洋红 `#FF00FF` 抠像背景，独立概念图继续保留透明 alpha。合图、格位 JSON 与视频提示词使用项目已有 `wan-prime-video` 流程。

## 来源与分发边界

参考包作者为 Pixel Frog。[Tiny Swords 作者页](https://pixelfrog-assets.itch.io/tiny-swords)（2026-11-11 核对）允许个人、商业项目使用及修改，但禁止将素材再分发、转售或重新打包，即使修改过也受限制。当前 Free Pack 与另列的旧版 CC0 包不能混为一谈。

此 skill 分发原创流程、提示词和脚本，不附带原包、裁出的原帧或含原帧对照图。生成图记录参考来源；不要把直接裁出的原素材或修改版冒称原创资产。
