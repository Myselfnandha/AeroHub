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

import psutil

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing deps. Run: pip install pystray Pillow psutil")
    sys.exit(1)

import tkinter as tk

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(SCRIPT_DIR, "battery_monitor.log")
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
    "bg_toast": "#161b22",
    "plug_green": "#00ff88",
    "unplug_orange": "#ff8800",
    "low_red": "#ff3366",
    "full_green": "#00ff88",
    "text": "#f0f0f0",
    "text_dim": "#8b949e",
    "border": "#30363d",
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


def play_sound(filepath):
    """Play a WAV file asynchronously."""
    try:
        winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        logger.error(f"Sound playback error: {e}")


# ══════════════════════════════════════════════════════════
#  Toast Notification (macOS-style animated slide-in)
# ══════════════════════════════════════════════════════════
class ToastNotification:
    """Animated slide-in toast notification using Tkinter."""

    _active_toasts = []

    def __init__(self, title: str, message: str, accent_color: str, icon_char: str = "⚡",
                 duration_ms: int = 4000):
        self.title = title
        self.message = message
        self.accent = accent_color
        self.icon_char = icon_char
        self.duration = duration_ms
        self._toast = None

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
            
            # Use transparent color trick for flawless rounded corners
            toast.config(bg="#000001", borderwidth=0, highlightthickness=0, relief="flat")
            toast.attributes("-transparentcolor", "#000001")

            # Decrease size slightly: 250x55
            toast_w, toast_h = 250, 55
            screen_w = toast.winfo_screenwidth()
            final_x = screen_w - toast_w - 20
            start_x = screen_w + 10
            y_pos = 60 + len(ToastNotification._active_toasts) * 65

            toast.geometry(f"{toast_w}x{toast_h}+{start_x}+{y_pos}")

            canvas = tk.Canvas(toast, width=toast_w, height=toast_h, bg="#000001", highlightthickness=0, borderwidth=0)
            canvas.pack(fill=tk.BOTH, expand=True)

            def create_round_rect(x1, y1, x2, y2, radius=12, **kwargs):
                points = [
                    x1+radius, y1,   x1+radius, y1,   x2-radius, y1,   x2-radius, y1,
                    x2, y1,          x2, y1+radius,   x2, y1+radius,   x2, y2-radius,
                    x2, y2-radius,   x2, y2,          x2-radius, y2,   x2-radius, y2,
                    x1+radius, y2,   x1+radius, y2,   x1, y2,          x1, y2-radius,
                    x1, y2-radius,   x1, y1+radius,   x1, y1+radius,   x1, y1
                ]
                return canvas.create_polygon(points, **kwargs, smooth=True)

            # Draw the pill background
            create_round_rect(0, 0, toast_w, toast_h, radius=15, fill=C["bg_toast"], outline="")

            # Draw the icon
            canvas.create_text(30, toast_h/2, text=self.icon_char, font=("Segoe UI Emoji", 16), fill=self.accent, anchor="center")

            # Draw the title and message text
            canvas.create_text(55, 18, text=self.title, font=("Segoe UI", 9, "bold"), fill=C["text"], anchor="w")
            canvas.create_text(55, 36, text=self.message, font=("Segoe UI", 8), fill=C["text_dim"], anchor="w")

            ToastNotification._active_toasts.append(self)

            # ── Slide-in animation ──
            def slide_in(step=0):
                total_steps = 20
                if step <= total_steps:
                    progress = step / total_steps
                    # Ease-out cubic
                    ease = 1 - (1 - progress) ** 3
                    current_x = int(start_x + (final_x - start_x) * ease)
                    alpha = min(0.95, ease)
                    try:
                        toast.geometry(f"{toast_w}x{toast_h}+{current_x}+{y_pos}")
                        toast.attributes("-alpha", alpha)
                        toast.after(16, lambda: slide_in(step + 1))
                    except tk.TclError:
                        pass
                else:
                    # Hold, then fade out
                    toast.after(self.duration, lambda: fade_out(0))

            def fade_out(step=0):
                total_steps = 15
                if step <= total_steps:
                    progress = step / total_steps
                    alpha = 0.95 * (1 - progress)
                    try:
                        toast.attributes("-alpha", max(0, alpha))
                        toast.after(20, lambda: fade_out(step + 1))
                    except tk.TclError:
                        pass
                else:
                    try:
                        if self in ToastNotification._active_toasts:
                            ToastNotification._active_toasts.remove(self)
                        toast.destroy()
                        root.destroy()
                    except Exception:
                        pass

            toast.deiconify()
            slide_in(0)
            root.mainloop()

        except Exception as e:
            logger.error(f"Toast error: {e}")


# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════
import winreg

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
        text_color = (30, 30, 30, 255)
        bolt_color = (200, 150, 0, 255) # Darker yellow/orange for contrast
        empty_fill = (200, 200, 200, 230)
    else:
        border_color = (200, 200, 200, 200)
        text_color = (220, 220, 220, 255)
        bolt_color = (255, 220, 0, 220)
        empty_fill = (220, 220, 220, 230)

    # Battery body
    bx1, by1, bx2, by2 = 8, 16, 56, 52
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=4, outline=border_color, width=2)

    # Battery tip (positive terminal)
    draw.rounded_rectangle([56, 26, 62, 42], radius=2, fill=border_color)

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
        bolt = [(30, 18), (24, 34), (30, 34), (26, 50), (40, 30), (34, 30), (38, 18)]
        draw.polygon(bolt, fill=bolt_color)

    # Percentage text
    try:
        font = ImageFont.truetype("segoeui.ttf", 13)
    except Exception:
        font = ImageFont.load_default()

    text = f"{percent}%"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw) // 2, 52), text, fill=text_color, font=font)

    return img


# ══════════════════════════════════════════════════════════
#  Main Monitor
# ══════════════════════════════════════════════════════════
class BatteryMonitorApp:
    def __init__(self):
        self.prev_percent = None
        self.prev_plugged = None
        self.prev_low = None
        self.prev_theme = None
        self.last_icon_update = 0

        self.low_notified = False    # fired when unplugged < 33%
        self.full_notified = False   # fired when plugged > 93%
        self.tray_icon = None
        self._running = True

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
                        play_sound(PLUG_SOUND)
                        ToastNotification(
                            title="Charging",
                            message=f"Battery at {percent}% — Charger connected",
                            accent_color=C["plug_green"],
                            icon_char="⚡",
                            duration_ms=4000,
                        ).show()
                        self.low_notified = False  # Reset low threshold
                    else:
                        # UNPLUGGED
                        logger.info(f"Charger DISCONNECTED — Battery at {percent}%")
                        play_sound(UNPLUG_SOUND)
                        ToastNotification(
                            title="On Battery",
                            message=f"Battery at {percent}% — Charger disconnected",
                            accent_color=C["unplug_orange"],
                            icon_char="🔋",
                            duration_ms=4000,
                        ).show()
                        self.full_notified = False  # Reset full threshold

                # ── Threshold alerts ──
                # Low battery: unplugged and below 33%
                if not plugged and percent <= 33 and not self.low_notified:
                    self.low_notified = True
                    logger.warning(f"LOW BATTERY: {percent}%")
                    ToastNotification(
                        title="Low Battery",
                        message=f"Battery at {percent}% — Please plug in charger",
                        accent_color=C["low_red"],
                        icon_char="🪫",
                        duration_ms=6000,
                    ).show()

                # Reset low notification when above threshold
                if not plugged and percent > 33:
                    self.low_notified = False

                # Full battery: plugged and above 93%
                if plugged and percent >= 93 and not self.full_notified:
                    self.full_notified = True
                    logger.info(f"BATTERY SUFFICIENT: {percent}%")
                    ToastNotification(
                        title="Battery Sufficiently Charged",
                        message=f"Battery at {percent}% — You may unplug",
                        accent_color=C["full_green"],
                        icon_char="✅",
                        duration_ms=5000,
                    ).show()

                # Reset full notification when below threshold
                if plugged and percent < 93:
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
                pystray.MenuItem("Quit", self._on_quit),
            ),
        )

        # Start monitor thread
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()

        logger.info(f"Initial: {percent}% — {'Charging' if plugged else 'Discharging'} | Theme: {self.prev_theme}")
        logger.info("Tray icon running.")
        self.tray_icon.run()


if __name__ == "__main__":
    app = BatteryMonitorApp()
    app.run()
