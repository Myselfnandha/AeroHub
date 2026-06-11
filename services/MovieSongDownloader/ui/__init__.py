# UI Module
import os


def resolve_image_src(
    cached_path: str | None, remote_url: str | None, fallback: str = ""
) -> str:
    """Resolve the best image source for display.

    In web mode (FLET_WEB_PORT set), file:// URIs are blocked by browsers.
    Always prefer remote HTTP URLs. Only use local paths in desktop mode.
    """
    is_web_mode = bool(os.environ.get("FLET_WEB_PORT"))

    if is_web_mode:
        # Web mode: remote URL always wins, local paths won't render
        if remote_url:
            return remote_url
        return fallback

    # Desktop mode: prefer cached local file for speed
    if cached_path and os.path.exists(cached_path):
        from pathlib import Path

        return Path(cached_path).as_uri()

    if remote_url:
        return remote_url

    return fallback
