#!/usr/bin/env bash
# Render the generated-character showcase using the checked-in Wan sample.
set -euo pipefail

root="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$root"
mkdir -p work
build="$(mktemp -d "$root/work/promo-render.XXXXXX")"
preview="$root/examples/tiny-swords/preview"
video="assets/video-inputs/blue-units-3x2-wan-prime-480p.mp4"
layout="examples/tiny-swords/wan-layout.json"
python_bin="${PYTHON_BIN:-python3}"
godot_bin="${GODOT_BIN:-godot}"
mkdir -p "$build/media"

"$python_bin" scripts/extract_frames.py --video "$video" --layout "$layout" --fps 10 --out "$build/before"
"$python_bin" scripts/extract_frames.py --video "$video" --layout "$layout" --fps 10 --despill-magenta --out "$build/clean"
"$godot_bin" --path examples/tiny-swords/godot --write-movie "$build/godot.avi" \
  --fixed-fps 10 --disable-vsync --quit-after 50 -- --frames="$build/clean"

ffmpeg -v error -i "$build/godot.avi" -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart -an "$build/media/godot.mp4"
ffmpeg -v error -ss 1 -i "$video" -t 4 -c:v libx264 -crf 24 -pix_fmt yuv420p -an "$build/media/source.mp4"
ffmpeg -v error -ss 1.4 -i "$build/godot.avi" -frames:v 1 "$build/godot-still.png"
ffmpeg -v error -i "$build/godot.avi" -t 4 \
  -vf 'crop=816:188:32:110,scale=720:-1:flags=neighbor,split[a][b];[a]palettegen=max_colors=100[p];[b][p]paletteuse=dither=none:diff_mode=rectangle' \
  "$build/godot-playback.gif"

"$python_bin" - "$build" <<'PY'
from pathlib import Path
import sys
from PIL import Image

build = Path(sys.argv[1])
with Image.open(build / 'before/r01c01/attack/0014.png') as before:
    x0, y0, x1, y1 = before.getchannel('A').getbbox()
    bounds = (x0 - 5, y0 - 5, x1 + 5, y1 + 5)
    before.crop(bounds).save(build / 'media/before.png')
with Image.open(build / 'clean/r01c01/attack/0014.png') as clean:
    clean.crop(bounds).save(build / 'media/clean.png')
with Image.open(build / 'godot-still.png') as still:
    still.save(build / 'godot-clean.webp', quality=90)
PY

cp examples/tiny-swords/promo/showcase.jsx "$build/showcase.jsx"
cd "$build"
npm install --no-audit --no-fund --save-exact remotion@4.0.400 @remotion/cli@4.0.400 react@19.1.0 react-dom@19.1.0
browser_args=()
if [[ -n "${REMOTION_CHROME:-}" ]]; then
  browser_args=(--browser-executable="$REMOTION_CHROME")
fi
npx --no-install remotion render showcase.jsx PixelAssetWorkshop workflow-render.mp4 \
  --public-dir=media --codec=h264 --crf=22 --concurrency=4 "${browser_args[@]}"
ffmpeg -v error -i workflow-render.mp4 -map 0:v:0 -c copy -movflags +faststart workflow-promo.mp4
ffmpeg -v error -ss 0.7 -i workflow-promo.mp4 -frames:v 1 workflow-poster.png
"$python_bin" -c "from PIL import Image; Image.open('workflow-poster.png').save('workflow-poster.webp', quality=90)"
cp workflow-promo.mp4 workflow-poster.webp godot-clean.webp godot-playback.gif "$preview/"
cp media/godot.mp4 "$preview/godot-playback.mp4"
