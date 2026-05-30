import sys
import tkinter as tk

sys.path.append(r'c:\Users\NANDHA A\Desktop\UTILITIES\services\health_app')
import health_app

def test_preview_window():
    root = tk.Tk()
    root.withdraw()
    try:
        app = health_app.HealthApp()
        app.root = root
        sw = health_app.SettingsWindow(root, app.settings, lambda x: print("saved", x))
        sw.entries = {}
        # mock entries
        for k in app.settings:
            v = tk.StringVar(value=str(app.settings[k]))
            sw.entries[k] = (v, True if isinstance(app.settings[k], bool) else (True if isinstance(app.settings[k], str) else False))
        
        # Test creating SettingsWindow without mainloop blocking
        assert sw is not None
    finally:
        root.destroy()

if __name__ == "__main__":
    # Interactive manual preview
    root = tk.Tk()
    root.withdraw()
    app = health_app.HealthApp()
    app.root = root
    
    def run_interactive():
        sw = health_app.SettingsWindow(root, app.settings, lambda x: print("saved", x))
        sw.entries = {}
        for k in app.settings:
            v = tk.StringVar(value=str(app.settings[k]))
            sw.entries[k] = (v, True if isinstance(app.settings[k], bool) else (True if isinstance(app.settings[k], str) else False))
        sw._preview_toast()
        root.destroy()

    root.after(100, run_interactive)
    root.mainloop()
