# 参考图生图提示词

[English](prompt-patterns.en.md)

按实际图像填写。给图像逐个编号并写明用途，调用时实际附上。

## 从画风档案生成同类资产

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

把最重要的验收条件放进提示词。建筑写清地基、入口朝向和屋顶投影。敌怪写清物种轮廓、攻击部位和预期身高。地块写清具体连接边和内外角。按钮写清常态、按下态的高光与位移，以及共享的边框结构、图标区和目标尺寸。图集生成后按实测拆分并验证接缝或拼装效果。

## 从原包校准新角色

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

若用户希望直接编辑某个已有角色，改用 `precise-object-edit`，说明它是编辑对象与允许修改的部位。若原帧只用作画风参考，不称它为需原样保留的角色身份。

## 以已确认的原创角色扩展职业

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

## 定向修订

附上待修订图作为编辑对象，必要时同时附确认版作为不变量参考。例：

```text
Use case: precise-object-edit
Image 1 is the candidate to repair; Image 2 is the approved anatomy reference.
Repair only the feet in Image 1 to match Image 2: [specific observed correction].
Preserve the current helmet, prop silhouette, face, hands, palette, body placement,
canvas margins and transparency. Output the same single full-body idle character.
```

## 尺寸和细节分开描述

用户只要文件放大时，用最近邻整数倍导出派生图；用户要更多细节时才请求模型重新生成，且重新检查像素密度。不要把简单放大描述为新增细节，也不要默认用高细节版替换已确认的粗像素基准。
