"""
Battery Monitor — macOS-style charging notifications for Windows.
Shows animated toast on plug/unplug, plays sound effects,
and alerts at 33% (low) and 93% (full) thresholds.
"""

import os
import sys
import time
import threading
import logging
import logging.handlers
import winsound
import json
import queue

import psutil
import winreg

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print("Missing deps. Run: pip install pystray Pillow psutil")
    sys.exit(1)

import tkinter as tk
from tkinter import ttk

# AeroHub Theme for Settings
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "accent": "#7c3aed",
    "fg": "#f0f0f0",
    "border": "#2d2d5e",
}

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = r"c:\Users\NANDHA A\Desktop\UTILITIES\Logs"
LOG_PATH = os.path.join(LOGS_DIR, "battery_monitor.log")
os.makedirs(LOGS_DIR, exist_ok=True)
PLUG_SOUND = os.path.join(SCRIPT_DIR, "sounds", "mac_connect.wav")
UNPLUG_SOUND = os.path.join(SCRIPT_DIR, "sounds", "mac_disconnect.wav")

os.makedirs(SCRIPT_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes as _ctypes
    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.BatteryMonitor")
except Exception:
    pass

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("BatteryMonitor")

# ── Colors ──
C = {
    "bg": "#0d1117",
    "bg_toast": "#252525",
    "icon_bg_green": "#28c840",
    "icon_bg_orange": "#fe9f0b",
    "icon_bg_red": "#ff3b30",
    "text": "#ffffff",
    "text_dim": "#a0a0a0",
    "border": "#3a3a3a",
    "close_btn_hover": "#4a4a4a",
}

# ══════════════════════════════════════════════════════════
#  Sound Generation
# ══════════════════════════════════════════════════════════
def verify_sounds():
    """Verify that plug/unplug WAV sound files exist in the sounds directory."""
    if not os.path.exists(PLUG_SOUND):
        logger.error(f"Plug sound file not found: {PLUG_SOUND}")
    if not os.path.exists(UNPLUG_SOUND):
        logger.error(f"Unplug sound file not found: {UNPLUG_SOUND}")


def play_sound(filepath, settings):
    """Play a WAV file asynchronously if sounds are enabled."""
    if not settings.get("enable_sounds", True):
        return
    try:
        winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        logger.error(f"Sound playback error: {e}")


# ══════════════════════════════════════════════════════════
#  Toast Notification (macOS-style animated slide-in)
# ══════════════════════════════════════════════════════════
class ToastNotification:
    """Animated slide-in toast notification replicating macOS style."""

    _active_toasts = []
    _lock = threading.Lock()

    def __init__(self, title: str, message: str, icon_bg: str, icon_char: str = "⚡", duration_ms: int = 4000):
        self.title = title
        self.message = message
        self.icon_bg = icon_bg
        self.icon_char = icon_char
        self.duration = duration_ms

    def show(self):
        threading.Thread(target=self._create_toast, daemon=True).start()

    def _create_toast(self):
        try:
            root = tk.Tk()
            root.withdraw()
            
            toast = tk.Toplevel(root)
            toast.overrideredirect(True)
            toast.attributes("-topmost", True)
            toast.attributes("-alpha", 0.0)
            
            # Transparent color trick for flawless rounded corners
            toast.config(bg="#000001", borderwidth=0, highlightthickness=0, relief="flat")
            toast.attributes("-transparentcolor", "#000001")

            # macOS notification dimensions
            toast_w, toast_h = 340, 74
            screen_w = toast.winfo_screenwidth()
            final_x = screen_w - toast_w - 20
            start_x = screen_w + 10
            
            with ToastNotification._lock:
                # Calculate Y position based on active toasts
                y_pos = 40 + len(ToastNotification._active_toasts) * (toast_h + 8)
                ToastNotification._active_toasts.append(self)
                self.toast_window = toast

            toast.geometry(f"{toast_w}x{toast_h}+{start_x}+{y_pos}")

            canvas = tk.Canvas(toast, width=toast_w, height=toast_h, bg="#000001", highlightthickness=0, borderwidth=0)
            canvas.pack(fill=tk.BOTH, expand=True)

            def create_round_rect(x1, y1, x2, y2, radius=16, **kwargs):
                points = [
                    x1+radius, y1,   x1+radius, y1,   x2-radius, y1,   x2-radius, y1,
                    x2, y1,          x2, y1+radius,   x2, y1+radius,   x2, y2-radius,
                    x2, y2-radius,   x2, y2,          x2-radius, y2,   x2-radius, y2,
                    x1+radius, y2,   x1+radius, y2,   x1, y2,          x1, y2-radius,
                    x1, y2-radius,   x1, y1+radius,   x1, y1+radius,   x1, y1
                ]
                return canvas.create_polygon(points, **kwargs, smooth=True)

            # Draw background and border
            create_round_rect(1, 1, toast_w-1, toast_h-1, radius=16, fill=C["bg_toast"], outline=C["border"], width=1)

            # Draw Icon Background (Rounded Square)
            icon_x, icon_y = 16, 17
            icon_size = 40
            create_round_rect(icon_x, icon_y, icon_x+icon_size, icon_y+icon_size, radius=10, fill=self.icon_bg, outline="")
            
            # Draw Icon Emoji
            canvas.create_text(icon_x + icon_size/2, icon_y + icon_size/2, text=self.icon_char, font=("Segoe UI Emoji", 18), fill="#ffffff", anchor="center")

            # Draw Title and Message
            text_x = 72
            canvas.create_text(text_x, 28, text=self.title, font=("Segoe UI", 10, "bold"), fill=C["text"], anchor="w")
            canvas.create_text(text_x, 48, text=self.message, font=("Segoe UI", 9), fill=C["text_dim"], anchor="w")

            # Close Button (Hidden by default, shown on hover)
            close_size = 20
            close_x, close_y = 16, 17 # Top left of the icon
            
            # Group for close button elements
            close_bg = create_round_rect(close_x, close_y, close_x+close_size, close_y+close_size, radius=10, fill=C["close_btn_hover"], outline="", state="hidden")
            close_text = canvas.create_text(close_x + close_size/2, close_y + close_size/2 - 1, text="✕", font=("Segoe UI", 10, "bold"), fill=C["text"], anchor="center", state="hidden")
            
            self.hovering = False
            self.closing = False

            def on_enter(e):
                self.hovering = True
                canvas.itemconfig(close_bg, state="normal")
                canvas.itemconfig(close_text, state="normal")

            def on_leave(e):
                self.hovering = False
                canvas.itemconfig(close_bg, state="hidden")
                canvas.itemconfig(close_text, state="hidden")

            def on_close_click(e):
                if close_x <= e.x <= close_x+close_size and close_y <= e.y <= close_y+close_size:
                    self.closing = True
                    fade_out(0)

            toast.bind("<Enter>", on_enter)
            toast.bind("<Leave>", on_leave)
            canvas.bind("<Button-1>", on_close_click)

            # ── Slide-in animation ──
            def slide_in(step=0):
                if self.closing:
                    return
                total_steps = 24
                if step <= total_steps:
                    progress = step / total_steps
                    ease = 1 - (1 - progress) ** 3 # ease-out cubic
                    current_x = int(start_x + (final_x - start_x) * ease)
                    alpha = min(0.98, ease)
                    try:
                        toast.geometry(f"{toast_w}x{toast_h}+{current_x}+{y_pos}")
                        toast.attributes("-alpha", alpha)
                        toast.after(16, lambda: slide_in(step + 1))
                    except tk.TclError:
                        pass
                else:
                    toast.after(100, check_hold)

            hold_time = 0
            def check_hold():
                nonlocal hold_time
                if self.closing:
                    return
                
                if not self.hovering:
                    hold_time += 100
                    
                if hold_time >= self.duration:
                    fade_out(0)
                else:
                    toast.after(100, check_hold)

            def fade_out(step=0):
                self.closing = True
                total_steps = 18
                if step <= total_steps:
                    progress = step / total_steps
                    alpha = 0.98 * (1 - progress)
                    try:
                        toast.attributes("-alpha", max(0, alpha))
                        toast.after(16, lambda: fade_out(step + 1))
                    except tk.TclError:
                        pass
                else:
                    cleanup()

            def cleanup():
                try:
                    with ToastNotification._lock:
                        if self in ToastNotification._active_toasts:
                            ToastNotification._active_toasts.remove(self)
                        # Reposition remaining toasts
                        for i, t in enumerate(ToastNotification._active_toasts):
                            try:
                                new_y = 40 + i * (toast_h + 8)
                                # Safely delegate the resize command to the owning thread's event loop
                                t.toast_window.after(0, lambda win=t.toast_window, y=new_y: win.geometry(f"+{final_x}+{y}"))
                            except Exception:
                                pass
                    toast.destroy()
                    root.destroy()
                except Exception:
                    pass

            toast.deiconify()
            slide_in(0)
            root.mainloop()

        except Exception as e:
            logger.error(f"Toast error: {e}")
            try:
                with ToastNotification._lock:
                    if self in ToastNotification._active_toasts:
                        ToastNotification._active_toasts.remove(self)
            except Exception:
                pass


# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════

def get_system_theme() -> str:
    """Return 'light' or 'dark' based on Windows registry."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        val, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")
        winreg.CloseKey(key)
        return "light" if val == 1 else "dark"
    except Exception:
        return "dark"  # Default if registry key is missing

def create_battery_icon(percent: int, plugged: bool, low: bool = False, theme: str = "dark") -> Image.Image:
    """Draw a battery-shaped tray icon with fill level and theme-aware colors."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Theme-aware colors
    if theme == "light":
        border_color = (60, 60, 60, 255)
        bolt_color = (200, 150, 0, 255) # Darker yellow/orange for contrast
        empty_fill = (200, 200, 200, 230)
    else:
        border_color = (200, 200, 200, 200)
        bolt_color = (255, 220, 0, 220)
        empty_fill = (220, 220, 220, 230)

    # Battery body (scaled to absolute maximum size within canvas)
    bx1, by1, bx2, by2 = 1, 13, 57, 51
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=4, outline=border_color, width=2)

    # Battery tip (positive terminal)
    draw.rounded_rectangle([57, 24, 63, 40], radius=2, fill=border_color)

    # Fill level
    fill_width = int((bx2 - bx1 - 6) * percent / 100)
    if fill_width > 0:
        if low:
            fill_color = (255, 51, 102, 230)  # red
        elif plugged:
            fill_color = (0, 255, 136, 230)  # green
        else:
            fill_color = empty_fill
        draw.rounded_rectangle(
            [bx1 + 3, by1 + 3, bx1 + 3 + fill_width, by2 - 3],
            radius=2, fill=fill_color
        )

    # Charging bolt icon
    if plugged:
        bolt = [(34, 15), (22, 34), (29, 34), (25, 49), (36, 30), (29, 30), (34, 15)]
        draw.polygon(bolt, fill=bolt_color)

    return img


