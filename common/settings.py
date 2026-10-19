"""
Settings loader — load/save JSON settings with defaults merging.

Handles:
- Missing file → creates from defaults
- Missing keys → fills from defaults (forward-compatible)
- Save with indent=2 for readability

Usage:
    from common.settings import load_settings, save_settings

    DEFAULTS = {"interval": 20, "sound": True}
    settings = load_settings("settings.json", DEFAULTS)
    settings["interval"] = 30
    save_settings("settings.json", settings)
"""

import json
import os


MAX_SETTINGS_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def load_settings(path: str, defaults: dict) -> dict:
    """Load settings from JSON file, merging with defaults for missing keys."""
    resolved_path = os.path.abspath(os.path.normpath(path))
    if os.path.islink(resolved_path):
        return dict(defaults)

    if not os.path.exists(resolved_path):
        save_settings(resolved_path, defaults)
        return dict(defaults)

    if not os.path.isfile(resolved_path):
        return dict(defaults)

    try:
        if os.path.getsize(resolved_path) > MAX_SETTINGS_FILE_SIZE:
            return dict(defaults)

        with open(resolved_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return dict(defaults)

    # Merge: add any new default keys not present in saved file
    merged = dict(defaults)
    merged.update(data)
    return merged


def save_settings(path: str, data: dict) -> None:
    """Save settings dict to JSON file."""
    resolved_path = os.path.abspath(os.path.normpath(path))
    if os.path.islink(resolved_path):
        return

    parent_dir = os.path.dirname(resolved_path) or "."
    os.makedirs(parent_dir, exist_ok=True)

    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(resolved_path, flags, 0o600)
        with open(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        with open(resolved_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
