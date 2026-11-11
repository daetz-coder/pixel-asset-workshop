"""Export paired PNG sheets and GIFs from the cleaned six-unit sample."""
import argparse
import json
from pathlib import Path

from PIL import Image


# Twelve poses per unit, sampled around the action in the mixed clip.
SELECTIONS = {
    "Warhammer Infantry": ("warhammer", 14),
    "Grenadier": ("grenadier", 16),
    "Standard Bearer": ("standard-bearer", 20),
    "Axe Infantry": ("axe", 24),
    "Crossbow Infantry": ("crossbow", 24),
    "Tower Shield Infantry": ("tower-shield", 26),
}
COLUMNS = 6


def export_unit(source, output, region, fps):
    name = region["name"]
    slug, start = SELECTIONS[name]
    indices = list(range(start, start + 24, 2))
    frames = []
    for index in indices:
        with Image.open(source / region["directory"] / f"{index:04d}.png") as image:
            frames.append(image.convert("RGBA"))

    anchor_x, anchor_y = region["anchor_xy"]
    boxes = [frame.getbbox() for frame in frames]
    left = max(0, min(box[0] for box in boxes) - 4)
    top = max(0, min(box[1] for box in boxes) - 4)
    right = min(frames[0].width, max(box[2] for box in boxes) + 4)
    bottom = min(frames[0].height, max(box[3] for box in boxes) + 4)
    width, height = right - left, bottom - top

    sheet_name = f"{slug}-sheet.png"
    gif_name = f"{slug}.gif"
    sheet = Image.new("RGBA", (COLUMNS * width, 2 * height))
    gif_frames = []
    entries = []
    duration_ms = round(2000 / fps)
    for slot, (index, image) in enumerate(zip(indices, frames)):
        frame = image.crop((left, top, right, bottom))
        row, col = divmod(slot, COLUMNS)
        x, y = col * width, row * height
        sheet.paste(frame, (x, y))
        entries.append({"source_index": index, "rect_xywh": [x, y, width, height],
                        "duration_ms": duration_ms})

        # Reserve one palette index for the GIF's binary transparency.
        paletted = frame.convert("RGB").quantize(colors=255, dither=Image.Dither.NONE)
        mask = frame.getchannel("A").point(lambda alpha: 255 if alpha < 128 else 0)
        paletted.paste(255, mask=mask)
        gif_frames.append(paletted)

    sheet.save(output / sheet_name)
    gif_frames[0].save(output / gif_name, save_all=True, append_images=gif_frames[1:],
                       duration=duration_ms, loop=0, disposal=2, transparency=255)
    return {"name": name, "sheet": sheet_name, "gif": gif_name,
            "cell_size": [width, height], "anchor_xy": [anchor_x - left, anchor_y - top],
            "frames": entries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads((args.frames / "manifest.json").read_text(encoding="utf-8"))
    fps = manifest["sampling"]["fps"]
    if fps != 10:
        parser.error("The selected source indices require the sample extracted at 10 fps.")
    regions = {region["name"]: region for region in manifest["regions"]}
    for name, (_, start) in SELECTIONS.items():
        if name not in regions or regions[name]["frames"] <= start + 22:
            parser.error(f"Missing the expected sample sequence for {name}.")

    args.out.mkdir(parents=True, exist_ok=True)
    exports = [export_unit(args.frames, args.out, regions[name], fps) for name in SELECTIONS]
    metadata = {"source": manifest["source"], "source_fps": fps, "columns": COLUMNS,
                "rows": 2, "sequences": exports}
    (args.out / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
