#!/usr/bin/env bash
# Build a local-only comparison with the user's own Tiny Swords Free Pack.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
pack="${1:-"$root/assets/references/tiny-swords/Tiny Swords (Free Pack)"}"
out="${2:-"$root/work/tiny-swords/comparison"}"
python_bin="${PYTHON_BIN:-python3}"
script="$root/skills/reference-game-characters/scripts/sprite_reference.py"
archer="$pack/Units/Blue Units/Archer/Archer_Idle.png"

if [[ ! -f "$archer" ]]; then
  echo "Download Tiny Swords Free Pack from https://pixelfrog-assets.itch.io/tiny-swords and pass the extracted pack root." >&2
  exit 1
fi
if [[ -e "$out" ]]; then
  echo "Choose a new output directory: $out" >&2
  exit 1
fi

"$python_bin" "$script" extract "$archer" --frame-size 192 192 --index 0 --scale 4 \
  --out "$out/archer-idle-x4.png"
"$python_bin" "$script" compare "$out/archer-idle-x4.png" "$root/assets/concepts/warhammer-infantry.png" \
  --reference-body-box 292 248 168 268 --candidate-body-box 326 391 464 604 \
  --body-height 67 --zoom 4 --out "$out/archer-vs-warhammer.png"
