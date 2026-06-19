#!/usr/bin/env bash
set -euo pipefail
ENV_MODE="dev"
PORT="8555"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)
      ENV_MODE="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1"
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
export FLET_WEB_PORT="$PORT"
echo "Starting movie_song_downloader in $ENV_MODE mode on port $PORT"
MAIN_SCRIPT="$REPO_ROOT/services/movie_song_downloader/main.py"
if [ "$ENV_MODE" = "dev" ]; then
  python "$MAIN_SCRIPT" &
  sleep 4
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://127.0.0.1:$PORT"
  elif command -v open >/dev/null 2>&1; then
    open "http://127.0.0.1:$PORT"
  fi
else
  python "$MAIN_SCRIPT" --env prod
fi
