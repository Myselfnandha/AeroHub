"""
DWM rounded corners — applies Windows 11 rounded corners to any window.

Uses DwmSetWindowAttribute with DWMWA_WINDOW_CORNER_PREFERENCE = 33.
Value 2 = DWMWCP_ROUND (rounded corners).
Safely no-ops on Linux / macOS / Windows 10.

Usage:
    from common.dwm import apply_rounded_corners
    apply_rounded_corners(hwnd)  # pass a tkinter or Win32 window handle
"""

import sys


def apply_rounded_corners(hwnd: int) -> None:
    """Apply Windows 11 rounded corners to a window handle."""
    if sys.platform != "win32":
        return

    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWCP_ROUND = 2

    try:
        import ctypes
        dwmapi = ctypes.windll.dwmapi  # type: ignore[attr-defined]
        value = ctypes.c_int(DWMWCP_ROUND)
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(value),
            ctypes.sizeof(value),
        )
    except Exception:
        # Silently fail on Windows 10 or if DWM is unavailable
        pass

