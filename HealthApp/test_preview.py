import sys
sys.path.append(r'c:\Users\NANDHA A\Desktop\UTILITIES\services\health_app')
import health_app
import tkinter as tk

root = tk.Tk()
root.withdraw()
app = health_app.HealthApp()
app.root = root

def test():
    try:
        sw = health_app.SettingsWindow(root, app.settings, lambda x: print("saved", x))
        sw.entries = {}
        # mock entries
        for k in app.settings:
            v = tk.StringVar(value=str(app.settings[k]))
            sw.entries[k] = (v, True if isinstance(app.settings[k], bool) else (True if isinstance(app.settings[k], str) else False))
        
        sw._preview_toast()
        print("SUCCESS")
    except Exception as e:
        print("ERROR:", e)
    root.destroy()

root.after(100, test)
root.mainloop()
