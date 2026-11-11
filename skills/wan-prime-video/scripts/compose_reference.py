"""Build one Wan first frame, one prompt and a matching crop layout from local sprites."""

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ACTIONS = {
    "idle": "Breathe gently in place and return to the starting pose.",
    "walk": "Walk in place through a complete looping step cycle.",
    "run": "Run in place through a complete looping stride cycle.",
    "attack": "Perform one attack with anticipation, a clear impact, follow-through, and recovery.",
}


def magick(*args):
    result = subprocess.run(["magick", *map(str, args)], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def bounded_int(value, minimum, maximum, label):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{label} must be an integer from {minimum} to {maximum}")
    return value


def fraction(value, low, high, label):
    if type(value) not in (int, float) or not low <= value <= high:
        raise ValueError(f"{label} must be between {low} and {high}")
    return value


def grid_for(count, width, height, cols, rows):
    if cols is not None:
        cols = bounded_int(cols, 1, 8, "cols")
    if rows is not None:
        rows = bounded_int(rows, 1, 8, "rows")
    candidates = [(c, r) for c in range(1, 9) for r in range(1, 9)
                  if c * r >= count and cols in (None, c) and rows in (None, r)]
    if not candidates:
        raise ValueError("the grid has fewer cells than sprites")
    return max(candidates, key=lambda pair: (
        min(width / pair[0], height / pair[1]), count - pair[0] * pair[1],
        -abs(math.log(width * pair[1] / (height * pair[0]))),
    ))


def load_roles(config, folder, default_action):
    roles = config.get("roles")
    if not isinstance(roles, list) or not 1 <= len(roles) <= 64:
        raise ValueError("roles must contain 1–64 sprites")
    result = []
    for index, role in enumerate(roles, 1):
        if not isinstance(role, dict) or not isinstance(role.get("image"), str):
            raise ValueError(f"role {index} needs an image path")
        source = (folder / role["image"]).resolve()
        if not source.is_file():
            raise ValueError(f"sprite image does not exist: {source}")
        name = role.get("name", source.stem)
        action = role.get("action", default_action)
        if not isinstance(name, str) or not 1 <= len(name.strip()) <= 80:
            raise ValueError(f"role {index} needs a name of 1–80 characters")
        if not isinstance(action, str) or action not in ACTIONS:
            raise ValueError(f"role {index} has an unsupported action")
        motion = role.get("motion", ACTIONS[action])
        if not isinstance(motion, str) or not 1 <= len(motion.strip()) <= 4000:
            raise ValueError(f"role {index} needs motion text of 1–4000 characters")
        result.append((source, " ".join(name.split()), action, motion.strip()))
    return result


def stage_sprite(source, normalized):
    magick(f"{source}[0]", "-auto-orient", "+repage", f"PNG32:{normalized}")
    bounds = magick(normalized, "-alpha", "extract", "-threshold", "6%",
                    "-bordercolor", "black", "-border", "1", "-format", "%@", "info:")
    match = re.fullmatch(r"(\d+)x(\d+)\+(\d+)\+(\d+)", bounds)
    if not match or not int(match[1]) or not int(match[2]):
        raise ValueError(f"sprite contains no visible pixels: {source}")
    width, height, x, y = map(int, match.groups())
    return width, height, x - 1, y - 1


def build(config_path, output):
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("config must be a JSON object")
    if output.suffix.lower() != ".png":
        raise ValueError("output must end in .png")
    prompt_path = output.with_name(output.stem + "-prompt.txt")
    layout_path = output.with_name(output.stem + "-layout.json")
    for destination in (output, prompt_path, layout_path):
        if destination.exists():
            raise FileExistsError(f"output already exists: {destination}")
    width = bounded_int(config.get("width", 1280), 240, 4096, "width")
    height = bounded_int(config.get("height", 720), 240, 4096, "height")
    if max(width, height) > 8 * min(width, height):
        raise ValueError("the canvas aspect ratio cannot exceed 8:1")
    duration = bounded_int(config.get("duration", 5), 2, 30, "duration")
    resolution = config.get("resolution", "480P")
    if resolution not in ("480P", "720P", "1080P"):
        raise ValueError("resolution must be 480P, 720P, or 1080P")
    color = config.get("color", "#ff00ff")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise ValueError("color must be a six-digit RGB hex color")
    color = color.lower()
    scale = fraction(config.get("scale", 0.5), 0.1, 0.95, "scale")
    baseline = fraction(config.get("baseline", 0.7), 0.1, 0.95, "baseline")
    action = config.get("action", "idle")
    if not isinstance(action, str) or action not in ACTIONS:
        raise ValueError("unsupported default action")
    roles = load_roles(config, config_path.resolve().parent, action)
    cols, rows = grid_for(len(roles), width, height, config.get("cols"), config.get("rows"))
    layout = {"version": 1, "width": width, "height": height, "rows": rows, "cols": cols,
              "color": color, "baseline": baseline, "action": action, "cells": []}
    prompt = [
        f"Use the input image as the first frame of one {duration}-second {resolution} video.",
        f"Keep the full canvas and a fixed {color.upper()} background with {cols} columns and {rows} rows.",
        "Animate every listed cell independently and simultaneously. Each role, its equipment, and its entire motion stay in its cell. "
        "Preserve the first frame's identity, pixel edges, palette, facing, proportions, and foot anchor. "
        "Lock the camera. Leave unlisted cells empty. Keep the frame free of grid lines, text, extra characters, and scenery.",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".wan-reference-", dir=output.parent) as temp:
        folder = Path(temp)
        sprites = []
        for i, (source, name, role_action, motion) in enumerate(roles):
            sprite = folder / f"sprite-{i}.png"
            sprites.append((sprite, stage_sprite(source, sprite)))
            row, col = divmod(i, cols)
            layout["cells"].append({"row": row, "col": col, "name": name, "action": role_action, "motion": motion})
            prompt.extend(("", f"Row {row + 1}, column {col + 1} · {name}", motion))
            if motion != ACTIONS[role_action]:
                prompt.append(ACTIONS[role_action])
        prompt_text = "\n".join(prompt) + "\n"
        if len(prompt_text) > 20000:
            raise ValueError("combined prompt exceeds 20,000 characters")
        cell_width, cell_height = width / cols, height / rows
        factor = min(cell_width * scale / max(rect[0] for _, rect in sprites),
                     cell_height * min(scale, baseline) / max(rect[1] for _, rect in sprites))
        args = ["-size", f"{width}x{height}", f"xc:{color}"]
        for (sprite, (sw, sh, sx, sy)), cell in zip(sprites, layout["cells"]):
            rw, rh = max(1, round(sw * factor)), max(1, round(sh * factor))
            center_x = int((cell["col"] + 0.5) * cell_width + 0.5)
            foot_y = int((cell["row"] + baseline) * cell_height + 0.5)
            x = center_x - (rw + 1) // 2
            y = foot_y - rh
            args.extend(("(", sprite, "-crop", f"{sw}x{sh}+{sx}+{sy}", "+repage",
                         "-filter", "point", "-resize", f"{rw}x{rh}!", ")", "-geometry",
                         f"{x:+d}{y:+d}", "-compose", "Over", "-composite"))
        image = folder / "reference.png"
        magick(*args, f"PNG24:{image}")
        prompt_file, layout_file = folder / "prompt.txt", folder / "layout.json"
        prompt_file.write_text(prompt_text, encoding="utf-8")
        layout_file.write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created = []
        try:
            for staged, destination in ((image, output), (prompt_file, prompt_path), (layout_file, layout_path)):
                os.link(staged, destination)
                created.append(destination)
        except OSError:
            for destination in created:
                destination.unlink()
            raise
    return output, prompt_path, layout_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="JSON batch config. Image paths are relative to it.")
    parser.add_argument("--output", type=Path, required=True, help="First-frame PNG destination")
    args = parser.parse_args()
    if shutil.which("magick") is None:
        parser.error("ImageMagick (magick) is required")
    try:
        for result in build(args.config, args.output):
            print(result.resolve())
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    except subprocess.CalledProcessError as error:
        parser.exit(1, f"ImageMagick: {error.stderr.strip()}\n")


if __name__ == "__main__":
    main()
