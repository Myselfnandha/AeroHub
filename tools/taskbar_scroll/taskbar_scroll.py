# ruff: noqa: E402
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

# Ensure workspace root is in sys.path to import services.aerohub_core.system_utils as system_utils
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)
import services.aerohub_core.system_utils as system_utils

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
        self.tp_window = None
        self.tp_hwnd = None
        self.is_clicking = False
        self.simulated_click_active = False
        self.clicked_button = None

    def load_settings(self):
        defaults = {
            "invert_scroll": False,
            "step_multiplier": 1,
            "enable_brightness_control": True,
            "brightness_step": 5,
            "enable_touchpad_support": True
        }
        if os.path.exists(SETTINGS_PATH):
            try:
                with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    defaults.update(data)
                    return defaults
            except Exception:
                pass
        return defaults

    def save_settings(self):
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def create_tray_icon_image(self):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw a simple speaker/scroll icon
        draw.polygon(
            [(16, 24), (16, 40), (26, 40), (40, 52), (40, 12), (26, 24)],
            fill=TH["accent"],
        )
        draw.arc((30, 20, 50, 44), -45, 45, fill=TH["accent"], width=4)
        draw.arc((20, 10, 60, 54), -45, 45, fill=TH["accent"], width=4)
        return img

    def on_quit(self, icon, item):
        icon.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.tp_window:
            try:
                self.tp_window.destroy()
            except Exception:
                pass
        if self.root:
            self.root.quit()
        os._exit(0)

    def _apply_dwm_rounding(self, hwnd):
        try:
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                ctypes.sizeof(ctypes.c_int),
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

        self.settings_window.geometry("350x420")
        try:
            self._apply_dwm_rounding(int(self.settings_window.wm_frame(), 16))
        except Exception:
            pass

        tk.Label(
            self.settings_window,
            text="🔊 Taskbar Scroll",
            font=("Segoe UI", 16, "bold"),
            bg=TH["bg"],
            fg=TH["accent"],
        ).pack(pady=(15, 5))

        frame = tk.Frame(self.settings_window, bg=TH["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Invert Scroll
        inv_var = tk.BooleanVar(value=self.settings.get("invert_scroll", False))
        tk.Checkbutton(
            frame,
            text="Invert Scroll Direction",
            variable=inv_var,
            font=("Segoe UI", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
            activeforeground=TH["fg"],
        ).pack(anchor=tk.W, pady=4)

        # Volume Step Multiplier
        tk.Label(
            frame,
            text="Volume Step Multiplier:",
            font=("Segoe UI", 10),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(4, 0))

        step_var = tk.StringVar(value=str(self.settings.get("step_multiplier", 1)))
        cbox = ttk.Combobox(
            frame,
            textvariable=step_var,
            values=["1", "2", "3", "4", "5"],
            state="readonly",
            font=("Segoe UI", 10),
            width=10,
        )
        cbox.pack(anchor=tk.W, pady=2)

        # Enable Brightness Control
        bright_var = tk.BooleanVar(value=self.settings.get("enable_brightness_control", True))
        tk.Checkbutton(
            frame,
            text="Enable Brightness Control (Ctrl + Scroll)",
            variable=bright_var,
            font=("Segoe UI", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
            activeforeground=TH["fg"],
        ).pack(anchor=tk.W, pady=4)

        # Brightness Step Size
        tk.Label(
            frame,
            text="Brightness Step Size (%):",
            font=("Segoe UI", 10),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(4, 0))

        b_step_var = tk.StringVar(value=str(self.settings.get("brightness_step", 5)))
        b_cbox = ttk.Combobox(
            frame,
            textvariable=b_step_var,
            values=["1", "2", "5", "10", "15", "20"],
            state="readonly",
            font=("Segoe UI", 10),
            width=10,
        )
        b_cbox.pack(anchor=tk.W, pady=2)

        # Enable Touchpad Support
        tp_var = tk.BooleanVar(value=self.settings.get("enable_touchpad_support", True))
        tk.Checkbutton(
            frame,
            text="Enable Touchpad Scroll Support",
            variable=tp_var,
            font=("Segoe UI", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
            activeforeground=TH["fg"],
        ).pack(anchor=tk.W, pady=4)

        def save():
            self.settings["invert_scroll"] = inv_var.get()
            self.settings["enable_brightness_control"] = bright_var.get()
            self.settings["enable_touchpad_support"] = tp_var.get()
            try:
                self.settings["step_multiplier"] = int(step_var.get())
            except Exception:
                pass
            try:
                self.settings["brightness_step"] = int(b_step_var.get())
            except Exception:
                pass
            self.save_settings()
            self.settings_window.destroy()

        tk.Button(
            self.settings_window,
            text="💾 Save",
            font=("Segoe UI", 10, "bold"),
            bg=TH["accent"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=save,
            padx=20,
            pady=5,
        ).pack(pady=15)

    def adjust_brightness(self, amount):
        try:
            import screen_brightness_control as sbc
            current = sbc.get_brightness()
            if isinstance(current, list):
                for idx, val in enumerate(current):
                    new_val = max(0, min(100, val + amount))
                    sbc.set_brightness(new_val, display=idx)
            else:
                new_val = max(0, min(100, current + amount))
                sbc.set_brightness(new_val)
        except Exception:
            try:
                import screen_brightness_control as sbc
                sbc.set_brightness(max(0, min(100, 50 + amount)))
            except Exception:
                pass

    def handle_scroll_action(self, dy):
        try:
            multiplier = int(self.settings.get("step_multiplier", 1))
            invert = bool(self.settings.get("invert_scroll", False))

            delta = dy
            if invert:
                delta = -delta

            # Check if Ctrl is held (VK_CONTROL = 0x11)
            is_ctrl = bool(ctypes.windll.user32.GetAsyncKeyState(0x11) & 0x8000)
            enable_brightness = bool(self.settings.get("enable_brightness_control", True))

            if is_ctrl and enable_brightness:
                step = int(self.settings.get("brightness_step", 5))
                amount = step * multiplier if delta > 0 else -step * multiplier
                self.adjust_brightness(amount)
            else:
                VK_VOLUME_UP = 0xAF
                VK_VOLUME_DOWN = 0xAE
                vk_code = VK_VOLUME_UP if delta > 0 else VK_VOLUME_DOWN

                for _ in range(multiplier):
                    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
                    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)
        except Exception:
            pass

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
                root_hwnd = ctypes.windll.user32.GetAncestor(hwnd, 2)  # GA_ROOT
                root_class = win32gui.GetClassName(root_hwnd) if root_hwnd else ""
            except Exception:
                class_name = ""
                root_class = ""

            valid_classes = ("Shell_TrayWnd", "Shell_SecondaryTrayWnd")
            if class_name in valid_classes or root_class in valid_classes:
                self.handle_scroll_action(dy)
        except Exception:
            pass

    def get_taskbar_rects(self):
        rects = []
        # Primary taskbar
        hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
        if hwnd:
            try:
                rect = win32gui.GetWindowRect(hwnd)
                rects.append(rect)
            except Exception:
                pass
        # Secondary taskbars
        hwnd = None
        while True:
            try:
                hwnd = win32gui.FindWindowEx(None, hwnd, "Shell_SecondaryTrayWnd", None)
                if not hwnd:
                    break
                rect = win32gui.GetWindowRect(hwnd)
                rects.append(rect)
            except Exception:
                break
        return rects

    def init_tp_window(self):
        self.tp_window = tk.Toplevel(self.root)
        self.tp_window.overrideredirect(True)
        self.tp_window.attributes("-toolwindow", True)
        self.tp_window.attributes("-topmost", True)
        self.tp_window.attributes("-alpha", 0.002)
        self.tp_window.configure(bg="black")
        
        self.tp_window.update_idletasks()
        self.tp_hwnd = self.tp_window.winfo_id()
        
        try:
            style = win32gui.GetWindowLong(self.tp_hwnd, -20)  # GWL_EXSTYLE = -20
            # WS_EX_NOACTIVATE = 0x08000000, WS_EX_TOOLWINDOW = 0x00000080
            style |= 0x08000000 | 0x00000080
            win32gui.SetWindowLong(self.tp_hwnd, -20, style)
        except Exception:
            pass
            
        self.tp_window.bind("<MouseWheel>", self.on_tp_scroll)
        self.tp_window.bind("<ButtonPress-1>", lambda e: self.on_tp_click(1))
        self.tp_window.bind("<ButtonPress-2>", lambda e: self.on_tp_click(2))
        self.tp_window.bind("<ButtonPress-3>", lambda e: self.on_tp_click(3))
        self.tp_window.withdraw()

    def on_tp_scroll(self, event):
        dy = 1 if event.delta > 0 else -1
        self.handle_scroll_action(dy)

    def on_tp_click(self, button_num):
        if hasattr(self, "tp_hwnd") and self.tp_hwnd:
            self.is_clicking = True
            self.simulated_click_active = True
            self.clicked_button = button_num
            ctypes.windll.user32.ShowWindow(self.tp_hwnd, 0)  # SW_HIDE
            try:
                self.tp_window.update()
            except Exception:
                pass
            
            # Map button number to mouse_event flags
            # Left down: 0x0002, Middle down: 0x0020, Right down: 0x0008
            flags = 0
            if button_num == 1:
                flags = 0x0002
            elif button_num == 2:
                flags = 0x0020
            elif button_num == 3:
                flags = 0x0008
                
            if flags:
                ctypes.windll.user32.mouse_event(flags, 0, 0, 0, 0)

    def on_global_click(self, x, y, button, pressed):
        if hasattr(self, "tp_hwnd") and self.tp_hwnd:
            if pressed:
                self.is_clicking = True
                ctypes.windll.user32.ShowWindow(self.tp_hwnd, 0)  # SW_HIDE (0)
            else:
                if getattr(self, "simulated_click_active", False):
                    # Simulate mouse-up event matching self.clicked_button
                    # Left up: 0x0004, Middle up: 0x0040, Right up: 0x0010
                    up_flags = 0
                    btn_num = getattr(self, "clicked_button", None)
                    if btn_num == 1:
                        up_flags = 0x0004
                    elif btn_num == 2:
                        up_flags = 0x0040
                    elif btn_num == 3:
                        up_flags = 0x0010
                    
                    if up_flags:
                        ctypes.windll.user32.mouse_event(up_flags, 0, 0, 0, 0)
                    self.simulated_click_active = False
                    self.clicked_button = None
                
                self.is_clicking = False
                if hasattr(self, "ui_queue"):
                    self.ui_queue.put("update_touchpad")

    def update_touchpad_windows(self):
        try:
            enable_tp = bool(self.settings.get("enable_touchpad_support", True))
            if not enable_tp:
                if hasattr(self, "tp_hwnd") and self.tp_hwnd:
                    ctypes.windll.user32.ShowWindow(self.tp_hwnd, 0)  # SW_HIDE
                self.root.after(100, self.update_touchpad_windows)
                return

            if not self.tp_window:
                self.init_tp_window()

            # Get cursor pos
            import win32api
            cx, cy = win32api.GetCursorPos()

            # Check if mouse is over any taskbar
            is_over = False
            active_rect = None
            for rect in self.get_taskbar_rects():
                left, top, right, bottom = rect
                if left <= cx <= right and top <= cy <= bottom:
                    is_over = True
                    active_rect = rect
                    break

            if is_over and not self.is_clicking:
                left, top, right, bottom = active_rect
                w = right - left
                h = bottom - top
                self.tp_window.geometry(f"{w}x{h}+{left}+{top}")
                # SW_SHOWNOACTIVATE = 4 (shows window without activating it)
                ctypes.windll.user32.ShowWindow(self.tp_hwnd, 4)
                self.tp_window.attributes("-topmost", True)
            else:
                if hasattr(self, "tp_hwnd") and self.tp_hwnd:
                    ctypes.windll.user32.ShowWindow(self.tp_hwnd, 0)  # SW_HIDE

        except Exception:
            pass
        self.root.after(100, self.update_touchpad_windows)

    def open_settings(self, icon, item):
        if hasattr(self, "ui_queue"):
            self.ui_queue.put("open_settings")

    def _poll_queue(self):
        try:
            while not self.ui_queue.empty():
                cmd = self.ui_queue.get_nowait()
                if cmd == "open_settings":
                    self.show_settings_window()
                elif cmd == "update_touchpad":
                    self.update_touchpad_windows()
        except Exception:
            pass
        if self.root:
            self.root.after(100, self._poll_queue)

    def run(self):
        self.ui_queue = __import__("queue").Queue()

        self.mouse_listener = mouse.Listener(on_scroll=self.on_scroll, on_click=self.on_global_click)
        self.mouse_listener.start()

        # Start parent process monitoring
        system_utils.monitor_parent_process(lambda: self.on_quit(self.icon, None))

        menu = pystray.Menu(
            pystray.MenuItem("Settings", self.open_settings, default=True),
            pystray.MenuItem("Quit", self.on_quit),
        )
        self.icon = pystray.Icon(
            "TaskbarScroll", self.create_tray_icon_image(), "Taskbar Scroll", menu
        )

        icon_thread = threading.Thread(target=self.icon.run, daemon=True)
        icon_thread.start()

        self.root = tk.Tk()
        self.root.withdraw()
        self.root.after(100, self._poll_queue)
        self.root.after(100, self.update_touchpad_windows)
        self.root.mainloop()


if __name__ == "__main__":
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "TaskbarScrollApp_Mutex")
    if ctypes.windll.kernel32.GetLastError() == 183:
        sys.exit(0)

    app = TaskbarScrollApp()
    app.run()
