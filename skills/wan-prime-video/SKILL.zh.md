# Wan Prime 视频批次

[English](SKILL.md)

多名角色使用同一套视频设置时，在本地把他们合成一张首帧。每格一名角色，配一段动作提示词。六名角色可以合用一次 Wan 任务。动作所需时长不同，或者武器和动作在格内摆不下时，分成多批。

## 在本地合图

使用 Python 3、ImageMagick 和合图脚本。JSON 中的角色按从左到右、从上到下排列，图片路径相对 JSON 文件。透明 PNG 可以在裁去透明边后按脚底对齐。 [compose_reference.py](scripts/compose_reference.py)

```json
{
  "roles": [
    {"name": "战锤兵", "image": "hammer.png", "action": "attack", "motion": "举锤，向右下砸一次，再收锤归位。"},
    {"name": "投弹兵", "image": "grenadier.png", "action": "run", "motion": "原地奔跑，双脚交替落地。"}
  ]
}
```

在仓库根目录运行。

```bash
python3 skills/wan-prime-video/scripts/compose_reference.py \
  --config ./batch.json --output ./batch-reference.png
```

输出 `batch-reference.png`、`batch-reference-prompt.txt` 和 `batch-reference-layout.json`。脚本默认按每个角色的可用空间选择网格。用 `cols`、`rows` 指定格位。默认画布为 1280 × 720，使用洋红抠像底色、统一缩放和脚底线。可选配置项有 `width`、`height`、`color`、`scale`、`baseline`、`duration`、`resolution` 和默认 `action`。合图支持 `idle`、`walk`、`run` 和 `attack`。检查合图以及每格的动作空间。自定义姿势和复杂动作可使用 `sprite-motion-prompts`。

只需要首帧或提示词时，在本地准备即可。生成视频时，每批向脚本提交一次合图和提示词。使用 `--ratio adaptive` 保持布局对应，时长和分辨率按批次配置。将 MP4 和格位 JSON 一起交付。在 SpriteFrame「逐帧」中使用「导入格位 JSON」，再打开同批视频。拆帧工具按成片实际尺寸换算已占用的格位。

## 生成视频

按项目和用户要求确定输入图、提示词、输出位置与设置。默认使用 5 秒、480P、16:9，关闭音频和提示词改写。透明区与画面比例留白默认填纯洋红。使用提示词文本，或把所选提示词保存为 UTF-8 文本文件。

在仓库根目录运行。

```bash
python3 scripts/generate_wan_video.py \
  --image ./reference.png \
  --prompt-file ./run-prompt.txt \
  --resolution 480P --ratio 16:9 --duration 5 \
  --output ./run.mp4
```

短提示词可直接用 `--prompt`。分辨率支持 480P、720P、1080P，时长支持 2–30 整秒。用 `--ratio adaptive` 保留输入图比例，`--background '#RRGGBB'` 指定抠像底色，`--audio` 或 `--prompt-extend` 启用音频或提示词改写。脚本需要 Python 3 和 ImageMagick。省略输出路径时，视频保存为当前目录的 `<image-stem>-wan-prime.mp4`。

`DASHSCOPE_WORKSPACE` 填 Model Studio 工作空间 ID，`DASHSCOPE_REGION` 填区域，默认为 `cn-beijing`。脚本使用环境变量 `DASHSCOPE_API_KEY`，或读取 macOS 钥匙串中账号 `codex`、服务名 `codex.wan-prime-video.<workspace-id>` 的条目。将凭据保存在环境或钥匙串中。可使用 `--dry-run` 在本地校验输入和设置，无需工作空间、凭据或付费任务。

## 取回并交付成片

服务接受请求后，脚本会打印任务 ID。任务完成后交付已保存的 MP4。轮询或下载中断时，使用同一工作空间和 `--task-id <id> --output <path>` 继续。如果请求状态不明且没有收到任务 ID，先到 Model Studio 核对。每次接受请求都会创建一个新生成任务。 [Alibaba Cloud Wan3.0 API 参考](https://help.aliyun.com/en/model-studio/wan3-video-generation-api-reference)

项目实测案例包含实际提交的提示词、源视频、裁切格位，以及用已有成片本地复现拆帧的方法。 [Tiny Swords 实测案例](../../examples/tiny-swords/README.zh.md)
