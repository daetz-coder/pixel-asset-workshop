---
name: spriteframe
description: Process a supplied character animation video into reviewed fixed-canvas PNG frames and a Godot 4 SpriteFrames resource. Use for local video-to-sprite workflows; this tool does not generate video or install assets into a game.
---

# SpriteFrame

[简体中文](SKILL.zh.md)

Run `python <skill-dir>/scripts/spriteframe.py --help`. The CLI uses Python 3.10+, Pillow, NumPy and FFmpeg. It can fall back to imageio-ffmpeg when FFmpeg is unavailable on PATH. In Pixel Asset Workshop, the workbench setup installs the Python dependencies. [Workbench setup](../../workbench/README.md)

Use a new output directory for each operation. `inspect` and `process` take `--video`, `--out`, `--duration` and optionally `--start` and `--fps`. `process` also takes `--size 128x128 --anchor 64,112`, optionally `--key 00ff00 --tolerance 60`, and the source acceptance flag. `approve` takes `--job` and `--reviewer`. `export-godot` takes `--job`, `--out`, `--name` and `--res-path res://sprites/attack`. Copy the output folder to that location inside the target Godot project.

1. Run `inspect` and view the contact sheet. Ask the user to approve the source clip, and specify a time window before processing. A source acceptance flag records this explicit human decision; do not set it on the user's behalf.
2. Run `process` with a single fixed transform, chosen output size and anchor. Flat-colour keying is optional and limited: inspect the output against both backgrounds, including at game size. Inspect every frame and the animation; automatic checks do not judge identity, weapon shape or motion. Reprocess into a new directory when necessary.
3. Only after the user explicitly accepts the processed frames, run `approve` with their name. `export-godot` checks approval and hashes of the frames, and creates a standalone Godot 4 resource package. Never treat automated QA or the agent's inspection as user approval.
4. Installation into a game, project-specific playback, live cloud generation, costs, and rollback are outside this local tool. Investigate the actual target project and get the appropriate authorization before modifying it. Never claim Godot loading or in-game playback was verified without running it.
