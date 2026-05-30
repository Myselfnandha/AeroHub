import os
import sys
import json
import ctypes
import ctypes.wintypes
import threading
import win32gui
from pynput import mouse
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import ttk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(SCRIPT_DIR, "settings.json")

# AeroHub Theme
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "accent": "#7c3aed",
    "fg": "#f0f0f0",
    "border": "#2d2d5e",
}

try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

class TaskbarScrollApp:
    def __init__(self):
        self.settings = self.load_settings()
        self.mouse_listener = None
        self.icon = None
        self.root = None
        self.settings_window = None

    def load_settings(self):
        if os.path.exists(SETTINGS_PATH):
            try:
                with open(SETTINGS_PATH, 'r', encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"invert_scroll": False, "step_multiplier": 1}

    def save_settings(self):
        with open(SETTINGS_PATH, 'w', encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def create_tray_icon_image(self):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw a simple speaker/scroll icon
        draw.polygon([(16, 24), (16, 40), (26, 40), (40, 52), (40, 12), (26, 24)], fill=TH["accent"])
        draw.arc((30, 20, 50, 44), -45, 45, fill=TH["accent"], width=4)
        draw.arc((20, 10, 60, 54), -45, 45, fill=TH["accent"], width=4)
        return img

    def on_quit(self, icon, item):
        icon.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.root:
            self.root.quit()
        os._exit(0)

    def _apply_dwm_rounding(self, hwnd):
        try:
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                ctypes.sizeof(ctypes.c_int)
            )
        except Exception:
            pass

    def show_settings_window(self, event=None):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Taskbar Scroll Settings")
        self.settings_window.configure(bg=TH["bg"])
        self.settings_window.resizable(False, False)
        
        self.settings_window.geometry(f"320x250")
        try:
            self._apply_dwm_rounding(int(self.settings_window.wm_frame(), 16))
        except Exception:
            pass

        tk.Label(
            self.settings_window, text="🔊 Taskbar Scroll",
            font=("Segoe UI", 16, "bold"), bg=TH["bg"], fg=TH["accent"]
        ).pack(pady=(20, 10))

        frame = tk.Frame(self.settings_window, bg=TH["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Invert Scroll
        inv_var = tk.BooleanVar(value=self.settings.get("invert_scroll", False))
        tk.Checkbutton(
            frame, text="Invert Scroll Direction", variable=inv_var,
            font=("Segoe UI", 10), bg=TH["bg"], fg=TH["fg"],
            selectcolor=TH["bg2"], activebackground=TH["bg"]
        ).pack(anchor=tk.W, pady=10)

        # Step Multiplier
        tk.Label(
            frame, text="Volume Step Multiplier:", font=("Segoe UI", 10),
            bg=TH["bg"], fg=TH["fg"]
        ).pack(anchor=tk.W)

        step_var = tk.StringVar(value=str(self.settings.get("step_multiplier", 1)))
        cbox = ttk.Combobox(
            frame, textvariable=step_var, values=["1", "2", "3", "4", "5"],
            state="readonly", font=("Segoe UI", 10), width=10
        )
        cbox.pack(anchor=tk.W, pady=5)

        def save():
            self.settings["invert_scroll"] = inv_var.get()
            try:
                self.settings["step_multiplier"] = int(step_var.get())
            except Exception:
                pass
            self.save_settings()
            self.settings_window.destroy()

        tk.Button(
            self.settings_window, text="💾 Save", font=("Segoe UI", 10, "bold"),
            bg=TH["accent"], fg="white", relief=tk.FLAT, cursor="hand2",
            command=save, padx=20, pady=5
        ).pack(pady=20)

    def on_scroll(self, x, y, dx, dy):
        try:
            # Ensure perfect coordinate matching regardless of DPI scaling
            try:
                import win32api
                cx, cy = win32api.GetCursorPos()
            except Exception:
                cx, cy = int(x), int(y)
                
            hwnd = win32gui.WindowFromPoint((cx, cy))
            try:
                class_name = win32gui.GetClassName(hwnd)
                root_hwnd = ctypes.windll.user32.GetAncestor(hwnd, 2) # GA_ROOT
                root_class = win32gui.GetClassName(root_hwnd) if root_hwnd else ""
            except Exception:
                class_name = ""
                root_class = ""
            
            valid_classes = ("Shell_TrayWnd", "Shell_SecondaryTrayWnd")
            if class_name in valid_classes or root_class in valid_classes:
                multiplier = int(self.settings.get("step_multiplier", 1))
                invert = bool(self.settings.get("invert_scroll", False))
                
                # dy is positive for scroll up, negative for scroll down
                delta = dy
                if invert:
                    delta = -delta

                VK_VOLUME_UP = 0xAF
                VK_VOLUME_DOWN = 0xAE
                vk_code = VK_VOLUME_UP if delta > 0 else VK_VOLUME_DOWN
                
                for _ in range(multiplier):
                    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
                    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)
                    
        except Exception as e:
            pass

    def open_settings(self, icon, item):
        if hasattr(self, 'ui_queue'):
            self.ui_queue.put("open_settings")

    def _poll_queue(self):
        try:
            while not self.ui_queue.empty():
                cmd = self.ui_queue.get_nowait()
                if cmd == "open_settings":
                    self.show_settings_window()
        except Exception:
            pass
        if self.root:
            self.root.after(100, self._poll_queue)

    def run(self):
        self.ui_queue = __import__('queue').Queue()
        
        self.mouse_listener = mouse.Listener(on_scroll=self.on_scroll)
        self.mouse_listener.start()

        menu = pystray.Menu(
            pystray.MenuItem("Settings", self.open_settings, default=True),
            pystray.MenuItem("Quit", self.on_quit)
        )
        self.icon = pystray.Icon("TaskbarScroll", self.create_tray_icon_image(), "Taskbar Scroll", menu)
        
        icon_thread = threading.Thread(target=self.icon.run, daemon=True)
        icon_thread.start()

        self.root = tk.Tk()
        self.root.withdraw()
        self.root.after(100, self._poll_queue)
        self.root.mainloop()

if __name__ == "__main__":
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "TaskbarScrollApp_Mutex")
    if ctypes.windll.kernel32.GetLastError() == 183:
        sys.exit(0)
    
    app = TaskbarScrollApp()
    app.run()
