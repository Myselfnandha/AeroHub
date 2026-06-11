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

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "Logs")
LOG_FILE = os.path.join(LOGS_DIR, "battery_monitor.log")

# Allow importing from root directory (AeroHub root)
root_dir = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if root_dir not in sys.path:
    sys.path.append(root_dir)
from toast_utils import BaseToast  # noqa: E402
import system_utils  # noqa: E402

# AeroHub Theme for Settings
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "accent": "#7c3aed",
    "fg": "#f0f0f0",
    "border": "#2d2d5e",
}

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SCRIPT_DIR, exist_ok=True)
PLUG_SOUND = os.path.join(SCRIPT_DIR, "sounds", "mac_connect.wav")
UNPLUG_SOUND = os.path.join(SCRIPT_DIR, "sounds", "mac_disconnect.wav")

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes as _ctypes

    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "AeroHub.BatteryMonitor"
    )
except Exception:
    pass

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"
        ),
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


def play_sound(sound_name, settings):
    """Play a sound (local WAV file name, system alias, or full file path) asynchronously."""
    if not settings.get("enable_sounds", True):
        return
    if not sound_name or sound_name == "None":
        return

    system_aliases = [
        "SystemAsterisk",
        "SystemExclamation",
        "SystemHand",
        "SystemQuestion",
        "SystemDefault",
    ]
    try:
        if sound_name in system_aliases:
            winsound.PlaySound(sound_name, winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif os.path.isabs(sound_name) and os.path.exists(sound_name):
            winsound.PlaySound(sound_name, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            # Treat as local WAV file name
            if not sound_name.endswith(".wav"):
                wav_name = sound_name + ".wav"
            else:
                wav_name = sound_name
            filepath = os.path.join(SCRIPT_DIR, "sounds", wav_name)
            if os.path.exists(filepath):
                winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                logger.error(f"Sound file not found: {filepath}")
    except Exception as e:
        logger.error(f"Sound playback error ({sound_name}): {e}")


# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════


def get_system_theme() -> str:
    """Return 'light' or 'dark' based on Windows registry."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        )
        val, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")
        winreg.CloseKey(key)
        return "light" if val == 1 else "dark"
    except Exception:
        return "dark"  # Default if registry key is missing


def create_battery_icon(
    percent: int, plugged: bool, low: bool = False, theme: str = "dark"
) -> Image.Image:
    """Draw a battery-shaped tray icon with fill level and theme-aware colors."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Theme-aware colors
    if theme == "light":
        border_color = (60, 60, 60, 255)
        bolt_color = (200, 150, 0, 255)  # Darker yellow/orange for contrast
        empty_fill = (200, 200, 200, 230)
    else:
        border_color = (200, 200, 200, 200)
        bolt_color = (255, 220, 0, 220)
        empty_fill = (220, 220, 220, 230)

    # Battery body (scaled to absolute maximum size within canvas)
    bx1, by1, bx2, by2 = 1, 13, 57, 51
    draw.rounded_rectangle(
        [bx1, by1, bx2, by2], radius=4, outline=border_color, width=2
    )

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
            [bx1 + 3, by1 + 3, bx1 + 3 + fill_width, by2 - 3], radius=2, fill=fill_color
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

        self.low_notified = False  # fired when unplugged < threshold
        self.full_notified = False  # fired when plugged > threshold
        self.tray_icon = None
        self._running = True

    def load_settings(self):
        default_settings = {
            "enable_sounds": True,
            "low_threshold": 20,
            "full_threshold": 93,
            "toast_pos": "Right",
            "toast_custom_x": 100,
            "toast_custom_y": 100,
            "toast_width": 260,
            "toast_height": 60,
            "toast_bg_color": "#252525",
            "toast_fg_color": "#ffffff",
            "toast_accent_color": "#28c840",
            "toast_font_size": 11,
            "toast_font_weight": "bold",
            "toast_font_family": "Segoe UI",
            "toast_emoji": "🔋",
            "toast_radius": 16,
            "toast_padding_x": 12,
            "toast_padding_y": 10,
            "toast_anim_style": "Slide",
            "toast_opacity": 0.92,
            "toast_border_width": 0,
            "toast_border_color": "#28c840",
            "toast_gradient": False,
            "toast_gradient_end": "#101625",
            "toast_shadow": True,
            "toast_accent_stripe": False,
            "toast_text_align": "left",
            "toast_auto_dismiss": True,
            "toast_click_action": "dismiss",
            "toast_progress_bar": False,
            "toast_enable_sound": True,
            "toast_sound_effect": "mac_connect",
            "sound_charger_connect": "mac_connect",
            "sound_charger_disconnect": "mac_disconnect",
            "sound_battery_full": "SystemAsterisk",
            "sound_battery_low": "SystemExclamation",
        }
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Merge with defaults to ensure new keys exist
                    for k, v in default_settings.items():
                        if k not in data:
                            data[k] = v
                    return data
            except Exception:
                pass
        return default_settings

    def save_settings(self):
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def _process_gui_queue(self):
        while not self.ui_queue.empty():
            try:
                data = self.ui_queue.get_nowait()
                if isinstance(data, dict):
                    if data.get("type") == "toast":
                        title = data["title"]
                        msg = data["msg"]
                        color_theme = data["color_theme"]

                        # Update local settings copy for correct color/emoji
                        temp_settings = dict(self.settings)
                        temp_settings["toast_enable_sound"] = (
                            False  # battery monitor plays sound directly
                        )
                        if color_theme == "low":
                            temp_settings["toast_accent_color"] = "#ff3b30"
                            temp_settings["toast_emoji"] = "🪫"
                        elif color_theme == "unplugged":
                            temp_settings["toast_accent_color"] = "#fe9f0b"
                            temp_settings["toast_emoji"] = "⚡"
                        else:
                            temp_settings["toast_accent_color"] = "#28c840"
                            temp_settings["toast_emoji"] = "🔋"

                        BaseToast(self.root, title, msg, temp_settings).show()
                    elif data.get("type") == "settings":
                        self.show_settings_window()
                elif data == "open_settings":
                    self.show_settings_window()
            except queue.Empty:
                break
            except Exception as e:
                logger.error(f"GUI queue error: {e}")

        if self._running and self.root:
            self.root.after(100, self._process_gui_queue)

    def show_settings_window(self):
        if (
            getattr(self, "settings_window_instance", None)
            and self.settings_window_instance.window.winfo_exists()
        ):
            self.settings_window_instance.window.lift()
            return

        from battery_settings_ui import SettingsWindow

        self.settings_window_instance = SettingsWindow(
            self.root, self.settings, self._on_settings_saved
        )

    def _on_settings_saved(self, new_settings):
        self.settings = new_settings
        self.save_settings()
        self.low_notified = False
        self.full_notified = False

    def _open_settings(self, icon, item):
        self.ui_queue.put("open_settings")

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
                if not system_utils.is_system_awake_and_unlocked():
                    time.sleep(2)
                    continue

                percent, plugged, has_battery = self._get_battery_info()

                if not has_battery:
                    time.sleep(10)
                    continue

                low = not plugged and percent < self.settings.get("low_threshold", 20)
                current_theme = get_system_theme()

                # ── Plug/Unplug event detection ──
                if self.prev_plugged is not None and plugged != self.prev_plugged:
                    if plugged:
                        # PLUGGED IN
                        logger.info(f"Charger CONNECTED — Battery at {percent}%")
                        play_sound(
                            self.settings.get("sound_charger_connect", "mac_connect"),
                            self.settings,
                        )
                        self.ui_queue.put(
                            {
                                "type": "toast",
                                "title": "Charging",
                                "msg": f"Battery at {percent}% — Charger connected",
                                "color_theme": "plugged",
                            }
                        )
                        self.low_notified = False  # Reset low threshold
                    else:
                        # UNPLUGGED
                        logger.info(f"Charger DISCONNECTED — Battery at {percent}%")
                        play_sound(
                            self.settings.get(
                                "sound_charger_disconnect", "mac_disconnect"
                            ),
                            self.settings,
                        )
                        self.ui_queue.put(
                            {
                                "type": "toast",
                                "title": "On Battery",
                                "msg": f"Battery at {percent}% — Charger disconnected",
                                "color_theme": "unplugged",
                            }
                        )
                        self.full_notified = False  # Reset full threshold

                # ── Threshold alerts ──
                low_threshold = self.settings.get("low_threshold", 20)
                full_threshold = self.settings.get("full_threshold", 93)

                # Low battery: unplugged and below threshold
                if not plugged and percent <= low_threshold and not self.low_notified:
                    self.low_notified = True
                    logger.warning(f"LOW BATTERY: {percent}%")
                    play_sound(
                        self.settings.get("sound_battery_low", "SystemExclamation"),
                        self.settings,
                    )
                    self.ui_queue.put(
                        {
                            "type": "toast",
                            "title": "Low Battery",
                            "msg": f"Battery at {percent}% — Please plug in charger",
                            "color_theme": "low",
                        }
                    )

                # Reset low notification when above threshold
                if not plugged and percent > low_threshold:
                    self.low_notified = False

                # Full battery: plugged and above threshold
                if plugged and percent >= full_threshold and not self.full_notified:
                    self.full_notified = True
                    logger.info(f"BATTERY SUFFICIENT: {percent}%")
                    play_sound(
                        self.settings.get("sound_battery_full", "SystemAsterisk"),
                        self.settings,
                    )
                    self.ui_queue.put(
                        {
                            "type": "toast",
                            "title": "Battery Sufficiently Charged",
                            "msg": f"Battery at {percent}% — You may unplug",
                            "color_theme": "full",
                        }
                    )

                # Reset full notification when below threshold
                if plugged and percent < full_threshold:
                    self.full_notified = False

                # Cache battery states and update icon only when state changes or 10 seconds elapsed
                now = time.time()
                changed = (
                    percent != self.prev_percent
                    or plugged != self.prev_plugged
                    or low != self.prev_low
                    or current_theme != self.prev_theme
                )
                force_update = now - self.last_icon_update >= 10

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
        self.prev_low = not plugged and percent < self.settings.get("low_threshold", 20)
        self.prev_theme = get_system_theme()

        if not has_battery:
            logger.warning(
                "No battery detected. Running in desktop mode (limited functionality)."
            )

        icon_image = create_battery_icon(
            percent, plugged, self.prev_low, self.prev_theme
        )
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

        # Start parent process monitoring
        system_utils.monitor_parent_process(lambda: self._on_quit(self.tray_icon, None))

        logger.info(
            f"Initial: {percent}% — {'Charging' if plugged else 'Discharging'} | Theme: {self.prev_theme}"
        )
        logger.info("Tray icon running.")

        # Run tray icon in background thread
        icon_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        icon_thread.start()

        # Run Tkinter mainloop in main thread
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.after(100, self._process_gui_queue)
        self.root.mainloop()


if __name__ == "__main__":
    app = BatteryMonitorApp()
    app.run()
