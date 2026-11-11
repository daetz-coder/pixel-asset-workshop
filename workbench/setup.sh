#!/bin/sh
set -eu
cd "$(dirname "$0")"
if command -v python3.12 >/dev/null 2>&1; then PY=python3.12
elif command -v python3.11 >/dev/null 2>&1; then PY=python3.11
elif command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; assert sys.version_info >= (3,11)' 2>/dev/null; then PY=python3
else printf '%s\n' 'Python 3.11 or newer is required.'; exit 1; fi
command -v ffmpeg >/dev/null 2>&1 || { printf '%s\n' 'FFmpeg and ffprobe are required.'; exit 1; }
command -v ffprobe >/dev/null 2>&1 || { printf '%s\n' 'ffprobe is required.'; exit 1; }
"$PY" -m venv .venv
.venv/bin/python -m pip install 'pillow>=12.3.0,<13' 'numpy>=2.2.6,<3'
.venv/bin/python -c 'import pathlib,site; pathlib.Path(site.getsitepackages()[0],"sprite_gen_local.pth").write_text(str(pathlib.Path("vendor/sprite-gen").resolve())+"\n")'
.venv/bin/python -m sprite_gen.cli --help >/dev/null
printf '%s\n' 'Setup complete. Run ./workbench/start.sh from the repository root.'
