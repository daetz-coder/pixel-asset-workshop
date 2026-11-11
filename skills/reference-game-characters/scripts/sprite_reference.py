#!/usr/bin/env python3
"""Extract source frames and compare existing sprites without redrawing them."""

import argparse
from collections import Counter
import json
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise SystemExit("Pillow is required. Use an environment with Pillow or `uv run --with pillow python`.")


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return number


def alpha_threshold(value):
    number = positive(value)
    if number > 255:
        raise argparse.ArgumentTypeError("expected an alpha threshold between 1 and 255")
    return number


def load(path):
    with Image.open(path) as original:
        return original.convert("RGBA")


def save_png(image, path):
    if path.suffix.lower() != ".png":
        raise ValueError("the output path must end in .png")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        image.save(output, format="PNG")


def rectangle(values, image, label):
    x, y, width, height = values
    if x < 0 or y < 0 or width < 1 or height < 1:
        raise ValueError(f"{label} needs a nonnegative origin and positive size")
    if x + width > image.width or y + height > image.height:
        raise ValueError(f"{label} is outside the {image.width}×{image.height} input")
    return x, y, x + width, y + height


def visible_bounds(alpha, threshold):
    return alpha.point([255 if value >= threshold else 0 for value in range(256)]).getbbox()


def inspect(args):
    image = load(args.image)
    alpha = image.getchannel("A")
    histogram = alpha.histogram()
    bounds = visible_bounds(alpha, args.alpha_threshold)
    colors = Counter()
    for count, pixel in image.getcolors(image.width * image.height):
        if pixel[3] >= 240:
            colors[pixel[:3]] += count
    return {
        "path": str(args.image),
        "size": image.size,
        "alpha_pixels": {
            "transparent": histogram[0],
            "partial": sum(histogram[1:255]),
            "opaque": histogram[255],
        },
        "nonzero_alpha_bbox_ltrb": alpha.getbbox(),
        "visible_alpha_threshold": args.alpha_threshold,
        "visible_bbox_ltrb": bounds,
        "visible_touches_canvas_edge": bool(bounds and (
            bounds[0] == 0 or bounds[1] == 0 or bounds[2] == image.width or bounds[3] == image.height
        )),
        "color_sample_min_alpha": 240,
        "common_near_opaque_colors": [
            {"hex": "#%02X%02X%02X" % rgb, "pixels": count} for rgb, count in colors.most_common(8)
        ],
    }


def extract(args):
    sheet = load(args.image)
    width, height = args.frame_size
    if sheet.width % width or sheet.height % height:
        raise ValueError(f"{sheet.width}×{sheet.height} is not divisible by frame size {width}×{height}")
    columns, rows = sheet.width // width, sheet.height // height
    if not 0 <= args.index < columns * rows:
        raise ValueError(f"frame index must be between 0 and {columns * rows - 1}")
    row, column = divmod(args.index, columns)
    frame_box = (column * width, row * height, (column + 1) * width, (row + 1) * height)
    frame = sheet.crop(frame_box)
    if args.crop:
        frame = frame.crop(rectangle(args.crop, frame, "crop"))
    if frame.getchannel("A").getbbox() is None:
        raise ValueError("the selected frame or crop is fully transparent")
    frame = enlarge(frame, args.scale)
    save_png(frame, args.out)
    return {
        "input": str(args.image),
        "frame_index": args.index,
        "frame_box_ltrb": frame_box,
        "crop_xywh": args.crop,
        "nearest_scale": args.scale,
        "output": str(args.out),
        "size": frame.size,
    }


def enlarge(image, scale):
    if scale == 1:
        return image
    return image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)


def prepare_panel(path, body, height, threshold):
    image = load(path)
    body_left, body_top, body_right, foot_y = rectangle(body, image, "body box")
    visible = visible_bounds(image.getchannel("A"), threshold)
    if visible is None:
        raise ValueError(f"{path} contains no pixels at or above alpha {threshold}")
    left, top, right, bottom = visible
    scale = height / (foot_y - body_top)
    crop = image.crop(visible)
    scaled = crop.resize((max(1, round((right - left) * scale)),
                          max(1, round((bottom - top) * scale))), Image.Resampling.NEAREST)
    # Offset from the body center and foot line, not the prop's bounds.
    x = round((left - (body_left + body_right) / 2) * scale)
    y = round((top - foot_y) * scale)
    return scaled, x, y, scale


