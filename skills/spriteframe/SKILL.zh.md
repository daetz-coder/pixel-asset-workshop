# SpriteFrame 逐帧技能

[English](SKILL.md)

使用本地视频检查、固定画布处理和导出命令，将审核通过的单个动作保存为透明 PNG 和 Godot 4 的 `SpriteFrames` 资源。[工作台与依赖安装](../../workbench/README.zh.md)

从仓库根目录查看命令参数：

```sh
workbench/.venv/bin/python skills/spriteframe/scripts/spriteframe.py --help
```

先用 `inspect` 查看原片，再用 `process` 对选定时段抠像并按统一脚底锚点排帧。检查联系表与 GIF 后，用 `approve` 记录审核。运行 `export-godot` 时，`--res-path` 要与目标游戏内的文件夹位置一致。
