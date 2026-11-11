#!/usr/bin/env python3
"""Local, review-gated sprite processing. No network or project mutation."""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def ffmpeg():
    exe = shutil.which('ffmpeg')
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as e:
        raise ValueError('Install imageio-ffmpeg or add ffmpeg to PATH') from e


def decode(video, start, duration, fps, directory):
    if not video.is_file():
        raise ValueError(f'Video not found: {video}')
    cmd = [ffmpeg(), '-hide_banner', '-loglevel', 'error', '-ss', str(start),
           '-i', str(video), '-t', str(duration), '-vf', f'fps={fps}',
           '-fps_mode', 'passthrough', str(directory / '%05d.png')]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise ValueError('FFmpeg decode failed: ' + p.stderr.strip())
    files = sorted(directory.glob('*.png'))
    if not files:
        raise ValueError('No frames decoded; check the selected time window')
    return files


def contact(images, path):
    thumb_w, thumb_h = 160, 160
    cols = min(5, len(images))
    rows = math.ceil(len(images) / cols)
    sheet = Image.new('RGB', (cols * thumb_w, rows * (thumb_h + 20)), '#303030')
    draw = ImageDraw.Draw(sheet)
    for i, im in enumerate(images):
        frame = im.convert('RGBA').copy()
        frame.thumbnail((thumb_w, thumb_h), Image.Resampling.NEAREST)
        x, y = i % cols * thumb_w, i // cols * (thumb_h + 20)
        sheet.paste(frame, (x + (thumb_w-frame.width)//2, y + (thumb_h-frame.height)//2), frame)
        draw.text((x + 4, y + thumb_h + 2), str(i), fill='white')
    sheet.save(path)


def make_output(out, action):
    out = out.resolve()
    if out.exists():
        raise ValueError(f'Output already exists: {out}')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.spriteframe-', dir=out.parent) as temp:
        staging = Path(temp) / 'result'
        staging.mkdir()
        action(staging)
        staging.rename(out)
    print(f'Created: {out}')


def inspect(args):
    def run(out):
        with tempfile.TemporaryDirectory() as temp:
            files = decode(args.video, args.start, args.duration, args.fps, Path(temp))
            images = [Image.open(p).convert('RGBA') for p in files]
            contact(images, out / 'contact.png')
        (out / 'source.json').write_text(json.dumps({'video': str(args.video.resolve()),
            'sha256': digest(args.video), 'start': args.start, 'duration': args.duration,
            'fps': args.fps, 'frames': len(images)}, indent=2), encoding='utf-8')
    make_output(args.out, run)


def parse_pair(value, separator):
    try:
        result = tuple(int(v) for v in value.lower().split(separator))
        if len(result) != 2:
            raise ValueError()
        return result
    except ValueError as e:
        raise ValueError(f'Invalid pair: {value}') from e


def process(args):
    if not args.source_accepted:
        raise ValueError('Source must be explicitly reviewed and accepted before processing')
    width, height = parse_pair(args.size, 'x')
    ax, ay = parse_pair(args.anchor, ',')
    if width <= 0 or height <= 0 or not (0 <= ax <= width and 0 <= ay <= height):
        raise ValueError('Size must be positive and anchor within canvas')
    if args.key and not re.fullmatch(r'[0-9a-fA-F]{6}', args.key):
        raise ValueError('Key must be six hex digits, e.g. 00ff00')
    if not 0 <= args.tolerance <= 441:
        raise ValueError('Tolerance must be between 0 and 441')

    def run(out):
        with tempfile.TemporaryDirectory() as temp:
            files = decode(args.video, args.start, args.duration, args.fps, Path(temp))
            frames = [Image.open(p).convert('RGBA') for p in files]
        if args.key:
            key = tuple(int(args.key[i:i+2], 16) for i in (0, 2, 4))
            for i, im in enumerate(frames):
                pixels = np.array(im)
                delta = pixels[:, :, :3].astype(np.int32) - np.array(key, dtype=np.int32)
                mask = np.sum(delta * delta, axis=2) <= args.tolerance**2
                pixels[mask] = 0
                frames[i] = Image.fromarray(pixels, 'RGBA')
        boxes = [im.getchannel('A').getbbox() for im in frames]
        if any(box is None for box in boxes):
            raise ValueError('Hard error: at least one empty frame')
        # A common bounding box and transform preserves relative motion across the clip.
        union = (min(b[0] for b in boxes), min(b[1] for b in boxes),
                 max(b[2] for b in boxes), max(b[3] for b in boxes))
        left, top, right, bottom = union
        available_w = 2 * min(ax, width-ax)
        if available_w <= 0 or ay <= 0:
            raise ValueError('Anchor leaves no room for subject')
        scale = min(available_w/(right-left), ay/(bottom-top))
        target_w = max(1, round((right-left)*scale))
        target_h = max(1, round((bottom-top)*scale))
        pos = (ax-target_w//2, ay-target_h)
        output = out / 'frames'
        output.mkdir()
        final = []
        for i, im in enumerate(frames):
            crop = im.crop(union).resize((target_w, target_h), Image.Resampling.NEAREST)
            canvas = Image.new('RGBA', (width, height))
            canvas.alpha_composite(crop, pos)
            if not canvas.getchannel('A').getbbox():
                raise ValueError(f'Hard error: frame {i} is empty after processing')
            canvas.save(output / f'{i:04}.png')
            final.append(canvas)
        contact(final, out / 'contact.png')
        for colour, name in [('#202020', 'dark'), ('#eeeeee', 'light')]:
            previews = []
            for im in final:
                bg = Image.new('RGBA', im.size, colour)
                bg.alpha_composite(im)
                previews.append(bg.convert('RGB'))
            previews[0].save(out / f'preview-{name}.gif', save_all=True,
                             append_images=previews[1:], duration=round(1000/args.fps), loop=0, disposal=2)
        warnings = ['Visual review required: identity, motion, edges and keying.']
        if not args.key:
            warnings.append('Opaque source retained; no background removal selected.')
        if any(b[0] == 0 or b[1] == 0 or b[2] == im.width or b[3] == im.height
               for b, im in zip(boxes, frames)):
            warnings.append('Foreground touches source edge; inspect for clipping or background residue.')
        manifest = {'version': 1, 'status': 'needs_review', 'source': str(args.video.resolve()),
                    'source_sha256': digest(args.video), 'source_accepted': True,
                    'start': args.start, 'duration': args.duration, 'fps': args.fps,
                    'size': [width,height], 'anchor': [ax,ay], 'source_union': list(union),
                    'key': args.key, 'tolerance': args.tolerance, 'scale': scale,
                    'frames': [{'file': p.name, 'sha256': digest(p)} for p in sorted(output.glob('*.png'))],
                    'warnings': warnings}
        (out/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    make_output(args.out, run)


def verify(job):
    manifest_path = job / 'manifest.json'
    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    if data.get('version') != 1 or not data.get('frames'):
        raise ValueError('Invalid manifest')
    expected = set()
    for item in data['frames']:
        name = item['file']
        if not re.fullmatch(r'\d{4,}\.png', name) or name in expected:
            raise ValueError('Invalid or duplicate frame filename')
        expected.add(name)
        path = job/'frames'/name
        if not path.is_file() or digest(path) != item['sha256']:
            raise ValueError(f'Frame missing or changed: {name}')
        with Image.open(path) as im:
            if list(im.size) != data['size'] or not im.convert('RGBA').getchannel('A').getbbox():
                raise ValueError(f'Invalid or empty frame: {name}')
    if {p.name for p in (job/'frames').glob('*.png')} != expected:
        raise ValueError('Frame list changed')
    return data


def approve(args):
    if not args.reviewer.strip():
        raise ValueError('Reviewer name is required')
    verify(args.job)
    path = args.job/'approval.json'
    if path.exists():
        raise ValueError('Approval already exists; use a new job for another review')
    approval = {'reviewer': args.reviewer, 'approved_at': datetime.now(timezone.utc).isoformat(),
                'manifest_sha256': digest(args.job/'manifest.json')}
    with path.open('x', encoding='utf-8') as f:
        json.dump(approval, f, indent=2)
    print(f'Approved: {args.job}')


def export(args):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.name):
        raise ValueError('Animation name must contain only letters, numbers, _ or -')
    if not re.fullmatch(r'res://[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*', args.res_path):
        raise ValueError('Specify the intended Godot folder, e.g. res://sprites/attack')
    data = verify(args.job)
    approval = json.loads((args.job/'approval.json').read_text(encoding='utf-8'))
    if approval['manifest_sha256'] != digest(args.job/'manifest.json'):
        raise ValueError('Manifest changed since approval')
    def run(out):
        shutil.copytree(args.job/'frames', out/'frames')
        # The destination must match the path supplied by the user at export time.
        lines = [f'[gd_resource type="SpriteFrames" load_steps={len(data["frames"])+1} format=3]', '']
        for i, frame in enumerate(data['frames']):
            lines.append(f'[ext_resource type="Texture2D" path="{args.res_path}/frames/{frame["file"]}" id="{i+1}"]')
        lines.extend(['', '[resource]', 'animations = [{', '"frames": ['])
        for i in range(len(data['frames'])):
            lines.append('{"duration": 1.0, "texture": ExtResource("%d")},' % (i+1))
        lines.extend(['],', f'"loop": {str(args.loop).lower()},', f'"name": &"{args.name}",',
                      f'"speed": {data["fps"]}', '}]', ''])
        (out/'animation.tres').write_text('\n'.join(lines), encoding='utf-8')
        shutil.copy2(args.job/'manifest.json', out/'manifest.json')
        shutil.copy2(args.job/'approval.json', out/'approval.json')
    make_output(args.out, run)


def positive(value):
    n = float(value)
    if not math.isfinite(n) or n <= 0:
        raise argparse.ArgumentTypeError('must be finite and positive')
    return n


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    for name, func in [('inspect', inspect), ('process', process)]:
        p = subs.add_parser(name)
        p.add_argument('--video', type=Path, required=True)
        p.add_argument('--out', type=Path, required=True)
        p.add_argument('--start', type=float, default=0)
        p.add_argument('--duration', type=positive, required=True)
        p.add_argument('--fps', type=positive, default=8)
        if name == 'process':
            p.add_argument('--size', required=True)
            p.add_argument('--anchor', required=True)
            p.add_argument('--key')
            p.add_argument('--tolerance', type=float, default=60)
            p.add_argument('--source-accepted', action='store_true')
        p.set_defaults(func=func)
    p = subs.add_parser('approve')
    p.add_argument('--job', type=Path, required=True)
    p.add_argument('--reviewer', required=True)
    p.set_defaults(func=approve)
    p = subs.add_parser('export-godot')
    p.add_argument('--job', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--name', required=True)
    p.add_argument('--res-path', required=True, help='destination within Godot project, e.g. res://sprites/attack')
    p.add_argument('--loop', action='store_true')
    p.set_defaults(func=export)
    args = parser.parse_args()
    try:
        if hasattr(args, 'start') and (not math.isfinite(args.start) or args.start < 0):
            raise ValueError('Start must be finite and nonnegative')
        args.func(args)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as e:
        print(f'error: {e}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