def compare(args):
    panels = [
        prepare_panel(args.reference, args.reference_body_box, args.body_height, args.alpha_threshold),
        prepare_panel(args.candidate, args.candidate_body_box, args.body_height, args.alpha_threshold),
    ]
    left = min(0, *(x for _, x, _, _ in panels))
    right = max(0, *(x + sprite.width for sprite, x, _, _ in panels))
    top = min(-args.body_height, *(y for _, _, y, _ in panels))
    bottom = max(0, *(y + sprite.height for sprite, _, y, _ in panels))
    padding, gap, caption = 12, 6, 20
    panel_width = max(116, right - left + 2 * padding)
    panel_height = bottom - top + 2 * padding
    canvas = Image.new("RGBA", (2 * panel_width + gap, panel_height + caption), "#202530")
    draw = ImageDraw.Draw(canvas)
    baseline = caption + padding - top
    for index, (sprite, x, y, scale) in enumerate(panels):
        start = index * (panel_width + gap)
        draw.text((start + padding, 4), ("Reference", "Candidate")[index], fill="white")
        block = 8
        for yy in range(0, panel_height, block):
            for xx in range(0, panel_width, block):
                color = ("#CFD2D9", "#A6ABB7")[(xx // block + yy // block) % 2]
                draw.rectangle((start + xx, caption + yy, start + min(xx + block, panel_width) - 1,
                                caption + min(yy + block, panel_height) - 1), fill=color)
        draw.line((start + 2, baseline, start + 7, baseline), fill="#546075")
        draw.line((start + panel_width - 8, baseline, start + panel_width - 3, baseline), fill="#546075")
        x_origin = start + (panel_width - (right - left)) // 2 - left
        canvas.alpha_composite(sprite, (x_origin + x, baseline + y))
    preview = enlarge(canvas.convert("RGB"), args.zoom)
    save_png(preview, args.out)
    return {
        "output": str(args.out),
        "size": preview.size,
        "body_height_before_zoom": args.body_height,
        "nearest_zoom": args.zoom,
        "display_body_height": args.body_height * args.zoom,
        "baseline_y": baseline * args.zoom,
        "reference_scale_before_zoom": panels[0][3],
        "candidate_scale_before_zoom": panels[1][3],
        "visible_alpha_threshold": args.alpha_threshold,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True)

    info = commands.add_parser("inspect", help="report alpha, visible bounds and common colors")
    info.add_argument("image", type=Path)
    info.add_argument("--alpha-threshold", type=alpha_threshold, default=16)
    info.set_defaults(run=inspect)

    frame = commands.add_parser("extract", help="extract one frame from a uniform sheet")
    frame.add_argument("image", type=Path)
    frame.add_argument("--frame-size", type=positive, nargs=2, required=True, metavar=("W", "H"))
    frame.add_argument("--index", type=int, default=0, help="zero-based index in row-major order")
    frame.add_argument("--crop", type=int, nargs=4, metavar=("X", "Y", "W", "H"))
    frame.add_argument("--scale", type=positive, default=1, help="integer nearest-neighbor enlargement")
    frame.add_argument("--out", type=Path, required=True)
    frame.set_defaults(run=extract)

    review = commands.add_parser("compare", help="align two sprites by a manually selected body box")
    review.add_argument("reference", type=Path)
    review.add_argument("candidate", type=Path)
    for name in ("reference", "candidate"):
        review.add_argument(f"--{name}-body-box", type=int, nargs=4, required=True,
                            metavar=("X", "Y", "W", "H"), help="body extent excluding equipment and shadow")
    review.add_argument("--body-height", type=positive, required=True, help="game display height before zoom")
    review.add_argument("--zoom", type=positive, default=1, help="integer nearest-neighbor preview enlargement")
    review.add_argument("--alpha-threshold", type=alpha_threshold, default=16)
    review.add_argument("--out", type=Path, required=True)
    review.set_defaults(run=compare)

    args = parser.parse_args()
    try:
        report = args.run(args)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
