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

export FLET_WEB_PORT="$PORT"
echo "Starting MovieSongDownloader in $ENV_MODE mode on port $PORT"
if [ "$ENV_MODE" = "dev" ]; then
  python MovieSongDownloader/main.py &
  sleep 4
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://127.0.0.1:$PORT"
  elif command -v open >/dev/null 2>&1; then
    open "http://127.0.0.1:$PORT"
  fi
else
  python MovieSongDownloader/main.py --env prod
fi
