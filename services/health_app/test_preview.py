import sys
import tkinter as tk

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)
from health_app import HealthApp  # noqa: E402
from ui.settings_ui import SettingsWindow  # noqa: E402



def test_preview_window():
    root = tk.Tk()
    root.withdraw()
    try:
        app = HealthApp()
        app.root = root
        sw = SettingsWindow(root, app.settings, lambda x: print("saved", x), app=app)
        sw.show()

        # Test creating SettingsWindow without mainloop blocking
        assert sw is not None
        assert sw.parent is not None

        # Verify triggering desktop previews for each tab to catch any NameErrors/crashes
        sw._show_desktop_preview_for_tab("📅 Schedule") # Should return None gracefully
        sw._show_desktop_preview_for_tab("✨ Toast FX")
        sw._show_desktop_preview_for_tab("💡 Health Toast")
        sw._show_desktop_preview_for_tab("🔆 Brightness Care")
        sw._show_desktop_preview_for_tab("🌙 Night Care")
    finally:
        root.destroy()


if __name__ == "__main__":
    # Interactive manual preview
    root = tk.Tk()
    root.withdraw()
    app = HealthApp()
    app.root = root

    def run_interactive():
        sw = SettingsWindow(root, app.settings, lambda x: print("saved", x))
        sw.entries = {}
        for k in app.settings:
            v = tk.StringVar(value=str(app.settings[k]))
            sw.entries[k] = (
                v,
                True
                if isinstance(app.settings[k], bool)
                else (True if isinstance(app.settings[k], str) else False),
            )
        sw._show_desktop_preview_for_tab("General")
        root.destroy()

    root.after(100, run_interactive)
    root.mainloop()
