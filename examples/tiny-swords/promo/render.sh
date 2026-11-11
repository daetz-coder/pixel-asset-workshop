#!/usr/bin/env bash
# Render the workflow walkthrough using the sample footage and exports in the repository.
set -euo pipefail

root="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$root"
mkdir -p work
build="$(mktemp -d "$root/work/promo-render.XXXXXX")"
preview="$root/examples/tiny-swords/preview"
video="assets/video-inputs/blue-units-3x2-wan-prime-480p.mp4"
layout="examples/tiny-swords/wan-layout.json"
python_bin="${PYTHON_BIN:-python3}"
mkdir -p "$build/media" "$build/promo" "$build/preview/exports"

"$python_bin" scripts/extract_frames.py --video "$video" --layout "$layout" --fps 10 --out "$build/before"
"$python_bin" scripts/extract_frames.py --video "$video" --layout "$layout" --fps 10 --despill-magenta --out "$build/clean"

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
PY

cp "$video" "$build/media/source.mp4"
cp "$preview/blue-squad.png" "$build/media/extract.png"
cp "$preview/spriteframe-curate.png" "$build/media/curate.png"
cp "$preview/training-ground.mp4" "$preview/exports/warhammer-sheet.png" "$build/media/"
cp "$preview/exports/manifest.json" "$build/preview/exports/"
cp examples/tiny-swords/promo/showcase.jsx "$build/promo/"

cd "$build"
npm install --no-audit --no-fund --save-exact remotion@4.0.400 @remotion/cli@4.0.400 react@19.1.0 react-dom@19.1.0
browser_args=()
if [[ -n "${REMOTION_CHROME:-}" ]]; then
  browser_args=(--browser-executable="$REMOTION_CHROME")
fi
npx --no-install remotion render promo/showcase.jsx PixelAssetWorkshop workflow-render.mp4 \
  --public-dir=media --codec=h264 --crf=20 --concurrency=4 "${browser_args[@]}"
ffmpeg -v error -i workflow-render.mp4 -map 0:v:0 -c copy -movflags +faststart workflow-promo.mp4
ffmpeg -v error -ss 0.7 -i workflow-promo.mp4 -frames:v 1 workflow-poster.png
"$python_bin" -c "from PIL import Image; Image.open('workflow-poster.png').save('workflow-poster.webp', quality=90)"
cp workflow-promo.mp4 workflow-poster.webp "$preview/"
