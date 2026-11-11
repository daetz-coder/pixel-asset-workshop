#!/usr/bin/env python3
"""Extract fixed-size RGBA sprite sequences from a video and a v1 grid layout."""

import argparse
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops

ACTIONS = {"idle", "walk", "run", "attack", "vfx"}


def integer(value, low, high):
    return type(value) is int and low <= value <= high


def load_layout(path):
    layout = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(layout, dict) or not integer(layout.get("version"), 1, 1):
        raise ValueError("expected a version 1 layout object")
    for key, maximum in (("width", 8000), ("height", 8000), ("rows", 8), ("cols", 8)):
        if not integer(layout.get(key), 1, maximum):
            raise ValueError(f"invalid layout {key}")
    color = layout.get("color")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise ValueError("layout color must be #RRGGBB")
    baseline = layout.get("baseline")
    if type(baseline) not in (int, float) or not 0 <= baseline <= 1:
        raise ValueError("layout baseline must be between 0 and 1")
    default = layout.get("action")
    if not isinstance(default, str) or default not in ACTIONS:
        raise ValueError("invalid default layout action")
    cells = layout.get("cells")
    if not isinstance(cells, list) or not cells:
        raise ValueError("layout needs at least one occupied cell")
    seen = set()
    for cell in cells:
        if not isinstance(cell, dict) or not (
            integer(cell.get("row"), 0, layout["rows"] - 1)
            and integer(cell.get("col"), 0, layout["cols"] - 1)
        ):
            raise ValueError("invalid cell coordinates")
        coord = cell["row"], cell["col"]
        if coord in seen:
            raise ValueError(f"duplicate cell: {coord}")
        seen.add(coord)
        name, action = cell.get("name"), cell.get("action", default)
        if not isinstance(name, str) or not name.strip() or len(name) > 160:
            raise ValueError(f"invalid cell name: {coord}")
        if not isinstance(action, str) or action not in ACTIONS:
            raise ValueError(f"invalid cell action: {coord}")
    return layout


def half_up(value):
    return math.floor(value + 0.5)


def regions_for(layout, width, height):
    rows, cols = layout["rows"], layout["cols"]
    for cell in layout["cells"]:
        row, col = cell["row"], cell["col"]
        x = half_up(col * width / cols)
        y = half_up(row * height / rows)
        right = half_up((col + 1) * width / cols)
        bottom = half_up((row + 1) * height / rows)
        action = cell.get("action", layout["action"])
        anchor = None if action == "vfx" else [
            half_up((col + 0.5) * width / cols) - x,
            half_up((row + layout["baseline"]) * height / rows) - y,
        ]
        yield {
            "row": row, "col": col, "name": cell["name"], "layout_action": action,
            "directory": f"r{row + 1:02d}c{col + 1:02d}/{action}",
            "crop_xywh": [x, y, right - x, bottom - y],
            "anchor_xy": anchor, "empty_frames": [], "edge_frames": [],
        }


def chroma_key(rgb, key, tolerance):
    # Max channel distance treats compressed variations of the key as background.
    r, g, b = ImageChops.difference(rgb, key).split()
    distance = ImageChops.lighter(ImageChops.lighter(r, g), b)
    alpha = distance.point([0] * (tolerance + 1) + [255] * (255 - tolerance))
    # Clear RGB in fully transparent pixels too.
    return Image.composite(rgb, Image.new("RGB", rgb.size), alpha), alpha


def probe(video):
    output = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,avg_frame_rate,sample_aspect_ratio",
        "-of", "json", str(video),
    ])
    streams = json.loads(output).get("streams", [])
    if not streams:
        raise ValueError("no video stream found")
    return streams[0]


