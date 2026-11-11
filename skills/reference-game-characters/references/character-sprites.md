# 角色精灵流程

[English](character-sprites.en.md)

适用于士兵、平民、人形敌军和怪物。先选同阵营或同类体型的原始 Idle 单帧。角色表补充共同色板与各职业的差异。做新阵营或新物种时，从对应原图重新学习头身、手脚、轮廓、色板和动作信号。

## 输入与生成

- 项目已确认的原创角色可作同类生图锚点。Tiny Swords 蓝队以第一版战锤兵为锚点。当前的医护兵实测见 [项目资产记录](../../../assets/character-runs/blue-field-medic/manifest.json)，在其它项目使用时按当前项目文件为准。
- 静态概念图默认一个角色、全身准备姿势和完整装备。锁定镜头、朝向、身体尺寸、脚底锚点、光照、材质与像素密度。新职业改变装备和识别轮廓，握持手位可按装备调整。
- 先看源帧再裁切。原包帧尺寸以文件和帧边界核对。同一资源包的多个角色可能有不同画布。记录实际图像输入、角色基准和生成提示词。

## 裁帧和检查

`sprite_reference.py` 需要 Python 3.10+ 和 Pillow 10+。可用 `uv run --with pillow python` 运行。令 `SKILL_DIR` 指向本 skill。

```bash
python "$SKILL_DIR/scripts/sprite_reference.py" inspect sprite.png
python "$SKILL_DIR/scripts/sprite_reference.py" extract sheet.png \
  --frame-size 192 192 --index 0 --scale 4 --out idle-reference.png
python "$SKILL_DIR/scripts/sprite_reference.py" compare original-idle.png candidate.png \
  --reference-body-box 58 47 60 80 --candidate-body-box 320 390 470 606 \
  --body-height 80 --zoom 4 --out comparison.png
```

帧索引从零开始逐行计算。可选 `--crop X Y W H` 在所选帧内再裁切。比较用人工标注的主体框，框底是脚底，排除长装备、突出装饰和阴影。示例坐标需按实际图替换。`--body-height` 为放大前的显示高度，设 `--zoom 1` 看原显示比例，随后以最近邻放大检查边缘。对照输出和裁帧均另存。alpha 阈值控制预览取框，原图透明度保留。

检查目标尺寸下能否辨认角色与装备，核对手脚、姿势、握持、像素密度、透明边和脚底。人物进入同场景时，以当前游戏的世界比例排列。对怪物按体型和威胁设相对比例，并检查敌我区分和主要行动部位。需要动画时按动作拆分角色、投射物与命中特效，保持各帧锚点和身份。
