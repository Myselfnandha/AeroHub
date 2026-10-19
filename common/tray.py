"""
Theme detection + tray icon helpers.

Reads Windows registry on Windows, or gsettings / desktop theme on Linux
for dark/light mode and accent colors.
Provides helper to set unique AppUserModelID for tray icon grouping (Windows).

Usage:
    from common.tray import get_theme, set_appusermodelid

    theme = get_theme()
    # theme = {"dark": True, "accent": (0, 120, 212), "accent_hex": "#0078d4"}

    set_appusermodelid("AeroHub.BatteryMonitor")
"""

import os
import subprocess
import sys


def _detect_linux_theme() -> dict:
    """Detect dark/light mode on Linux."""
    dark = True
    accent = (0, 120, 212)  # Default primary blue

    # Try GNOME / Cinnamon / MATE via gsettings
    try:
        res = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True, text=True, timeout=1,
        )
        if res.returncode == 0:
            val = res.stdout.strip().strip("'\"")
            if "prefer-dark" in val or "dark" in val:
                dark = True
            elif "prefer-light" in val or "light" in val:
                dark = False
    except (subprocess.SubprocessError, OSError):
        pass

    # Check GTK theme name
    try:
        res = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
            capture_output=True, text=True, timeout=1,
        )
        if res.returncode == 0:
            theme_name = res.stdout.strip().lower()
            dark = "dark" in theme_name
    except (subprocess.SubprocessError, OSError):
        pass

    # Try detecting accent color from gsettings if available
    try:
        res = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "accent-color"],
            capture_output=True, text=True, timeout=1,
        )
        if res.returncode == 0:
            val = res.stdout.strip().strip("'\"").lower()
            accents = {
                "blue": (53, 132, 228),
                "teal": (33, 144, 164),
                "green": (46, 194, 126),
                "yellow": (229, 165, 10),
                "orange": (230, 97, 0),
                "red": (224, 27, 36),
                "pink": (213, 97, 153),
                "purple": (145, 65, 172),
                "slate": (94, 103, 111),
            }
            if val in accents:
                accent = accents[val]
    except (subprocess.SubprocessError, OSError, KeyError, ValueError):
        pass

    accent_hex = "#{:02x}{:02x}{:02x}".format(*accent)
    return {"dark": dark, "accent": accent, "accent_hex": accent_hex}


def get_theme() -> dict:
    """Detect dark/light mode and accent color across OS platforms."""
    if sys.platform != "win32":
        return _detect_linux_theme()

    dark = True
    accent = (0, 120, 212)  # Default Windows blue

    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        )
        # 0 = dark mode, 1 = light mode
        value, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")
        dark = value == 0
        winreg.CloseKey(key)
    except (OSError, KeyError, ValueError):
        pass

    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\DWM",
        )
        value, _ = winreg.QueryValueEx(key, "AccentColor")
        winreg.CloseKey(key)
        # AccentColor is ABGR format as a 32-bit int
        r = value & 0xFF
        g = (value >> 8) & 0xFF
        b = (value >> 16) & 0xFF
        accent = (r, g, b)
    except (OSError, KeyError, ValueError):
        pass

    accent_hex = "#{:02x}{:02x}{:02x}".format(*accent)
    return {"dark": dark, "accent": accent, "accent_hex": accent_hex}


def set_appusermodelid(app_id: str) -> None:
    """Set unique AppUserModelID so Windows groups tray icons correctly."""
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)  # type: ignore[attr-defined]
        except (AttributeError, OSError):
            pass

