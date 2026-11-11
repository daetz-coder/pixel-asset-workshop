#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ] || [ ! -d vendor/sprite-gen/sprite_gen ]; then
  printf '%s\n' 'Run ./workbench/setup.sh from the repository root first.'
  exit 1
fi
exec .venv/bin/python server.py
