#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
export FLET_WEB_PORT="8555"
echo "Building MovieSongDownloader production bundle..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python "$ROOT_DIR/main.py" --env prod
archive="$ROOT_DIR/../logs/MovieSongDownloader-production-$(date +%Y%m%d%H%M%S).zip"
mkdir -p "$ROOT_DIR/../logs"
zip -r "$archive" "$ROOT_DIR"
echo "Packaged production artifact: $archive"
