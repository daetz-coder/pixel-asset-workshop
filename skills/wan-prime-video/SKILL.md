---
name: wan-prime-video
description: Batch multiple local sprite images into one Wan3.0-Video-Prime first frame with per-role prompts and a matching crop layout. Use for cost-conscious sprite animation batches, single-image Wan Prime generation, or resuming an existing Wan Prime task.
---

# Wan Prime Video

[简体中文](SKILL.zh.md)

When given multiple roles for the same video settings, compose them locally into one first frame. Each role gets its own cell and motion text. A batch uses one Wan task, so six roles can share a single submission. Use separate batches when motions need different durations or when the shared canvas leaves too little room for equipment or motion.

## Prepare a batch locally

Use [compose_reference.py](scripts/compose_reference.py) with Python 3 and ImageMagick. Make a JSON file listing the role images in reading order. Paths are relative to the JSON file. Transparent PNGs preserve clean edges and make it possible to align feet after trimming transparent margins.

```json
{
  "roles": [
    {"name": "Warhammer", "image": "hammer.png", "action": "attack", "motion": "Raise the hammer, strike down to the right once, and recover."},
    {"name": "Grenadier", "image": "grenadier.png", "action": "run", "motion": "Run in place with alternating foot contacts."}
  ]
}
```

```bash
python3 ~/.codex/skills/wan-prime-video/scripts/compose_reference.py \
  --config ./batch.json --output ./batch-reference.png
```

This writes `batch-reference.png`, `batch-reference-prompt.txt`, and `batch-reference-layout.json`. It chooses a grid that maximizes space per role. Supply `cols` and/or `rows` to control the layout. The default is a 1280 × 720 canvas with a magenta key, common scale, and aligned feet. Optional config keys are `width`, `height`, `color`, `scale`, `baseline`, `duration`, `resolution`, and a default `action`. Supported actions are `idle`, `walk`, `run`, and `attack`. Review the composite and each cell's motion clearance. For custom poses or complex action prompts, use `$sprite-motion-prompts`.

Local preparation is sufficient when the user asks only for the reference or prompt. When generation is requested, pass the combined PNG and combined prompt to the runner **once per batch**. Set `--ratio adaptive` so the composition stays aligned with its layout. Match `--duration` and `--resolution` to the batch config. Deliver the layout JSON with the MP4. In 逐帧, import the JSON via 「导入格位 JSON」 and load the video. The extractor maps the saved occupied cells to the actual video size.

## Generate a clip

Resolve the user's image, prompt, output location, and settings from the request and project. Default to 5 seconds, 480P, 16:9, audio off, prompt rewriting off, and a solid magenta fill for transparent sprites and aspect-ratio padding. Honor the supplied settings. Provide prompt text or write just the selected prompt block to a UTF-8 text file.

Run the bundled script by its absolute path. For example, with the default Codex skill location:

```bash
python3 ~/.codex/skills/wan-prime-video/scripts/generate_wan_video.py \
  --image ./reference.png \
  --prompt-file ./run-prompt.txt \
  --resolution 480P --ratio 16:9 --duration 5 \
  --output ./run.mp4
```

Use `--prompt` for a short inline prompt. Resolution supports 480P, 720P, and 1080P. Duration supports 2–30 whole seconds. Use `--ratio adaptive` to keep the input image proportions. Set `--background '#RRGGBB'` for a different key color. Set `--audio` or `--prompt-extend` when requested. The runner requires Python 3 and ImageMagick. With no output path, it saves `<image-stem>-wan-prime.mp4` in the working directory.

Set `DASHSCOPE_WORKSPACE` to your Model Studio workspace ID and `DASHSCOPE_REGION` to its region (defaults to `cn-beijing`). The runner uses `DASHSCOPE_API_KEY` or reads the macOS Keychain item for account `codex` and service `codex.wan-prime-video.<workspace-id>`. Keep credentials in the environment or Keychain and out of prompts, command arguments, and output. Add `--dry-run` to validate the inputs and settings locally without a workspace, credential or paid submission.

## Retrieve and deliver

The runner prints the task ID as soon as Alibaba accepts it. Wait for the task and link the saved MP4. If polling or the download is interrupted, run the same script with `--task-id <id> --output <path>` and the same workspace. If submission status is uncertain and no ID was returned, check Model Studio before submitting again. Each accepted submission is a separate generation.

See [Alibaba Cloud's Wan3.0 API reference](https://help.aliyun.com/en/model-studio/wan3-video-generation-api-reference) for model settings and response details.

The Pixel Asset Workshop example includes the exact submitted prompt, source clip and crop layout. It also shows how to extract the saved video locally without submitting another task. [Tiny Swords case study](../../examples/tiny-swords/README.md)