# ══════════════════════════════════════════════════════════
#  Main Monitor
# ══════════════════════════════════════════════════════════
class BatteryMonitorApp:
    def __init__(self):
        self.settings_path = os.path.join(SCRIPT_DIR, "settings.json")
        self.settings = self.load_settings()
        self.ui_queue = queue.Queue()
        self.root = None
        self.settings_window = None

        self.prev_percent = None
        self.prev_plugged = None
        self.prev_low = None
        self.prev_theme = None
        self.last_icon_update = 0

        self.low_notified = False    # fired when unplugged < threshold
        self.full_notified = False   # fired when plugged > threshold
        self.tray_icon = None
        self._running = True

    def load_settings(self):
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, 'r', encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"enable_sounds": True, "low_threshold": 20, "full_threshold": 93}

    def save_settings(self):
        with open(self.settings_path, 'w', encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def _apply_dwm_rounding(self, hwnd):
        try:
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2
            import ctypes
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                ctypes.sizeof(ctypes.c_int)
            )
        except Exception:
            pass

    def show_settings_window(self):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Battery Monitor Settings")
        self.settings_window.configure(bg=TH["bg"])
        self.settings_window.resizable(False, False)
        
        self.settings_window.geometry("320x300")
        try:
            self._apply_dwm_rounding(int(self.settings_window.wm_frame(), 16))
        except Exception:
            pass

        tk.Label(
            self.settings_window, text="🔋 Battery Monitor",
            font=("Segoe UI", 16, "bold"), bg=TH["bg"], fg=TH["accent"]
        ).pack(pady=(20, 10))

        frame = tk.Frame(self.settings_window, bg=TH["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Sounds Toggle
        snd_var = tk.BooleanVar(value=self.settings.get("enable_sounds", True))
        tk.Checkbutton(
            frame, text="Enable Plug/Unplug Sounds", variable=snd_var,
            font=("Segoe UI", 10), bg=TH["bg"], fg=TH["fg"],
            selectcolor=TH["bg2"], activebackground=TH["bg"]
        ).pack(anchor=tk.W, pady=10)

        # Low Threshold
        tk.Label(
            frame, text="Low Battery Warning (%):", font=("Segoe UI", 10),
            bg=TH["bg"], fg=TH["fg"]
        ).pack(anchor=tk.W)
        low_var = tk.StringVar(value=str(self.settings.get("low_threshold", 20)))
        ttk.Combobox(
            frame, textvariable=low_var, values=["10", "15", "20", "25", "30", "35"],
            state="readonly", font=("Segoe UI", 10), width=10
        ).pack(anchor=tk.W, pady=5)

        # Full Threshold
        tk.Label(
            frame, text="Full Battery Alert (%):", font=("Segoe UI", 10),
            bg=TH["bg"], fg=TH["fg"]
        ).pack(anchor=tk.W, pady=(5,0))
        full_var = tk.StringVar(value=str(self.settings.get("full_threshold", 93)))
        ttk.Combobox(
            frame, textvariable=full_var, values=["80", "85", "90", "93", "95", "100"],
            state="readonly", font=("Segoe UI", 10), width=10
        ).pack(anchor=tk.W, pady=5)

        def save():
            self.settings["enable_sounds"] = snd_var.get()
            try:
                self.settings["low_threshold"] = int(low_var.get())
                self.settings["full_threshold"] = int(full_var.get())
            except Exception:
                pass
            self.save_settings()
            # Reset notifications so they can fire again with new thresholds
            self.low_notified = False
            self.full_notified = False
            self.settings_window.destroy()

        tk.Button(
            self.settings_window, text="💾 Save", font=("Segoe UI", 10, "bold"),
            bg=TH["accent"], fg="white", relief=tk.FLAT, cursor="hand2",
            command=save, padx=20, pady=5
        ).pack(pady=20)

    def _open_settings(self, icon, item):
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

    def _on_quit(self, icon, item):
        logger.info("Battery Monitor shutting down.")
        self._running = False
        icon.stop()
        os._exit(0)

    def _get_battery_info(self):
        """Return (percent, plugged, has_battery)."""
        bat = psutil.sensors_battery()
        if bat is None:
            return 100, True, False
        return int(bat.percent), bat.power_plugged, True

    def _update_icon(self, percent, plugged, low, theme):
        """Update the tray icon image and tooltip."""
        if self.tray_icon:
            try:
                self.tray_icon.icon = create_battery_icon(percent, plugged, low, theme)
                state = "Charging" if plugged else "Discharging"
                self.tray_icon.title = f"Battery: {percent}% — {state}"
                self.tray_icon.menu = pystray.Menu(
                    pystray.MenuItem(f"Battery: {percent}%", None, enabled=False),
                    pystray.Menu.SEPARATOR,
                    pystray.MenuItem("Settings", self._open_settings, default=True),
                    pystray.MenuItem("Quit", self._on_quit),
                )
            except Exception as e:
                logger.error(f"Icon update error: {e}")

    def _monitor_loop(self):
        """Background thread: poll battery every 1 second."""
        logger.info("Battery monitoring loop started.")

        while self._running:
            try:
                percent, plugged, has_battery = self._get_battery_info()

                if not has_battery:
                    time.sleep(10)
                    continue

                low = not plugged and percent < 20
                current_theme = get_system_theme()

                # ── Plug/Unplug event detection ──
                if self.prev_plugged is not None and plugged != self.prev_plugged:
                    if plugged:
                        # PLUGGED IN
                        logger.info(f"Charger CONNECTED — Battery at {percent}%")
                        play_sound(PLUG_SOUND, self.settings)
                        ToastNotification(
                            title="Charging",
                            message=f"Battery at {percent}% — Charger connected",
                            icon_bg=C["icon_bg_green"],
                            icon_char="⚡",
                            duration_ms=4000,
                        ).show()
                        self.low_notified = False  # Reset low threshold
                    else:
                        # UNPLUGGED
                        logger.info(f"Charger DISCONNECTED — Battery at {percent}%")
                        play_sound(UNPLUG_SOUND, self.settings)
                        ToastNotification(
                            title="On Battery",
                            message=f"Battery at {percent}% — Charger disconnected",
                            icon_bg=C["icon_bg_orange"],
                            icon_char="🔋",
                            duration_ms=4000,
                        ).show()
                        self.full_notified = False  # Reset full threshold

                # ── Threshold alerts ──
                low_threshold = self.settings.get("low_threshold", 20)
                full_threshold = self.settings.get("full_threshold", 93)

                # Low battery: unplugged and below threshold
                if not plugged and percent <= low_threshold and not self.low_notified:
                    self.low_notified = True
                    logger.warning(f"LOW BATTERY: {percent}%")
                    ToastNotification(
                        title="Low Battery",
                        message=f"Battery at {percent}% — Please plug in charger",
                        icon_bg=C["icon_bg_red"],
                        icon_char="🪫",
                        duration_ms=6000,
                    ).show()

                # Reset low notification when above threshold
                if not plugged and percent > low_threshold:
                    self.low_notified = False

                # Full battery: plugged and above threshold
                if plugged and percent >= full_threshold and not self.full_notified:
                    self.full_notified = True
                    logger.info(f"BATTERY SUFFICIENT: {percent}%")
                    ToastNotification(
                        title="Battery Sufficiently Charged",
                        message=f"Battery at {percent}% — You may unplug",
                        icon_bg=C["icon_bg_green"],
                        icon_char="✅",
                        duration_ms=5000,
                    ).show()

                # Reset full notification when below threshold
                if plugged and percent < full_threshold:
                    self.full_notified = False

                # Cache battery states and update icon only when state changes or 10 seconds elapsed
                now = time.time()
                changed = (percent != self.prev_percent or 
                           plugged != self.prev_plugged or 
                           low != self.prev_low or
                           current_theme != self.prev_theme)
                force_update = (now - self.last_icon_update >= 10)

                if changed or force_update or self.prev_percent is None:
                    self._update_icon(percent, plugged, low, current_theme)
                    self.last_icon_update = now

                self.prev_percent = percent
                self.prev_plugged = plugged
                self.prev_low = low
                self.prev_theme = current_theme

            except Exception as e:
                logger.error(f"Monitor loop error: {e}")

            time.sleep(1)

    def run(self):
        logger.info("=" * 50)
        logger.info("Battery Monitor starting...")

        # Verify sounds exist
        verify_sounds()

        # Initial battery state
        percent, plugged, has_battery = self._get_battery_info()
        self.prev_percent = percent
        self.prev_plugged = plugged
        self.prev_low = not plugged and percent < 20
        self.prev_theme = get_system_theme()

        if not has_battery:
            logger.warning("No battery detected. Running in desktop mode (limited functionality).")

        icon_image = create_battery_icon(percent, plugged, self.prev_low, self.prev_theme)
        state = "Charging" if plugged else "Discharging"

        self.tray_icon = pystray.Icon(
            name="BatteryMonitor",
            icon=icon_image,
            title=f"Battery: {percent}% — {state}",
            menu=pystray.Menu(
                pystray.MenuItem(f"Battery: {percent}%", None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Settings", self._open_settings, default=True),
                pystray.MenuItem("Quit", self._on_quit),
            ),
        )

        # Start monitor thread
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()

        logger.info(f"Initial: {percent}% — {'Charging' if plugged else 'Discharging'} | Theme: {self.prev_theme}")
        logger.info("Tray icon running.")
        
        # Run tray icon in background thread
        icon_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        icon_thread.start()

        # Run Tkinter mainloop in main thread
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.after(100, self._poll_queue)
        self.root.mainloop()


if __name__ == "__main__":
    app = BatteryMonitorApp()
    app.run()