def extract(video, layout_path, out, fps, start, end, tolerance):
    video, out = video.resolve(strict=True), out.resolve()
    if out.exists():
        raise FileExistsError(f"output already exists: {out}")
    layout = load_layout(layout_path)
    source = probe(video)
    width, height = source["width"], source["height"]
    if (width < layout["cols"] or height < layout["rows"]
            or abs(width / height / (layout["width"] / layout["height"]) - 1) > 0.01
            or source.get("sample_aspect_ratio") not in (None, "N/A", "1:1", "0:1")):
        raise ValueError("video must match the reference aspect ratio and use square pixels")
    color = layout["color"]
    regions = list(regions_for(layout, width, height))
    command = ["ffmpeg", "-v", "error", "-nostdin", "-ss", str(start),
               "-noautorotate", "-i", str(video), "-map", "0:v:0"]
    if end is not None:
        command += ["-t", str(end - start)]
    command += ["-vf", f"fps={fps}", "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"]
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".sprite-extract-", dir=out.parent) as temporary:
        staged = Path(temporary) / "frames"
        for region in regions:
            (staged / region["directory"]).mkdir(parents=True)
        key = Image.new("RGB", (width, height), color)
        count = 0
        with subprocess.Popen(command, stdout=subprocess.PIPE) as decoder:
            try:
                while data := decoder.stdout.read(width * height * 3):
                    if len(data) != width * height * 3:
                        raise RuntimeError("FFmpeg returned a partial frame")
                    frame = Image.frombytes("RGB", (width, height), data)
                    frame, alpha = chroma_key(frame, key, tolerance)
                    frame.putalpha(alpha)
                    for region in regions:
                        x, y, w, h = region["crop_xywh"]
                        sprite = frame.crop((x, y, x + w, y + h))
                        bounds = sprite.getchannel("A").getbbox()
                        if bounds is None:
                            region["empty_frames"].append(count)
                        elif bounds[0] == 0 or bounds[1] == 0 or bounds[2] == w or bounds[3] == h:
                            region["edge_frames"].append(count)
                        sprite.save(staged / region["directory"] / f"{count:04d}.png")
                    count += 1
                if decoder.wait():
                    raise RuntimeError("FFmpeg failed to decode the clip")
            finally:
                if decoder.poll() is None:
                    decoder.kill()
        if not count:
            raise ValueError("no frames in the selected time range")
        for region in regions:
            region["frames"] = count
        manifest = {
            "version": 1, "status": "unreviewed", "source": video.name,
            "source_size": [width, height], "source_fps": source.get("avg_frame_rate"),
            "reference_size": [layout["width"], layout["height"]],
            "sampling": {"start_seconds": start, "end_seconds": end, "fps": fps,
                         "frame_duration_seconds": 1 / fps},
            "key": {"color": color, "max_channel_tolerance": tolerance},
            "regions": regions,
        }
        (staged / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        staged.rename(out)
    return count, len(regions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--layout", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="new output directory")
    parser.add_argument("--fps", type=float, default=10)
    parser.add_argument("--start", type=float, default=0, help="start time in seconds")
    parser.add_argument("--end", type=float, help="exclusive end time in seconds")
    parser.add_argument("--tolerance", type=int, default=48, help="RGB key tolerance (0–254)")
    args = parser.parse_args()
    if not 0 < args.fps <= 120 or not (math.isfinite(args.start) and args.start >= 0):
        parser.error("fps must be in (0, 120] and start must be finite and nonnegative")
    if args.end is not None and not (math.isfinite(args.end) and args.end > args.start):
        parser.error("end must be finite and greater than start")
    if not 0 <= args.tolerance <= 254:
        parser.error("tolerance must be in 0–254")
    if any(not shutil.which(tool) for tool in ("ffmpeg", "ffprobe")):
        parser.error("FFmpeg and ffprobe are required")
    try:
        count, regions = extract(args.video, args.layout, args.out, args.fps,
                                 args.start, args.end, args.tolerance)
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"{regions} cells × {count} frames → {args.out / 'manifest.json'}")


if __name__ == "__main__":
    main()
