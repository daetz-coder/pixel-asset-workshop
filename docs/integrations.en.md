# Tools and integrations

[简体中文](integrations.md) · [Project home](../README.en.md)

| Component | Input → Output | Account requirement |
| --- | --- | --- |
| Reference art skill | Reference frames and notes → style profile, prompts, comparisons and review criteria | Local analysis requires no account. Image generation depends on the provider. |
| Wan composition skill and CLI | Local transparent PNGs and batch config → first frame, prompt and layout JSON | None for composition |
| Wan API or model interface | First frame, prompt, duration and resolution → MP4 | Provider authorization and billing apply to new tasks |
| Local extraction CLI or SpriteFrame | MP4 and matching layout JSON → transparent PNGs for each character | None for local processing |

## Models and MCP

Use any video model with first-frame input. Submit the composite and per-cell prompts, preserve the aspect ratio and cell positions, and disable automatic camera movement. Process the downloaded clip locally. The Wan client is an optional adapter. Its settings depend on the model and workspace. [Alibaba Cloud Wan API reference](https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-api-reference/)

If your environment has image or video MCP tools, use them to generate art or submit video jobs and keep the original PNG or MP4 locally. The provider determines parameters, upload methods, model names, job states and usage. The composition and extraction interfaces work with local files and require no particular agent, client or MCP server.

## SpriteFrame

In SpriteFrame, select “导入格位 JSON” in the asset panel to import the layout, then open the MP4 from the same batch. Check the grid and key color. Extract at 10 fps and review the frames, or choose an action's time range before sampling. Use the full cell or inspect the motion envelope if auto-detection clips weapons or particles. The command-line tools and included clip can reproduce the export independently. [Local example](../README.en.md#reproduce-the-example-offline)

## Layout format v1

`width` and `height` describe the first frame in pixels. `cols` and `rows` define the grid. `color` is a six-digit hex key color. `baseline` is the foot line within a cell, expressed as a fraction from 0 to 1. Each item in `cells[]` has zero-based `row` and `col` values, a display `name`, and an optional `action` that overrides the batch label. The extractor supports `idle`, `walk`, `run`, `attack` and `vfx`. Standalone effects omit the foot anchor.

The exporter computes column boundaries with `roundHalfUp(col × video width / cols)` and row boundaries the same way using video height. Neighbors share a boundary. Crop metadata uses `[x,y,width,height]`. Foot anchors are relative to the top-left corner of each PNG. The CLI expects square video pixels and an aspect ratio within 1% of the reference. Correct letterboxing, rotation or framing drift before extraction. Output directories are named by row, column and action. The manifest retains the character names.

## Before importing into a game

- Use `--start` and `--end` to select a time range and `--fps` to sample uniformly. Review at the source frame rate first to locate brief release or impact poses.
- `--tolerance` defaults to 48 and uses the largest RGB channel difference from the key color. Check the actual background color if fringe pixels remain. Lower the tolerance or use a different key color if sprite or effect pixels disappear. Review each sequence and use `empty_frames` and `edge_frames` to locate flagged frames.
- Extracted PNGs retain the full cell and the video's pixel scale. Check character identity, feet, equipment and transparency before selecting loop or one-shot frames. Use nearest-neighbor sampling when resizing. Export projectiles, hits and characters separately and synchronize them with game events.
