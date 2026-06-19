import sys
import os
import pytest

# Ensure Tcl/Tk can find its init.tcl in some Python installs where the
# embedded tcl folder isn't discovered automatically. Use LOCALAPPDATA
# Python install path as a sensible default on Windows.
if "TCL_LIBRARY" not in os.environ or "TK_LIBRARY" not in os.environ:
    base_tcl_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Programs",
        "Python",
        "Python312",
        "tcl"
    )
    if os.path.isdir(base_tcl_dir):
        os.environ["TCL_LIBRARY"] = os.path.join(base_tcl_dir, "tcl8.6")
        os.environ["TK_LIBRARY"] = os.path.join(base_tcl_dir, "tk8.6")

import tkinter as tk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from services.aerohub_core.toast_utils import BaseToast  # noqa: E402


def test():
    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        pytest.skip("Tcl/Tk not available on this system; skipping GUI test")
    settings = {
        "ht_toast_pos": "Right",
        "ht_toast_custom_x": 100,
        "ht_toast_custom_y": 100,
        "ht_toast_width": 280,
        "ht_toast_height": 70,
        "ht_toast_bg_color": "#101625",
        "ht_toast_fg_color": "#e2e8f0",
        "ht_toast_accent_color": "#00f0ff",
        "ht_toast_font_size": 10,
        "ht_toast_font_weight": "normal",
        "ht_toast_font_family": "Segoe UI",
        "ht_toast_emoji": "\u26a1",
        "ht_toast_radius": 18,
        "ht_toast_padding_x": 12,
        "ht_toast_padding_y": 10,
        "ht_toast_anim_style": "Slide",
        "ht_toast_opacity": 0.95,
        "ht_toast_border_width": 1,
        "ht_toast_border_color": "#1e293b",
        "ht_toast_gradient": False,
        "ht_toast_gradient_end": "#101625",
        "ht_toast_shadow": True,
        "ht_toast_accent_stripe": False,
        "ht_toast_text_align": "left",
        "ht_toast_auto_dismiss": True,
        "ht_duration_sec": 2,
        "toast_enable_sound": False,
    }

    # Send multiple toasts
    toast1 = BaseToast(
        root, "Health Tip", "First toast! ⚡", settings, is_health_tip=True
    )
    toast1.show()

    toast2 = BaseToast(
        root, "Health Tip", "Second toast! 💧", settings, is_health_tip=True
    )
    toast2.show()

    root.after(10000, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    test()
