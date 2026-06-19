# Codebase Summary: toggles

## Overview
- **Scan Date:** 2026-06-14 00:30:53
- **Source Folder:** `C:\Users\NANDHA A\Desktop\FOLDERS\UTILITIES\toggles`
- **Total Text Files:** 14
- **Estimated Token Count:** 49,843

## Directory Tree
```text
toggles/
├── battery_monitor/
│   ├── battery_monitor.py
│   ├── battery_settings_ui.py
│   ├── settings.json
│   ├── sounds/
│   │   ├── mac_connect.wav
│   │   └── mac_disconnect.wav
│   └── test_battery_monitor.py
├── temp_monitor/
│   ├── settings.json
│   ├── temp_monitor.log
│   ├── temp_monitor.py
│   └── temp_settings_ui.py
└── touch_toggle/
    ├── TouchToggle.exe
    ├── TouchToggle.ps1
    ├── install_touch_toggle_service.ps1
    ├── run_hidden.vbs
    ├── touch_settings.json
    ├── touch_toggle.py
    └── uninstall_touch_toggle_service.ps1
```

## File Contents

### File: `battery_monitor/battery_monitor.py`
- **Path:** `battery_monitor/battery_monitor.py`
- **Estimated Tokens:** 5,113
- **mtime:** 1781288700.949

```python
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
from services.aerohub_core.toast_utils import BaseToast  # noqa: E402
import services.aerohub_core.system_utils as system_utils  # noqa: E402

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
```

---

### File: `battery_monitor/battery_settings_ui.py`
- **Path:** `battery_monitor/battery_settings_ui.py`
- **Estimated Tokens:** 5,639
- **mtime:** 1781288700.952

```python
import tkinter as tk
from tkinter import ttk, colorchooser
import sys
import os

# AeroHub Theme
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "bg3": "#1e1e3f",
    "accent": "#7c3aed",
    "accent_hover": "#8b5cf6",
    "fg": "#f0f0f0",
    "fg_dim": "#a0a0b0",
    "border": "#2d2d5e",
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from services.aerohub_core.toast_utils import BaseToast, EmojiPickerPanel  # noqa: E402


class SettingsWindow:
    def __init__(self, root, current_settings, on_save_callback):
        self.parent = root
        self.settings = current_settings
        self.on_save = on_save_callback

        self.entries = {}
        self.window = tk.Toplevel(root)
        self.window.title("Battery Monitor Settings")
        self.window.geometry("800x600")
        self.window.configure(bg=TH["bg"])

        # Apply rounded corners
        try:
            import ctypes

            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                int(self.window.wm_frame(), 16),
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(2)),
                ctypes.sizeof(ctypes.c_int),
            )
        except Exception:
            pass

        try:
            from PIL import ImageTk
            from toggles.battery_monitor.battery_monitor import create_battery_icon
            icon_img = create_battery_icon(100, False)
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            self.window.iconphoto(False, self.icon_photo)
        except Exception:
            pass

        # Scan available sounds
        sounds_dir = os.path.join(SCRIPT_DIR, "sounds")
        wav_files = []
        if os.path.exists(sounds_dir):
            try:
                wav_files = [
                    os.path.splitext(f)[0]
                    for f in os.listdir(sounds_dir)
                    if f.endswith(".wav")
                ]
            except Exception:
                pass
        system_sounds = [
            "SystemAsterisk",
            "SystemExclamation",
            "SystemHand",
            "SystemQuestion",
            "SystemDefault",
        ]
        self.sound_choices = ["None"] + sorted(wav_files) + system_sounds

        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()

    def _on_close(self):
        if hasattr(self, "preview_instance") and self.preview_instance:
            try:
                self.preview_instance.force_close()
            except Exception:
                pass
            self.preview_instance = None

        # Safely delete Tkinter variables in the main thread to prevent their __del__
        # from being called by the garbage collector in a background thread,
        # which causes random STATUS_BREAKPOINT crashes in tcl86t.dll.
        for key in list(self.entries.keys()):
            var, var_type = self.entries.pop(key)
            del var

        self.window.destroy()

    def _build_ui(self):
        main_container = tk.Frame(self.window, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="BATTERY.SYS",
            font=("Consolas", 18, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
        ).pack(pady=(30, 40))

        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        f_general = tk.Frame(self.content_area, bg=TH["bg"])
        f_toast = tk.Frame(self.content_area, bg=TH["bg"])

        self.frames = {"General": f_general, "Toast FX": f_toast}

        self._build_general_tab(f_general)
        self._build_toast_tab(f_toast)

        self.current_frame = None
        self.nav_buttons = {}

        def switch_tab(name):
            if self.current_frame:
                self.current_frame.pack_forget()
                self.nav_buttons[self.current_frame_name].config(
                    bg=TH["bg2"], fg=TH["fg_dim"]
                )
            self.current_frame = self.frames[name]
            self.current_frame_name = name
            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
            self.nav_buttons[name].config(bg=TH["bg3"], fg=TH["accent"])

        for name in ["General", "Toast FX"]:
            btn = tk.Button(
                self.sidebar,
                text=f"■ {name.upper()}",
                font=("Consolas", 11, "bold"),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                activebackground=TH["bg3"],
                activeforeground=TH["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                anchor="w",
                padx=24,
                pady=12,
                command=lambda n=name: switch_tab(n),
            )
            btn.pack(fill=tk.X, pady=4)
            self.nav_buttons[name] = btn

        self.btn_save = tk.Button(
            self.sidebar,
            text="[ SAVE_CFG ]",
            font=("Consolas", 12, "bold"),
            bg=TH["accent"],
            fg=TH["bg"],
            activebackground=TH["accent_hover"],
            activeforeground=TH["bg"],
            relief=tk.FLAT,
            cursor="hand2",
            pady=12,
            command=self._save_settings_clicked,
        )
        self.btn_save.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=24)

        switch_tab("General")

    def _add_field(self, parent_frame, label, key, row, is_str=False):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))
        tk.Entry(
            parent_frame,
            textvariable=var,
            font=("Consolas", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            insertbackground=TH["accent"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=TH["accent"],
            highlightbackground=TH["border"],
            width=14,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, is_str)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_combo(self, parent_frame, label, key, row, values):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, values[0])))
        ttk.Combobox(
            parent_frame,
            textvariable=var,
            values=values,
            font=("Consolas", 10),
            state="readonly",
            width=12,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_sound_field(self, parent_frame, label, key, row, sound_choices):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)

        # Frame for combobox and Play button side-by-side
        f = tk.Frame(parent_frame, bg=TH["bg"])
        f.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))

        var = tk.StringVar(value=str(self.settings.get(key, "None")))
        combo = ttk.Combobox(
            f,
            textvariable=var,
            values=sound_choices,
            font=("Consolas", 10),
            state="readonly",
            width=14,
        )
        combo.pack(side=tk.LEFT, padx=(0, 8))

        def play_preview():
            val = var.get()
            if not val or val == "None":
                return
            system_aliases = [
                "SystemAsterisk",
                "SystemExclamation",
                "SystemHand",
                "SystemQuestion",
                "SystemDefault",
            ]
            try:
                import winsound

                if val in system_aliases:
                    winsound.PlaySound(val, winsound.SND_ALIAS | winsound.SND_ASYNC)
                else:
                    if not val.endswith(".wav"):
                        wav_name = val + ".wav"
                    else:
                        wav_name = val

                    path = os.path.join(SCRIPT_DIR, "sounds", wav_name)
                    if os.path.exists(path):
                        winsound.PlaySound(
                            path, winsound.SND_FILENAME | winsound.SND_ASYNC
                        )
                    else:
                        print(f"Sound file not found: {path}")
            except Exception as e:
                print(f"Preview play error: {e}")

        btn = tk.Button(
            f,
            text="▶",
            font=("Segoe UI", 10),
            bg=TH["bg2"],
            fg=TH["accent"],
            activebackground=TH["bg3"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=play_preview,
            width=3,
            height=1,
        )
        btn.pack(side=tk.LEFT)

        self.entries[key] = (var, True)

    def _add_color_field(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))

        def choose_color(v=var):
            c = colorchooser.askcolor(initialcolor=v.get())[1]
            if c:
                v.set(c)
                btn.config(bg=c)

        btn = tk.Button(
            parent_frame,
            bg=var.get(),
            width=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_grid_chk(self, parent_frame, label, key, row):
        var = tk.BooleanVar(value=self.settings.get(key, True))
        tk.Checkbutton(
            parent_frame,
            text=label.upper(),
            variable=var,
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
            activeforeground=TH["accent"],
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=8)
        self.entries[key] = (var, "bool")
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_emoji_picker(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "🔋")))
        f = tk.Frame(parent_frame, bg=TH["bg"])
        f.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        lbl = tk.Label(
            f, textvariable=var, font=("Segoe UI Emoji", 12), bg=TH["bg"], fg=TH["fg"]
        )
        lbl.pack(side=tk.LEFT, padx=(0, 5))

        def _on_select(emoji):
            var.set(emoji)
            if key.startswith("toast_"):
                self._schedule_preview()

        def _open_picker():
            EmojiPickerPanel(self.window, _on_select)

        btn = tk.Button(
            f,
            text="Pick",
            font=("Consolas", 8),
            bg=TH["bg2"],
            fg=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=_open_picker,
        )
        btn.pack(side=tk.LEFT)
        self.entries[key] = (var, True)

    def _build_general_tab(self, tab):
        tk.Label(
            tab,
            text="BATTERY PARAMETERS",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 20))
        f1 = tk.Frame(tab, bg=TH["bg"])
        f1.pack(fill=tk.X)
        self._add_grid_chk(f1, "Enable Plug/Unplug Sounds", "enable_sounds", 0)
        self._add_field(f1, "Low Battery Warning (%):", "low_threshold", 1)
        self._add_field(f1, "Full Battery Alert (%):", "full_threshold", 2)

        # Sound Profile Configuration
        tk.Label(
            tab,
            text="SOUND PROFILE CONFIG",
            font=("Consolas", 12, "bold"),
            bg=TH["bg"],
            fg=TH["accent"],
        ).pack(anchor=tk.W, pady=(24, 12))
        f_sounds = tk.Frame(tab, bg=TH["bg"])
        f_sounds.pack(fill=tk.X)
        self._add_sound_field(
            f_sounds,
            "Charger Connected:",
            "sound_charger_connect",
            0,
            self.sound_choices,
        )
        self._add_sound_field(
            f_sounds,
            "Charger Disconnected:",
            "sound_charger_disconnect",
            1,
            self.sound_choices,
        )
        self._add_sound_field(
            f_sounds,
            "Battery Full / Sufficient:",
            "sound_battery_full",
            2,
            self.sound_choices,
        )
        self._add_sound_field(
            f_sounds, "Battery Low:", "sound_battery_low", 3, self.sound_choices
        )

    def _build_toast_tab(self, tab):
        tk.Label(
            tab,
            text="UI / UX CONFIG",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 10))
        canvas = tk.Canvas(tab, bg=TH["bg"], highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg=TH["bg"])
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_mousewheel(event):
            try:
                w = event.widget.winfo_containing(event.x_root, event.y_root)
                while w:
                    if isinstance(w, tk.Canvas):
                        w.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        break
                    w = w.master
            except Exception:
                pass

        tab.winfo_toplevel().bind_all("<MouseWheel>", _on_mousewheel)

        f_top = tk.Frame(scrollable_frame, bg=TH["bg"])
        f_top.pack(fill=tk.BOTH, expand=True)
        f2_left = tk.Frame(f_top, bg=TH["bg"])
        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        f2_right = tk.Frame(f_top, bg=TH["bg"])
        f2_right.pack(side=tk.LEFT, fill=tk.Y)

        positions = [
            "Top-Left",
            "Top-Center",
            "Top-Right",
            "Bottom-Left",
            "Bottom-Center",
            "Bottom-Right",
            "Middle-Left",
            "Middle-Right",
            "Custom",
        ]
        animations = ["Slide", "Fade", "Bounce", "Scale", "Typewriter", "Glow", "Drop"]
        fonts = ["Segoe UI", "Consolas", "Cascadia Code", "Arial", "Verdana"]
        actions = ["dismiss", "snooze", "settings"]

        self._add_combo(f2_left, "Position:", "toast_pos", 0, positions)
        self._add_combo(f2_left, "Animation:", "toast_anim_style", 1, animations)
        self._add_field(f2_left, "Width (px):", "toast_width", 2)
        self._add_field(f2_left, "Height (px):", "toast_height", 3)
        self._add_field(f2_left, "Custom X (if custom):", "toast_custom_x", 4)
        self._add_field(f2_left, "Custom Y (if custom):", "toast_custom_y", 5)
        self._add_color_field(f2_left, "Background Color:", "toast_bg_color", 6)
        self._add_color_field(f2_left, "Text Color:", "toast_fg_color", 7)
        self._add_color_field(f2_left, "Accent Color:", "toast_accent_color", 8)
        self._add_combo(f2_left, "Font Family:", "toast_font_family", 9, fonts)
        self._add_field(f2_left, "Font Size:", "toast_font_size", 10)
        self._add_combo(
            f2_left, "Font Weight:", "toast_font_weight", 11, ["normal", "bold"]
        )
        self._add_combo(
            f2_left, "Text Align:", "toast_text_align", 12, ["left", "center", "right"]
        )

        self._add_emoji_picker(f2_right, "Emoji Icon:", "toast_emoji", 0)
        self._add_field(f2_right, "Border Radius (px):", "toast_radius", 1)
        self._add_field(f2_right, "Padding X (px):", "toast_padding_x", 2)
        self._add_field(f2_right, "Padding Y (px):", "toast_padding_y", 3)
        self._add_field(f2_right, "Opacity (0.1 - 1.0):", "toast_opacity", 4)
        self._add_field(f2_right, "Border Width (px):", "toast_border_width", 5)
        self._add_color_field(f2_right, "Border Color:", "toast_border_color", 6)
        self._add_color_field(f2_right, "Gradient End Color:", "toast_gradient_end", 7)
        self._add_combo(f2_right, "Click Action:", "toast_click_action", 8, actions)
        self._add_field(f2_right, "Duration (sec):", "toast_duration_sec", 9)
        self._add_field(f2_right, "Transition (ms):", "toast_transition_time_ms", 10)

        sound_choices = [
            "mac_connect",
            "mac_disconnect",
            "SystemAsterisk",
            "SystemExclamation",
            "SystemHand",
            "SystemQuestion",
            "SystemDefault",
        ]
        self._add_combo(
            f2_right, "Sound Effect:", "toast_sound_effect", 10, sound_choices
        )

        f3 = tk.Frame(scrollable_frame, bg=TH["bg"])
        f3.pack(fill=tk.X, pady=(15, 0))

        self._add_grid_chk(f3, "Enable Shadow/Glow", "toast_shadow", 0)
        self._add_grid_chk(f3, "Enable Gradient BG", "toast_gradient", 1)
        self._add_grid_chk(f3, "Enable Accent Stripe", "toast_accent_stripe", 2)
        self._add_grid_chk(f3, "Show Progress Bar", "toast_progress_bar", 3)
        self._add_grid_chk(f3, "Auto-Dismiss", "toast_auto_dismiss", 4)
        self._add_grid_chk(f3, "Play Warning Sound", "toast_enable_sound", 5)

        btn_frame = tk.Frame(scrollable_frame, bg=TH["bg"])
        btn_frame.pack(fill=tk.X, pady=20)
        tk.Button(
            btn_frame,
            text="[ PREVIEW_UI ]",
            font=("Consolas", 10, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
            activebackground=TH["bg3"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._preview_toast,
            padx=20,
            pady=8,
        ).pack(side=tk.RIGHT)

    def _schedule_preview(self):
        self._preview_toast(is_auto_edit=True)

    def _preview_toast(self, is_auto_edit=False):
        toast_exists = False
        if hasattr(self, "preview_instance") and self.preview_instance:
            if getattr(self.preview_instance, "toast_window", None) and self.preview_instance.toast_window.winfo_exists():
                toast_exists = True
            else:
                self.preview_instance = None

        temp_settings = dict(self.settings)
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    temp_settings[key] = float(val)
                elif var_type is False:
                    temp_settings[key] = int(val)
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        if is_auto_edit:
            temp_settings["toast_auto_dismiss"] = False
            temp_settings["toast_enable_sound"] = False

        if toast_exists:
            try:
                self.preview_instance.update_settings(temp_settings)
            except Exception:
                # Silently fail if updater isn't fully ready
                pass
        else:
            if hasattr(self, "preview_instance") and self.preview_instance:
                try:
                    self.preview_instance.force_close()
                except Exception:
                    pass
            self.preview_instance = BaseToast(
                self.window, "BATTERY PREVIEW", "Battery is full", temp_settings
            )
            self.preview_instance.show()

    def _save_settings_clicked(self):
        if hasattr(self, "preview_instance") and self.preview_instance:
            try:
                self.preview_instance.force_close()
            except Exception:
                pass
            self.preview_instance = None

        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    self.settings[key] = float(val)
                elif var_type is False:
                    self.settings[key] = int(val)
                else:
                    self.settings[key] = val
            except ValueError:
                pass
        self.on_save(self.settings)

        self.btn_save.config(text="[ SAVED ]", state=tk.DISABLED)
        def reset_btn():
            try:
                self.btn_save.config(text="[ SAVE_CFG ]", state=tk.NORMAL)
            except Exception:
                pass
        self.window.after(2000, reset_btn)
```

---

### File: `battery_monitor/settings.json`
- **Path:** `battery_monitor/settings.json`
- **Estimated Tokens:** 299
- **mtime:** 1781257317.504

```json
{
    "enable_sounds": true,
    "low_threshold": 30,
    "full_threshold": 95,
    "toast_pos": "Top-Center",
    "toast_custom_x": 120,
    "toast_custom_y": 120,
    "toast_width": 220,
    "toast_height": 30,
    "toast_bg_color": "#000000",
    "toast_fg_color": "#ffffff",
    "toast_accent_color": "#28c840",
    "toast_font_size": 11,
    "toast_font_weight": "bold",
    "toast_font_family": "Segoe UI",
    "toast_emoji": "\ud83d\udd0b",
    "toast_radius": 22,
    "toast_padding_x": 18,
    "toast_padding_y": 18,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.92,
    "toast_border_width": 0,
    "toast_border_color": "#000000",
    "toast_gradient": false,
    "toast_gradient_end": "#101625",
    "toast_shadow": false,
    "toast_accent_stripe": false,
    "toast_text_align": "center",
    "toast_auto_dismiss": true,
    "toast_click_action": "dismiss",
    "toast_progress_bar": false,
    "toast_enable_sound": true,
    "toast_sound_effect": "mac_connect",
    "toast_duration": 3,
    "sound_charger_connect": "mac_connect",
    "sound_charger_disconnect": "mac_disconnect",
    "sound_battery_full": "SystemDefault",
    "sound_battery_low": "SystemExclamation"
}
```

---

### File: `battery_monitor/test_battery_monitor.py`
- **Path:** `battery_monitor/test_battery_monitor.py`
- **Estimated Tokens:** 826
- **mtime:** 1780856515.52

```python
import os
import sys

# Add current dir to path to import battery_monitor
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import unittest  # noqa: E402
from unittest.mock import patch, MagicMock  # noqa: E402

import battery_monitor  # noqa: E402
from PIL import Image  # noqa: E402


class TestBatteryMonitor(unittest.TestCase):
    def test_get_system_theme_default(self):
        """Test theme defaults to dark if registry fails"""
        with patch("winreg.OpenKey", side_effect=Exception("Mock Registry Error")):
            theme = battery_monitor.get_system_theme()
            self.assertEqual(theme, "dark")

    def test_get_system_theme_light(self):
        """Test registry returns light theme"""
        with (
            patch("winreg.OpenKey", return_value=MagicMock()),
            patch("winreg.QueryValueEx", return_value=(1, 4)),
            patch("winreg.CloseKey"),
        ):
            theme = battery_monitor.get_system_theme()
            self.assertEqual(theme, "light")

    def test_create_battery_icon_full(self):
        """Test drawing battery icon at 100%"""
        img = battery_monitor.create_battery_icon(
            100, plugged=True, low=False, theme="dark"
        )
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (64, 64))

    def test_create_battery_icon_low(self):
        """Test drawing low battery icon"""
        img = battery_monitor.create_battery_icon(
            15, plugged=False, low=True, theme="light"
        )
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (64, 64))

    def test_battery_info_mocked(self):
        """Test battery info extraction"""
        app = battery_monitor.BatteryMonitorApp()

        mock_bat = MagicMock()
        mock_bat.percent = 85.5
        mock_bat.power_plugged = True

        with patch("psutil.sensors_battery", return_value=mock_bat):
            percent, plugged, has_battery = app._get_battery_info()
            self.assertEqual(percent, 85)
            self.assertTrue(plugged)
            self.assertTrue(has_battery)

    def test_battery_info_no_battery(self):
        """Test fallback when no battery is found"""
        app = battery_monitor.BatteryMonitorApp()

        with patch("psutil.sensors_battery", return_value=None):
            percent, plugged, has_battery = app._get_battery_info()
            self.assertEqual(percent, 100)
            self.assertTrue(plugged)
            self.assertFalse(has_battery)

    def test_play_sound_system_alias(self):
        """Test play_sound plays system aliases correctly via winsound"""
        settings = {"enable_sounds": True}
        with patch("winsound.PlaySound") as mock_play:
            battery_monitor.play_sound("SystemAsterisk", settings)
            import winsound

            mock_play.assert_called_once_with(
                "SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC
            )

    def test_play_sound_none(self):
        """Test play_sound does not play if set to None"""
        settings = {"enable_sounds": True}
        with patch("winsound.PlaySound") as mock_play:
            battery_monitor.play_sound("None", settings)
            mock_play.assert_not_called()


if __name__ == "__main__":
    unittest.main()
```

---

### File: `temp_monitor/settings.json`
- **Path:** `temp_monitor/settings.json`
- **Estimated Tokens:** 220
- **mtime:** 1780569786.725

```json
{
    "warning_temp": 65,
    "critical_temp": 70,
    "toast_pos": "Bottom-Center",
    "toast_custom_x": 100,
    "toast_custom_y": 100,
    "toast_width": 200,
    "toast_height": 50,
    "toast_bg_color": "#ffffff",
    "toast_fg_color": "#950000",
    "toast_accent_color": "#000000",
    "toast_font_size": 10,
    "toast_font_weight": "bold",
    "toast_font_family": "Arial",
    "toast_emoji": "\ud83d\udd25",
    "toast_radius": 18,
    "toast_padding_x": 18,
    "toast_padding_y": 18,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.92,
    "toast_border_width": 0,
    "toast_border_color": "#060606",
    "toast_gradient": true,
    "toast_gradient_end": "#40090a",
    "toast_shadow": true,
    "toast_accent_stripe": false,
    "toast_text_align": "right",
    "toast_auto_dismiss": true,
    "toast_click_action": "dismiss",
    "toast_progress_bar": false
}
```

---

### File: `temp_monitor/temp_monitor.log`
- **Path:** `temp_monitor/temp_monitor.log`
- **Estimated Tokens:** 15,067
- **mtime:** 1780160881.992

```
2026-05-30 22:08:43,890 - INFO - ==================================================
2026-05-30 22:08:43,890 - INFO - Temperature Monitor starting...
2026-05-30 22:08:44,681 - WARNING - LibreHardwareMonitorLib.dll not found.
2026-05-30 22:08:44,806 - INFO - WMI temperature reader initialized.
2026-05-30 22:08:46,899 - INFO - Initial CPU: 52°C | GPU: N/A
2026-05-30 22:08:46,900 - INFO - Temperature monitoring loop started.
2026-05-30 22:08:46,901 - INFO - Using reader: WMIReader
2026-05-30 22:08:46,900 - INFO - Tray icon running.
2026-05-30 22:08:47,505 - INFO - WMI temperature reader initialized.
2026-05-30 22:08:48,085 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:08:51,270 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:08:54,364 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:08:57,470 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:00,610 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:03,748 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:06,938 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:10,041 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:13,180 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:16,467 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:19,750 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:22,815 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:25,978 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:29,043 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:32,141 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:35,199 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:38,365 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:41,427 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:44,719 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:47,771 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:50,888 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:53,947 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:09:57,126 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:00,272 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:03,398 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:06,581 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:09,634 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:12,830 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:16,030 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:19,086 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:22,215 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:25,274 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:28,323 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:31,378 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:34,480 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:37,610 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:40,691 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:43,847 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:47,125 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:50,262 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:53,551 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:56,619 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:10:59,775 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:03,216 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:06,289 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:09,395 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:12,677 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:15,799 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:19,015 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:22,101 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:25,237 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:28,515 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:31,670 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:34,729 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:37,785 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:40,930 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:44,024 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:47,141 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:50,247 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:53,319 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:56,421 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:11:59,498 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:02,605 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:05,664 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:08,818 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:11,866 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:14,923 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:18,102 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:21,331 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:24,507 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:27,611 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:30,667 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:33,791 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:36,849 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:40,167 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:43,400 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:46,473 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:49,589 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:52,676 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:55,784 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:12:58,981 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:02,050 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:05,150 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:08,202 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:11,260 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:11,498 - INFO - WMI temperature reader initialized.
2026-05-30 22:13:11,728 - ERROR - Manual refresh error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:11,729 - ERROR - An error occurred when calling message handler
Traceback (most recent call last):
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 412, in _dispatcher
    return int(icon._message_handlers.get(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 201, in _on_notify
    self()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_base.py", line 111, in __call__
    self.update_menu()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_base.py", line 275, in update_menu
    self._update_menu()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 107, in _update_menu
    hmenu = self._create_menu(self.menu, callbacks)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 285, in _create_menu
    win32.InsertMenuItem(hmenu, i, True, ctypes.byref(menu_item))
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_util\win32.py", line 204, in _err
    raise ctypes.WinError()
OSError: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:14,359 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:17,422 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:20,511 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:23,674 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:26,941 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:30,131 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:32,679 - ERROR - Manual refresh error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:32,680 - ERROR - An error occurred when calling message handler
Traceback (most recent call last):
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 412, in _dispatcher
    return int(icon._message_handlers.get(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 201, in _on_notify
    self()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_base.py", line 111, in __call__
    self.update_menu()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_base.py", line 275, in update_menu
    self._update_menu()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 107, in _update_menu
    hmenu = self._create_menu(self.menu, callbacks)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 285, in _create_menu
    win32.InsertMenuItem(hmenu, i, True, ctypes.byref(menu_item))
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_util\win32.py", line 204, in _err
    raise ctypes.WinError()
OSError: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:32,861 - ERROR - Manual refresh error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:32,862 - ERROR - An error occurred when calling message handler
Traceback (most recent call last):
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 412, in _dispatcher
    return int(icon._message_handlers.get(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 201, in _on_notify
    self()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_base.py", line 111, in __call__
    self.update_menu()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_base.py", line 275, in update_menu
    self._update_menu()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 107, in _update_menu
    hmenu = self._create_menu(self.menu, callbacks)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 285, in _create_menu
    win32.InsertMenuItem(hmenu, i, True, ctypes.byref(menu_item))
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_util\win32.py", line 204, in _err
    raise ctypes.WinError()
OSError: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:33,233 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:34,612 - ERROR - Manual refresh error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:34,614 - ERROR - An error occurred when calling message handler
Traceback (most recent call last):
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 412, in _dispatcher
    return int(icon._message_handlers.get(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 201, in _on_notify
    self()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_base.py", line 111, in __call__
    self.update_menu()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_base.py", line 275, in update_menu
    self._update_menu()
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 107, in _update_menu
    hmenu = self._create_menu(self.menu, callbacks)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_win32.py", line 285, in _create_menu
    win32.InsertMenuItem(hmenu, i, True, ctypes.byref(menu_item))
  File "C:\Users\NANDHA A\AppData\Local\Programs\Python\Python312\Lib\site-packages\pystray\_util\win32.py", line 204, in _err
    raise ctypes.WinError()
OSError: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:36,296 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:39,410 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:42,583 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:45,640 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:48,737 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:51,794 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:54,850 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:13:57,970 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:01,358 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:04,541 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:07,658 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:10,919 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:14,096 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:17,401 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:20,626 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:23,675 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:26,733 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:29,898 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:32,947 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:36,051 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:39,369 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:42,430 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:45,767 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:48,960 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:52,011 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:55,141 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:14:58,307 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:01,443 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:04,560 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:07,654 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:10,725 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:13,853 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:17,041 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:20,612 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:23,754 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:27,134 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:30,240 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:33,323 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:36,431 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:39,499 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:42,550 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:45,598 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:48,700 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:51,907 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:54,983 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:15:58,337 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:01,531 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:04,726 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:08,036 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:11,300 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:14,359 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:17,537 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:20,585 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:23,692 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:26,781 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:29,837 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:32,915 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:35,974 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:39,031 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:42,157 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:45,208 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:48,370 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:51,561 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:54,816 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:16:57,976 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:01,063 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:04,260 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:07,509 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:10,561 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:13,617 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:16,930 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:20,315 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:23,504 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:26,638 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:29,762 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:33,002 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:36,058 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:39,403 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:42,480 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:45,587 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:48,694 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:51,776 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:54,894 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:17:57,952 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:01,008 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:04,068 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:07,177 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:10,275 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:13,357 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:16,687 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:20,177 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:23,361 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:26,507 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:29,634 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:32,693 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:35,745 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:38,803 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:41,861 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:44,920 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:47,970 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:51,025 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:54,082 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:18:57,255 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:00,325 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:03,417 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:06,467 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:09,567 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:12,623 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:15,706 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:18,767 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:21,860 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:24,919 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:27,978 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:31,041 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:34,099 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:37,156 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:40,213 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:43,326 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:46,413 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:49,506 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:52,564 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:55,684 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:19:59,049 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:02,111 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:05,249 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:08,304 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:11,365 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:14,423 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:17,476 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:20,702 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:23,761 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:26,920 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:29,982 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:33,089 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:36,139 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:39,261 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:42,312 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:45,367 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:48,432 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:51,582 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:54,857 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:20:58,201 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:01,517 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:04,654 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:07,986 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:11,151 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:15,092 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:18,297 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:22,493 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:25,783 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:28,873 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:32,303 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:35,665 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:38,923 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:42,117 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:45,490 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:48,763 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:52,028 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:55,270 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:21:58,594 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:01,915 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:05,264 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:08,317 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:11,377 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:14,610 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:17,709 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:20,899 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:24,039 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:27,248 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:30,442 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:33,680 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:36,738 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:39,790 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:43,076 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:46,133 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:49,384 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:52,534 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:55,585 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:22:58,635 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:01,850 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:05,036 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:08,185 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:11,237 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:14,287 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:17,351 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:20,408 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:23,697 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:26,774 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:29,907 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:33,016 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:36,087 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:39,135 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:42,198 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:45,263 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:48,320 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:51,377 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:54,606 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:23:57,714 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:00,764 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:03,854 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:06,930 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:09,988 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:13,160 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:16,214 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:19,264 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:22,325 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:25,503 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:28,558 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:31,713 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:35,185 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:38,440 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:41,553 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:44,601 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:47,761 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:50,821 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:53,876 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:56,941 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:24:59,994 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:03,074 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:06,133 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:09,219 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:12,281 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:15,326 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:18,382 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:21,540 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:24,590 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:27,649 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:30,708 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:33,765 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:36,825 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:39,880 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:42,936 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:45,991 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:49,083 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:52,153 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:55,259 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:25:58,315 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:01,379 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:04,571 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:07,625 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:10,702 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:13,749 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:16,888 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:19,944 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:23,000 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:26,048 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:29,101 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:32,156 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:35,211 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:38,278 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:41,331 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:44,384 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:47,439 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:50,557 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:53,608 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:56,852 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:26:59,967 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:03,012 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:06,241 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:09,296 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:12,346 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:15,473 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:18,526 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:21,582 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:24,630 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:27,694 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:30,798 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:33,853 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:36,901 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:39,951 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:43,006 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:46,092 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:49,202 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:52,394 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:55,649 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:27:59,137 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:02,197 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:05,256 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:08,547 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:11,840 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:14,922 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:17,978 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:21,037 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:24,228 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:27,340 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:30,484 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:33,590 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:36,666 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:39,766 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:42,817 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:45,888 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:49,043 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:52,186 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:55,242 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:28:58,365 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:01,414 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:04,475 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:07,603 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:10,668 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:13,965 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:17,016 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:20,077 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:23,135 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:26,201 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:29,258 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:32,378 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:35,446 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:38,603 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:41,682 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:44,768 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:47,826 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:50,891 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:53,952 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:29:57,027 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:00,158 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:03,212 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:06,273 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:09,328 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:12,493 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:15,550 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:18,605 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:21,761 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:24,816 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:27,913 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:30,990 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:34,045 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:37,100 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:40,155 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:43,220 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:46,274 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:49,321 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:52,408 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:55,462 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:30:58,724 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:01,992 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:05,044 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:08,094 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:11,176 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:14,239 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:17,288 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:20,342 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:23,396 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:26,452 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:29,528 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:32,582 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:35,636 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:38,804 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:41,867 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:44,923 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:48,147 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:51,202 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:54,257 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:31:57,304 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:00,351 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:03,418 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:06,471 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:09,529 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:12,582 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:15,636 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:18,694 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:21,756 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:24,811 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:27,866 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:30,921 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:33,976 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:37,032 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:40,098 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:43,161 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:46,223 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:49,270 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:52,322 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:55,417 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:32:58,534 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:01,597 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:04,656 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:07,735 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:10,791 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:13,839 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:16,895 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:19,952 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:23,007 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:26,053 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:29,104 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:32,151 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:35,199 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:38,245 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:41,292 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:44,340 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:47,416 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:50,461 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:53,516 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:56,571 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:33:59,746 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:02,796 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:05,851 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:08,909 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:11,967 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:15,034 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:18,089 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:21,151 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:24,207 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:27,252 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:30,332 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:33,444 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:36,498 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:39,555 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:42,682 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:45,732 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:48,877 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:51,927 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:54,983 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:34:58,139 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:01,193 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:04,253 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:07,420 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:10,472 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:13,527 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:16,581 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:19,663 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:22,718 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:25,764 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:28,821 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:31,877 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:34,933 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:37,988 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:41,043 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:44,098 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:47,144 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:50,200 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:53,249 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:56,438 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:35:59,497 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:02,553 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:05,647 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:08,698 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:11,756 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:14,810 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:17,873 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:20,920 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:23,970 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:27,051 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:30,098 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:33,157 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:36,213 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:39,310 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:42,357 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:45,411 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:48,500 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:51,596 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:54,643 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:36:57,699 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:00,763 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:03,820 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:06,868 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:09,915 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:12,970 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:16,045 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:19,091 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:22,146 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:25,221 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:28,269 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:31,327 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:34,381 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:37,483 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:40,536 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:43,600 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:46,702 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:49,751 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:52,807 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:55,871 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:37:58,944 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
2026-05-30 22:38:01,992 - ERROR - Tray update error: [WinError 87] The parameter is incorrect.
```

---

### File: `temp_monitor/temp_monitor.py`
- **Path:** `temp_monitor/temp_monitor.py`
- **Estimated Tokens:** 8,708
- **mtime:** 1781288700.955

```python
"""
Temperature Monitor — CPU/GPU temperature monitoring with tray display and animated toast alerts.
Uses LibreHardwareMonitor COM server for accurate readings.
Falls back to WMI if LibreHWMon is not available.
"""

import os
import sys
import time
import threading
import logging
import logging.handlers
import tkinter as tk
import json
import queue

# AeroHub Theme for Settings
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "accent": "#ff3366",  # Red/pink accent for temp
    "fg": "#f0f0f0",
    "border": "#2d2d5e",
}

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing deps. Run: pip install pystray Pillow")
    sys.exit(1)

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "Logs")
LOG_FILE = os.path.join(LOGS_DIR, "temp_monitor.log")

# Allow importing from root directory (AeroHub root)
root_dir = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if root_dir not in sys.path:
    sys.path.append(root_dir)
from services.aerohub_core.toast_utils import BaseToast  # noqa: E402
import services.aerohub_core.system_utils as system_utils  # noqa: E402

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SCRIPT_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes as _ctypes

    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "AeroHub.TempMonitor"
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
logger = logging.getLogger("TempMonitor")


# ── Colors ──
def temp_color(temp: float) -> tuple:
    """Return RGBA color based on temperature."""
    if temp < 60:
        return (0, 255, 136)  # green
    elif temp < 75:
        return (255, 221, 0)  # yellow
    elif temp < 85:
        return (255, 136, 0)  # orange
    else:
        return (255, 51, 102)  # red


def temp_hex(temp: float) -> str:
    r, g, b = temp_color(temp)
    return f"#{r:02x}{g:02x}{b:02x}"


# ══════════════════════════════════════════════════════════
#  Temperature Readers
# ══════════════════════════════════════════════════════════
class LibreHWMonReader:
    """Read temperatures via LibreHardwareMonitor COM/DLL."""

    def __init__(self):
        self.computer = None
        self.available = False
        self._init()

    def _init(self):
        try:
            import clr

            # Try common install paths
            dll_paths = [
                r"C:\Program Files\LibreHardwareMonitor\LibreHardwareMonitorLib.dll",
                r"C:\Program Files (x86)\LibreHardwareMonitor\LibreHardwareMonitorLib.dll",
                os.path.join(SCRIPT_DIR, "LibreHardwareMonitorLib.dll"),
            ]
            loaded = False
            for dll in dll_paths:
                if os.path.isfile(dll):
                    clr.AddReference(dll)
                    loaded = True
                    logger.info(f"Loaded LibreHWMon DLL: {dll}")
                    break

            if not loaded:
                # Try adding by name (if in GAC or current dir)
                try:
                    clr.AddReference("LibreHardwareMonitorLib")
                    loaded = True
                except Exception:
                    pass

            if not loaded:
                logger.warning("LibreHardwareMonitorLib.dll not found.")
                return

            from LibreHardwareMonitor.Hardware import Computer, SensorType

            self.computer = Computer()
            self.computer.IsCpuEnabled = True
            self.computer.IsGpuEnabled = True
            self.computer.IsMotherboardEnabled = True
            self.computer.IsStorageEnabled = True
            self.computer.Open()
            self.available = True
            self.SensorType = SensorType
            logger.info("LibreHardwareMonitor initialized successfully.")

        except ImportError:
            logger.warning("pythonnet (clr) not installed. LibreHWMon unavailable.")
        except Exception as e:
            logger.warning(f"LibreHWMon init failed: {e}")

    def read_temps(self) -> dict:
        """Return dict of {sensor_name: temp_celsius}."""
        temps = {}
        if not self.available or not self.computer:
            return temps

        try:
            for hw in self.computer.Hardware:
                hw.Update()
                for sub in hw.SubHardware:
                    sub.Update()
                    for sensor in sub.Sensors:
                        if (
                            sensor.SensorType == self.SensorType.Temperature
                            and sensor.Value is not None
                        ):
                            name = f"{hw.Name} / {sensor.Name}"
                            temps[name] = float(sensor.Value)

                for sensor in hw.Sensors:
                    if (
                        sensor.SensorType == self.SensorType.Temperature
                        and sensor.Value is not None
                    ):
                        name = f"{hw.Name} / {sensor.Name}"
                        temps[name] = float(sensor.Value)
        except Exception as e:
            logger.error(f"LibreHWMon read error: {e}")

        return temps

    def close(self):
        if self.computer:
            try:
                self.computer.Close()
            except Exception:
                pass


class WMIReader:
    """Fallback: read temperatures via WMI."""

    def __init__(self):
        self.available = True
        self._local = threading.local()
        self._is_ohm = False
        self.consecutive_failures = 0

    def read_temps(self) -> dict:
        temps = {}
        if not self.available:
            return temps

        initialized = False
        try:
            import pythoncom

            pythoncom.CoInitialize()
            initialized = True
        except Exception:
            pass

        try:
            import wmi

            # Fetch or initialize wmi_obj for the current thread
            wmi_obj = getattr(self._local, "wmi_obj", None)
            if not wmi_obj:
                try:
                    wmi_obj = wmi.WMI(namespace="root\\wmi")
                    self._is_ohm = False
                    self._local.wmi_obj = wmi_obj
                    logger.info("WMI temperature reader initialized.")
                except Exception as e1:
                    try:
                        wmi_obj = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                        self._is_ohm = True
                        self._local.wmi_obj = wmi_obj
                        logger.info("OpenHardwareMonitor WMI reader initialized.")
                    except Exception as e2:
                        logger.warning(f"WMI lazy init failed: {e1} | {e2}")
                        self.consecutive_failures += 1

                        is_access_denied = any(
                            "0x80041003" in str(ex)
                            or "80041003" in str(ex)
                            or "-2147217405" in str(ex)
                            or "access denied" in str(ex).lower()
                            for ex in (e1, e2)
                        )
                        if is_access_denied or self.consecutive_failures >= 3:
                            reason = (
                                "Access Denied (requires Administrator)"
                                if is_access_denied
                                else f"{self.consecutive_failures} consecutive failures"
                            )
                            logger.warning(f"WMI reader permanently disabled: {reason}")
                            self.available = False
                        return temps

            if self._is_ohm:
                # OpenHardwareMonitor WMI
                for sensor in wmi_obj.Sensor():
                    if sensor.SensorType == "Temperature":
                        temps[sensor.Name] = float(sensor.Value)
            else:
                # Standard WMI thermal zone
                for tz in wmi_obj.MSAcpi_ThermalZoneTemperature():
                    # WMI returns temp in tenths of Kelvin
                    temp_c = (tz.CurrentTemperature / 10.0) - 273.15
                    temps[f"Thermal Zone {tz.InstanceName}"] = round(temp_c, 1)

            # Reset consecutive failures on successful read
            self.consecutive_failures = 0
        except Exception as e:
            logger.error(f"WMI read error: {e}")
            self._local.wmi_obj = None  # Force reconnection next time for this thread
            self.consecutive_failures += 1

            # 0x80041003 is WBEM_E_ACCESS_DENIED (Access Denied / privilege issue)
            # -2147217405 is the signed 32-bit int representation of 0x80041003
            is_access_denied = (
                "0x80041003" in str(e)
                or "80041003" in str(e)
                or "-2147217405" in str(e)
                or "access denied" in str(e).lower()
            )

            if is_access_denied or self.consecutive_failures >= 3:
                reason = (
                    "Access Denied (requires Administrator)"
                    if is_access_denied
                    else f"{self.consecutive_failures} consecutive failures"
                )
                logger.warning(f"WMI reader permanently disabled: {reason}")
                self.available = False
        finally:
            if initialized:
                try:
                    pythoncom.CoUninitialize()
                except Exception:
                    pass

        return temps

    def close(self):
        self._local = threading.local()


class SimulatedReader:
    """Fallback when no hardware reader is available — shows a message."""

    def __init__(self):
        self.available = True
        logger.warning(
            "No hardware temperature reader available. Using simulated data."
        )

    def read_temps(self) -> dict:
        import math

        t = time.time()
        # Dynamic sine wave oscillating between 45 and 55 for high-fidelity premium display
        cpu_t = 48.0 + 6.0 * math.sin(t / 20.0)
        gpu_t = 44.0 + 4.0 * math.cos(t / 25.0)
        return {
            "CPU Package (simulated)": round(cpu_t, 1),
            "GPU Core (simulated)": round(gpu_t, 1),
        }

    def close(self):
        pass


# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════
def create_temp_icon(temp: float) -> Image.Image:
    """Draw tray icon with temperature number and color-coded background."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r, g, b = temp_color(temp)
    draw.rounded_rectangle([2, 2, 62, 62], radius=8, fill=(r, g, b, 230))

    # Temperature text (increased font size to 36 and centered)
    try:
        font = ImageFont.truetype("segoeuib.ttf", 36)
    except Exception:
        try:
            font = ImageFont.truetype("segoeui.ttf", 36)
        except Exception:
            font = ImageFont.load_default()

    temp_str = str(int(temp)) if temp > 0 else "N/A"
    bbox = draw.textbbox((0, 0), temp_str, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Exactly center the text
    x = (size - tw) // 2
    y = (size - th) // 2 - bbox[1]
    draw.text((x, y), temp_str, fill=(0, 0, 0, 235), font=font)

    return img


# ══════════════════════════════════════════════════════════
#  Main App
# ══════════════════════════════════════════════════════════
class TempMonitorApp:
    def __init__(self):
        self.settings_path = os.path.join(SCRIPT_DIR, "settings.json")
        self.settings = self.load_settings()
        self.ui_queue = queue.Queue()
        self.root = None
        self.settings_window = None

        self.reader = None
        self.tray_icon = None
        self._running = True
        self._paused = False
        self._warning_fired = False
        self._critical_fired = False
        self.all_temps = {}
        self.cpu_temp = 0.0
        self.gpu_temp = 0.0
        self.default_display_sensor = None

    def load_settings(self):
        default_settings = {
            "warning_temp": 75,
            "critical_temp": 85,
            "toast_pos": "Top-Right",
            "toast_custom_x": 100,
            "toast_custom_y": 100,
            "toast_width": 280,
            "toast_height": 70,
            "toast_bg_color": "#252525",
            "toast_fg_color": "#ffffff",
            "toast_accent_color": "#ff3366",
            "toast_font_size": 11,
            "toast_font_weight": "bold",
            "toast_font_family": "Segoe UI",
            "toast_emoji": "🔥",
            "toast_radius": 16,
            "toast_padding_x": 16,
            "toast_padding_y": 16,
            "toast_anim_style": "Drop",
            "toast_opacity": 0.92,
            "toast_border_width": 1,
            "toast_border_color": "#444444",
            "toast_gradient": False,
            "toast_gradient_end": "#1a1a2e",
            "toast_shadow": True,
            "toast_accent_stripe": True,
            "toast_text_align": "left",
            "toast_auto_dismiss": True,
            "toast_click_action": "dismiss",
            "toast_progress_bar": False,
        }
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
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

    def _apply_dwm_rounding(self, hwnd):
        try:
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2
            import ctypes

            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                ctypes.sizeof(ctypes.c_int),
            )
        except Exception:
            pass

    def show_settings_window(self):
        if self.settings_window and self.settings_window.window.winfo_exists():
            self.settings_window.window.lift()
            return

        from temp_settings_ui import SettingsWindow

        self.settings_window = SettingsWindow(
            self.root, self.settings, self._on_settings_saved
        )

    def _on_settings_saved(self, new_settings):
        self.settings = new_settings
        self.save_settings()
        self._warning_fired = False
        self._critical_fired = False

    def _open_settings(self, icon, item):
        self.ui_queue.put("open_settings")

    def _poll_queue(self):
        try:
            while not self.ui_queue.empty():
                cmd = self.ui_queue.get_nowait()
                if isinstance(cmd, dict) and cmd.get("type") == "toast":
                    title = cmd["title"]
                    msg = cmd["msg"]
                    color_theme = cmd["color_theme"]

                    temp_settings = dict(self.settings)
                    if color_theme == "critical":
                        temp_settings["toast_accent_color"] = "#ff3366"
                        temp_settings["toast_emoji"] = "🔥"
                    elif color_theme == "warning":
                        temp_settings["toast_accent_color"] = "#ff8800"
                        temp_settings["toast_emoji"] = "⚠"

                    BaseToast(self.root, title, msg, temp_settings).show()
                elif cmd == "open_settings":
                    self.show_settings_window()
        except Exception:
            pass
        if self.root:
            self.root.after(100, self._poll_queue)

    def _start_udp_listener(self):
        """Start UDP listener on port 5099 for IPC commands (e.g. from AeroHub)."""
        import socket

        def listener():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                except Exception:
                    pass
                sock.bind(("127.0.0.1", 5099))
                logger.info("TempMonitor UDP IPC Listener bound to 127.0.0.1:5099")

                while self._running:
                    data, addr = sock.recvfrom(1024)
                    msg = data.decode("utf-8").strip()
                    if msg == "game_mode:on":
                        logger.info(
                            "[UDP] Game Mode activated. Pausing temp monitor..."
                        )
                        self._paused = True
                    elif msg == "game_mode:off":
                        logger.info(
                            "[UDP] Game Mode deactivated. Resuming temp monitor..."
                        )
                        self._paused = False
                        self._force_refresh()
            except Exception as e:
                logger.error(f"Error in UDP listener: {e}")

        threading.Thread(target=listener, daemon=True).start()

    def _init_reader(self):
        """Initialize the best available temperature reader."""
        # Try LibreHardwareMonitor first
        lhm = LibreHWMonReader()
        if lhm.available:
            self.reader = lhm
            return

        # Try WMI
        wmi_r = WMIReader()
        if wmi_r.available:
            self.reader = wmi_r
            return

        # Simulated fallback
        self.reader = SimulatedReader()

    def _identify_cpu_gpu(self, temps: dict):
        """Extract primary CPU and GPU temps from the sensor dict."""
        cpu = 0.0
        gpu = 0.0

        for name, val in temps.items():
            name_l = name.lower()
            if val <= 0 or val > 150:
                continue
            if "cpu" in name_l and (
                "package" in name_l or "core" in name_l or "tctl" in name_l
            ):
                cpu = max(cpu, val)
            elif "cpu" in name_l and cpu == 0:
                cpu = val
            elif "gpu" in name_l and (
                "hot spot" in name_l or "core" in name_l or "temperature" in name_l
            ):
                gpu = max(gpu, val)
            elif "gpu" in name_l and gpu == 0:
                gpu = val

        # Fallback: just use the highest temps
        if cpu == 0 and temps:
            for name, val in temps.items():
                if 0 < val < 150 and "cpu" in name.lower():
                    cpu = val
                    break
        if cpu == 0 and temps:
            vals = [v for v in temps.values() if 0 < v < 150]
            cpu = max(vals) if vals else 0

        return cpu, gpu

    def _shorten_name(self, name: str) -> str:
        """Shorten verbose hardware sensor names to compact labels."""
        name_upper = name.upper()
        mappings = {
            "BATZ": "Battery Temp",
            "CHGZ": "Charger Temp",
            "CPUZ": "CPU Temp",
            "EXTZ": "External Temp",
            "GFXZ": "Graphics Zone",
            "LOCZ": "Local Temp",
            "PCHZ": "PCH Zone",
        }
        for key, value in mappings.items():
            if key in name_upper:
                return value
        if "THERMAL ZONE" in name_upper or "THERMALZONE" in name_upper:
            parts = name.split("\\")
            if parts:
                last_part = parts[-1].replace("_0", "").replace("_1", "").strip()
                if last_part.upper().startswith("THERMAL ZONE"):
                    last_part = last_part[12:].strip()
                return f"{last_part} Zone" if last_part else "Thermal Zone"

        if " / " in name:
            parts = name.split(" / ")
            hw_name = parts[0].strip()
            sensor_name = parts[1].strip()

            # Identify component category
            hw_lower = hw_name.lower()
            if "cpu" in hw_lower or "core i" in hw_lower or "ryzen" in hw_lower:
                comp = "CPU"
            elif "gpu" in hw_lower or "geforce" in hw_lower or "radeon" in hw_lower:
                comp = "GPU"
            elif (
                "samsung" in hw_lower
                or "ssd" in hw_lower
                or "wds" in hw_lower
                or "crucial" in hw_lower
                or "kingston" in hw_lower
                or "sandisk" in hw_lower
                or "nvme" in hw_lower
                or "hdd" in hw_lower
            ):
                # Extract drive model if possible (e.g. Samsung SSD 970 EVO -> SSD 970)
                comp = (
                    hw_name.replace("Samsung SSD", "SSD")
                    .replace("NVMe", "")
                    .replace("SATA", "")
                )
                comp = " ".join(comp.split()[:2])  # Keep first two words
            else:
                # Motherboard or other
                comp = (
                    "MB"
                    if (
                        "asus" in hw_lower
                        or "msi" in hw_lower
                        or "gigabyte" in hw_lower
                        or "asrock" in hw_lower
                    )
                    else hw_name
                )
                comp = " ".join(comp.split()[:2])

            # Shorten sensor name
            sensor_name = sensor_name.replace("CPU Package", "Pkg").replace(
                "GPU Core", "Core"
            )
            sensor_name = sensor_name.replace("Temperature", "Temp").replace(
                "Hot Spot", "Hot"
            )
            sensor_name = sensor_name.replace("Package", "Pkg")

            if comp.lower() in sensor_name.lower():
                return sensor_name
            return f"{comp} {sensor_name}"

        replacements = {
            "CPU Package": "CPU Pkg",
            "GPU Hot Spot": "GPU Hot",
            "Temperature": "Temp",
            "Package": "Pkg",
            " (simulated)": " (sim)",
        }
        for old, new in replacements.items():
            name = name.replace(old, new)
        return name

    def _force_refresh(self, icon=None, item=None):
        """Force an immediate temperature refresh on left-click."""
        try:
            self.all_temps = self.reader.read_temps()
            if not getattr(self.reader, "available", True) and not isinstance(
                self.reader, SimulatedReader
            ):
                self.reader = SimulatedReader()
                self.all_temps = self.reader.read_temps()
            self.cpu_temp, self.gpu_temp = self._identify_cpu_gpu(self.all_temps)
            if (
                self.default_display_sensor
                and self.default_display_sensor in self.all_temps
            ):
                display_temp = self.all_temps[self.default_display_sensor]
            else:
                display_temp = self.cpu_temp if self.cpu_temp > 0 else self.gpu_temp
            if self.tray_icon:
                self.tray_icon.icon = create_temp_icon(display_temp)
                lines = []
                for name, val in sorted(self.all_temps.items()):
                    # Filter out individual CPU core sensors to save tooltip space for other components
                    name_lower = name.lower()
                    if "core #" in name_lower or "cpu core" in name_lower:
                        has_pkg = any(
                            "package" in k.lower() or "tctl" in k.lower()
                            for k in self.all_temps.keys()
                        )
                        if has_pkg:
                            continue
                    short_name = self._shorten_name(name)
                    lines.append(f"{short_name}: {val:.0f}°C")
                tooltip_str = "\n".join(lines)
                if len(tooltip_str) > 127:
                    tooltip_str = tooltip_str[:124] + "..."
                self.tray_icon.title = tooltip_str
                self.tray_icon.menu = self._build_sensor_menu()
            logger.info("Manual temperature refresh completed.")
        except Exception as e:
            logger.error(f"Manual refresh error: {e}")

    def _monitor_loop(self):
        """Background monitoring thread."""
        try:
            import pythoncom

            pythoncom.CoInitialize()
        except Exception:
            pass
        logger.info("Temperature monitoring loop started.")
        reader_name = type(self.reader).__name__
        logger.info(f"Using reader: {reader_name}")

        while self._running:
            if (
                getattr(self, "_paused", False)
                or not system_utils.is_system_awake_and_unlocked()
            ):
                time.sleep(3)
                continue
            try:
                self.all_temps = self.reader.read_temps()
                # Check if current reader became unavailable due to read error
                if not getattr(self.reader, "available", True) and not isinstance(
                    self.reader, SimulatedReader
                ):
                    logger.warning(
                        "Active reader failed. Falling back to SimulatedReader."
                    )
                    self.reader = SimulatedReader()
                    self.all_temps = self.reader.read_temps()
                self.cpu_temp, self.gpu_temp = self._identify_cpu_gpu(self.all_temps)

                if (
                    self.default_display_sensor
                    and self.default_display_sensor in self.all_temps
                ):
                    display_temp = self.all_temps[self.default_display_sensor]
                else:
                    display_temp = self.cpu_temp if self.cpu_temp > 0 else self.gpu_temp

                # Update tray icon and dynamic tooltip
                if self.tray_icon:
                    try:
                        self.tray_icon.icon = create_temp_icon(display_temp)

                        # Generate dynamic tooltip listing all sensor temperatures
                        lines = []
                        for name, val in sorted(self.all_temps.items()):
                            # Filter out individual CPU core sensors to save tooltip space for other components
                            name_lower = name.lower()
                            if "core #" in name_lower or "cpu core" in name_lower:
                                has_pkg = any(
                                    "package" in k.lower() or "tctl" in k.lower()
                                    for k in self.all_temps.keys()
                                )
                                if has_pkg:
                                    continue
                            short_name = self._shorten_name(name)
                            lines.append(f"{short_name}: {val:.0f}°C")

                        tooltip_str = "\n".join(lines)
                        if len(tooltip_str) > 127:
                            tooltip_str = tooltip_str[:124] + "..."

                        self.tray_icon.title = tooltip_str

                        # Dynamically rebuild the static menu with latest temperatures
                        if hasattr(self, "tray_icon") and self.tray_icon:
                            self.tray_icon.menu = self._build_sensor_menu()
                            self.tray_icon.update_menu()
                    except Exception as e:
                        logger.error(f"Tray update error: {e}")

                # ── Temperature alerts ──
                max_temp = (
                    max(self.cpu_temp, self.gpu_temp)
                    if self.gpu_temp > 0
                    else self.cpu_temp
                )
                warning_temp = self.settings.get("warning_temp", 75)
                critical_temp = self.settings.get("critical_temp", 85)

                if max_temp >= critical_temp and not self._critical_fired:
                    self._critical_fired = True
                    self._warning_fired = True
                    source = "CPU" if self.cpu_temp >= critical_temp else "GPU"
                    logger.critical(f"CRITICAL: {source} at {max_temp:.0f}°C!")
                    self.ui_queue.put(
                        {
                            "type": "toast",
                            "title": f"CRITICAL: {source} at {max_temp:.0f}°C!",
                            "msg": "Thermal throttling risk! Close heavy applications.",
                            "color_theme": "critical",
                        }
                    )

                elif max_temp >= warning_temp and not self._warning_fired:
                    self._warning_fired = True
                    source = "CPU" if self.cpu_temp >= warning_temp else "GPU"
                    logger.warning(f"WARNING: {source} at {max_temp:.0f}°C")
                    self.ui_queue.put(
                        {
                            "type": "toast",
                            "title": f"Temperature Warning: {source} at {max_temp:.0f}°C",
                            "msg": "Temperature is elevated. Monitor your workload.",
                            "color_theme": "warning",
                        }
                    )

                # Reset alerts when temp drops
                if max_temp < warning_temp - 5:
                    self._warning_fired = False
                    self._critical_fired = False
                elif max_temp < critical_temp - 5:
                    self._critical_fired = False

            except Exception as e:
                logger.error(f"Monitor loop error: {e}")

            time.sleep(3)

    def _set_display_sensor(self, sensor_name):
        self.default_display_sensor = sensor_name
        self._force_refresh()

    def _build_sensor_menu(self):
        """Build menu items with live temperatures."""
        items = []

        # Show all temps at the top
        if self.all_temps:
            for name, val in sorted(self.all_temps.items()):
                short = self._shorten_name(name)
                items.append(
                    pystray.MenuItem(f"{short}: {val:.0f}°C", None, enabled=False)
                )
        else:
            items.append(pystray.MenuItem("No sensors detected", None, enabled=False))

        items.append(pystray.Menu.SEPARATOR)

        # Controls
        items.append(pystray.MenuItem("Refresh Now", self._force_refresh, default=True))
        items.append(pystray.Menu.SEPARATOR)

        display_items = []
        display_items.append(
            pystray.MenuItem(
                "Auto (CPU/GPU)",
                lambda icon, item: self._set_display_sensor(None),
                checked=lambda item: self.default_display_sensor is None,
                radio=True,
            )
        )
        display_items.append(pystray.Menu.SEPARATOR)

        if self.all_temps:
            for name in sorted(self.all_temps.keys()):
                short = self._shorten_name(name)

                def make_callback(s_name):
                    return lambda icon, item: self._set_display_sensor(s_name)

                def make_checked(s_name):
                    return lambda item: self.default_display_sensor == s_name

                display_items.append(
                    pystray.MenuItem(
                        short,
                        make_callback(name),
                        checked=make_checked(name),
                        radio=True,
                    )
                )

        items.append(
            pystray.MenuItem("Set Default Display", pystray.Menu(*display_items))
        )
        items.append(pystray.Menu.SEPARATOR)

        warn_t = self.settings.get("warning_temp", 75)
        crit_t = self.settings.get("critical_temp", 85)
        items.append(pystray.MenuItem(f"⚠ Warn: {warn_t}°C", None, enabled=False))
        items.append(pystray.MenuItem(f"🔥 Crit: {crit_t}°C", None, enabled=False))

        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem("Settings", self._open_settings))
        items.append(pystray.MenuItem("Quit", self._on_quit))
        return pystray.Menu(*items)

    def _on_quit(self, icon, item):
        logger.info("Temperature Monitor shutting down.")
        self._running = False
        if self.reader:
            self.reader.close()
        icon.stop()
        os._exit(0)

    def run(self):
        logger.info("=" * 50)
        logger.info("Temperature Monitor starting...")

        self._init_reader()

        # Initial read
        self.all_temps = self.reader.read_temps()
        self.cpu_temp, self.gpu_temp = self._identify_cpu_gpu(self.all_temps)
        if (
            self.default_display_sensor
            and self.default_display_sensor in self.all_temps
        ):
            display_temp = self.all_temps[self.default_display_sensor]
        else:
            display_temp = self.cpu_temp if self.cpu_temp > 0 else self.gpu_temp

        icon_image = create_temp_icon(display_temp)
        gpu_str = f"{self.gpu_temp:.0f}°C" if self.gpu_temp > 0 else "N/A"

        # Unused variables removed for linting

        self.tray_icon = pystray.Icon(
            name="TempMonitor",
            icon=icon_image,
            title=f"CPU: {self.cpu_temp:.0f}°C | GPU: {gpu_str}",
            menu=self._build_sensor_menu(),
        )

        # Start UDP listener for game mode
        self._start_udp_listener()

        # Start monitor thread
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()

        # Start parent process monitoring
        system_utils.monitor_parent_process(lambda: self._on_quit(self.tray_icon, None))

        logger.info(f"Initial CPU: {self.cpu_temp:.0f}°C | GPU: {gpu_str}")
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
    app = TempMonitorApp()
    app.run()
```

---

### File: `temp_monitor/temp_settings_ui.py`
- **Path:** `temp_monitor/temp_settings_ui.py`
- **Estimated Tokens:** 4,404
- **mtime:** 1781288700.957

```python
import tkinter as tk
from tkinter import ttk, colorchooser
import sys
import os

# AeroHub Theme
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "bg3": "#1e1e3f",
    "accent": "#ff3366",  # Red/pink accent for temp
    "accent_hover": "#ff6688",
    "fg": "#f0f0f0",
    "fg_dim": "#a0a0b0",
    "border": "#2d2d5e",
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from services.aerohub_core.toast_utils import BaseToast, EmojiPickerPanel
except ImportError:
    pass


class SettingsWindow:
    def __init__(self, root, current_settings, on_save_callback):
        self.parent = root
        self.settings = current_settings
        self.on_save = on_save_callback

        self.entries = {}
        self.window = tk.Toplevel(root)
        self.window.title("Temperature Monitor Settings")
        self.window.geometry("800x600")
        self.window.configure(bg=TH["bg"])

        # Apply rounded corners
        try:
            import ctypes

            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                int(self.window.wm_frame(), 16),
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(2)),
                ctypes.sizeof(ctypes.c_int),
            )
        except Exception:
            pass

        try:
            from PIL import ImageTk
            from toggles.temp_monitor.temp_monitor import create_temp_icon
            icon_img = create_temp_icon(45.0)
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            self.window.iconphoto(False, self.icon_photo)
        except Exception:
            pass

        def on_closing():
            if hasattr(self, "preview_instance") and self.preview_instance:
                try:
                    self.preview_instance.force_close()
                except Exception:
                    pass
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        self._build_ui()

    def _build_ui(self):
        main_container = tk.Frame(self.window, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="TEMP.SYS",
            font=("Consolas", 18, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
        ).pack(pady=(30, 40))

        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        f_general = tk.Frame(self.content_area, bg=TH["bg"])
        f_toast = tk.Frame(self.content_area, bg=TH["bg"])

        self.frames = {"General": f_general, "Toast FX": f_toast}

        self._build_general_tab(f_general)
        self._build_toast_tab(f_toast)

        self.current_frame = None
        self.nav_buttons = {}

        def switch_tab(name):
            if self.current_frame:
                self.current_frame.pack_forget()
                self.nav_buttons[self.current_frame_name].config(
                    bg=TH["bg2"], fg=TH["fg_dim"]
                )
            self.current_frame = self.frames[name]
            self.current_frame_name = name
            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
            self.nav_buttons[name].config(bg=TH["bg3"], fg=TH["accent"])

        for name in ["General", "Toast FX"]:
            btn = tk.Button(
                self.sidebar,
                text=f"■ {name.upper()}",
                font=("Consolas", 11, "bold"),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                activebackground=TH["bg3"],
                activeforeground=TH["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                anchor="w",
                padx=24,
                pady=12,
                command=lambda n=name: switch_tab(n),
            )
            btn.pack(fill=tk.X, pady=4)
            self.nav_buttons[name] = btn

        self.btn_save = tk.Button(
            self.sidebar,
            text="[ SAVE_CFG ]",
            font=("Consolas", 12, "bold"),
            bg=TH["accent"],
            fg="white",
            activebackground=TH["accent_hover"],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            pady=12,
            command=self._save_settings_clicked,
        )
        self.btn_save.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=24)

        switch_tab("General")

    def _add_field(self, parent_frame, label, key, row, is_str=False):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))
        tk.Entry(
            parent_frame,
            textvariable=var,
            font=("Consolas", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            insertbackground=TH["accent"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=TH["accent"],
            highlightbackground=TH["border"],
            width=14,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, is_str)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_combo(self, parent_frame, label, key, row, values):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, values[0])))
        ttk.Combobox(
            parent_frame,
            textvariable=var,
            values=values,
            font=("Consolas", 10),
            state="readonly",
            width=12,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_color_field(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))

        def choose_color(v=var):
            c = colorchooser.askcolor(initialcolor=v.get())[1]
            if c:
                v.set(c)
                btn.config(bg=c)

        btn = tk.Button(
            parent_frame,
            bg=var.get(),
            width=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_grid_chk(self, parent_frame, label, key, row):
        var = tk.BooleanVar(value=self.settings.get(key, True))
        tk.Checkbutton(
            parent_frame,
            text=label.upper(),
            variable=var,
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
            activeforeground=TH["accent"],
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=8)
        self.entries[key] = (var, "bool")
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_emoji_picker(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "🔥")))
        f = tk.Frame(parent_frame, bg=TH["bg"])
        f.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        lbl = tk.Label(
            f, textvariable=var, font=("Segoe UI Emoji", 12), bg=TH["bg"], fg=TH["fg"]
        )
        lbl.pack(side=tk.LEFT, padx=(0, 5))

        def _on_select(emoji):
            var.set(emoji)
            if key.startswith("toast_"):
                self._schedule_preview()

        def _open_picker():
            EmojiPickerPanel(self.window, _on_select)

        btn = tk.Button(
            f,
            text="Pick",
            font=("Consolas", 8),
            bg=TH["bg2"],
            fg=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=_open_picker,
        )
        btn.pack(side=tk.LEFT)
        self.entries[key] = (var, True)

    def _build_general_tab(self, tab):
        tk.Label(
            tab,
            text="THERMAL THRESHOLDS",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 20))
        f1 = tk.Frame(tab, bg=TH["bg"])
        f1.pack(fill=tk.X)
        self._add_field(f1, "Warning Temp (°C):", "warning_temp", 0)
        self._add_field(f1, "Critical Temp (°C):", "critical_temp", 1)

    def _build_toast_tab(self, tab):
        tk.Label(
            tab,
            text="UI / UX CONFIG",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 10))
        canvas = tk.Canvas(tab, bg=TH["bg"], highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg=TH["bg"])
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_mousewheel(event):
            try:
                w = event.widget.winfo_containing(event.x_root, event.y_root)
                while w:
                    if isinstance(w, tk.Canvas):
                        w.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        break
                    w = w.master
            except Exception:
                pass

        tab.winfo_toplevel().bind_all("<MouseWheel>", _on_mousewheel)

        f_top = tk.Frame(scrollable_frame, bg=TH["bg"])
        f_top.pack(fill=tk.BOTH, expand=True)
        f2_left = tk.Frame(f_top, bg=TH["bg"])
        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        f2_right = tk.Frame(f_top, bg=TH["bg"])
        f2_right.pack(side=tk.LEFT, fill=tk.Y)

        positions = [
            "Top-Left",
            "Top-Center",
            "Top-Right",
            "Bottom-Left",
            "Bottom-Center",
            "Bottom-Right",
            "Middle-Left",
            "Middle-Right",
            "Custom",
        ]
        animations = ["Slide", "Fade", "Bounce", "Scale", "Typewriter", "Glow", "Drop"]
        fonts = ["Segoe UI", "Consolas", "Cascadia Code", "Arial", "Verdana"]
        actions = ["dismiss", "snooze", "settings"]

        self._add_combo(f2_left, "Position:", "toast_pos", 0, positions)
        self._add_combo(f2_left, "Animation:", "toast_anim_style", 1, animations)
        self._add_field(f2_left, "Width (px):", "toast_width", 2)
        self._add_field(f2_left, "Height (px):", "toast_height", 3)
        self._add_field(f2_left, "Custom X (if custom):", "toast_custom_x", 4)
        self._add_field(f2_left, "Custom Y (if custom):", "toast_custom_y", 5)
        self._add_color_field(f2_left, "Background Color:", "toast_bg_color", 6)
        self._add_color_field(f2_left, "Text Color:", "toast_fg_color", 7)
        self._add_color_field(f2_left, "Accent Color:", "toast_accent_color", 8)
        self._add_combo(f2_left, "Font Family:", "toast_font_family", 9, fonts)
        self._add_field(f2_left, "Font Size:", "toast_font_size", 10)
        self._add_combo(
            f2_left, "Font Weight:", "toast_font_weight", 11, ["normal", "bold"]
        )
        self._add_combo(
            f2_left, "Text Align:", "toast_text_align", 12, ["left", "center", "right"]
        )

        self._add_emoji_picker(f2_right, "Emoji Icon:", "toast_emoji", 0)
        self._add_field(f2_right, "Border Radius (px):", "toast_radius", 1)
        self._add_field(f2_right, "Padding X (px):", "toast_padding_x", 2)
        self._add_field(f2_right, "Padding Y (px):", "toast_padding_y", 3)
        self._add_field(f2_right, "Opacity (0.1 - 1.0):", "toast_opacity", 4)
        self._add_field(f2_right, "Border Width (px):", "toast_border_width", 5)
        self._add_color_field(f2_right, "Border Color:", "toast_border_color", 6)
        self._add_color_field(f2_right, "Gradient End Color:", "toast_gradient_end", 7)
        self._add_combo(f2_right, "Click Action:", "toast_click_action", 8, actions)
        self._add_field(f2_right, "Duration (sec):", "toast_duration_sec", 9)
        self._add_field(f2_right, "Transition (ms):", "toast_transition_time_ms", 10)

        f3 = tk.Frame(scrollable_frame, bg=TH["bg"])
        f3.pack(fill=tk.X, pady=(15, 0))

        self._add_grid_chk(f3, "Enable Shadow/Glow", "toast_shadow", 0)
        self._add_grid_chk(f3, "Enable Gradient BG", "toast_gradient", 1)
        self._add_grid_chk(f3, "Enable Accent Stripe", "toast_accent_stripe", 2)
        self._add_grid_chk(f3, "Show Progress Bar", "toast_progress_bar", 3)
        self._add_grid_chk(f3, "Auto-Dismiss", "toast_auto_dismiss", 4)

        btn_frame = tk.Frame(scrollable_frame, bg=TH["bg"])
        btn_frame.pack(fill=tk.X, pady=20)
        tk.Button(
            btn_frame,
            text="[ PREVIEW_UI ]",
            font=("Consolas", 10, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
            activebackground=TH["bg3"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._preview_toast,
            padx=20,
            pady=8,
        ).pack(side=tk.RIGHT)

    def _schedule_preview(self):
        self._preview_toast(is_auto_edit=True)

    def _preview_toast(self, is_auto_edit=False):
        toast_exists = False
        if hasattr(self, "preview_instance") and self.preview_instance:
            if getattr(self.preview_instance, "toast_window", None) and self.preview_instance.toast_window.winfo_exists():
                toast_exists = True
            else:
                self.preview_instance = None

        temp_settings = dict(self.settings)
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    temp_settings[key] = float(val)
                elif var_type is False:
                    temp_settings[key] = int(val)
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        if is_auto_edit:
            temp_settings["toast_auto_dismiss"] = False
            temp_settings["toast_enable_sound"] = False

        if toast_exists:
            try:
                self.preview_instance.update_settings(temp_settings)
            except Exception:
                # Silently fail if updater isn't fully ready
                pass
        else:
            if hasattr(self, "preview_instance") and self.preview_instance:
                try:
                    self.preview_instance.force_close()
                except Exception:
                    pass
            self.preview_instance = BaseToast(
                self.window, "THERMAL PREVIEW", "Warning: 80°C reached", temp_settings
            )
            self.preview_instance.show()

    def _save_settings_clicked(self):
        if hasattr(self, "preview_instance") and self.preview_instance:
            try:
                self.preview_instance.force_close()
            except Exception:
                pass
            self.preview_instance = None

        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    self.settings[key] = float(val)
                elif var_type is False:
                    self.settings[key] = int(val)
                else:
                    self.settings[key] = val
            except ValueError:
                pass
        self.on_save(self.settings)

        self.btn_save.config(text="[ SAVED ]", state=tk.DISABLED)
        def reset_btn():
            try:
                self.btn_save.config(text="[ SAVE_CFG ]", state=tk.NORMAL)
            except Exception:
                pass
        self.window.after(2000, reset_btn)
```

---

### File: `touch_toggle/TouchToggle.ps1`
- **Path:** `touch_toggle/TouchToggle.ps1`
- **Estimated Tokens:** 323
- **mtime:** 1780159086.273

```powershell
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'

$logPath = "c:\Users\NANDHA A\Desktop\UTILITIES\Logs\touch_toggle_run.log"
"--- Run at $(Get-Date) ---" | Out-File $logPath -Append

try {
    $device = Get-PnpDevice -Class 'HIDClass' | Where-Object { $_.FriendlyName -match 'touch screen' } | Select-Object -First 1
    if (-not $device) {
        "  [ERROR] No HID-compliant touch screen device found!" | Out-File $logPath -Append
        exit 1
    }

    $instanceId = $device.InstanceId
    $currentStatus = $device.Status

    "Device: $($device.FriendlyName)" | Out-File $logPath -Append
    "ID: $instanceId" | Out-File $logPath -Append
    "Status: $currentStatus" | Out-File $logPath -Append

    if ($currentStatus -eq 'OK') {
        "Attempting to disable..." | Out-File $logPath -Append
        Disable-PnpDevice -InstanceId "$instanceId" -Confirm:$false
        "Disabled successfully." | Out-File $logPath -Append
    } else {
        "Attempting to enable..." | Out-File $logPath -Append
        Enable-PnpDevice -InstanceId "$instanceId" -Confirm:$false
        "Enabled successfully." | Out-File $logPath -Append
    }
} catch {
    "ERROR: $_" | Out-File $logPath -Append
    "ScriptStackTrace: $($_.ScriptStackTrace)" | Out-File $logPath -Append
    exit 1
}

```

---

### File: `touch_toggle/install_touch_toggle_service.ps1`
- **Path:** `touch_toggle/install_touch_toggle_service.ps1`
- **Estimated Tokens:** 202
- **mtime:** 1780923522.142

```powershell
param(
    [string]$TaskName = "TouchToggle Service"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $root "TouchToggle.ps1"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
    Write-Host "Installed scheduled task: $TaskName"
} catch {
    Write-Error "Failed to install TouchToggle service: $_"
    exit 1
}
```

---

### File: `touch_toggle/run_hidden.vbs`
- **Path:** `touch_toggle/run_hidden.vbs`
- **Estimated Tokens:** 39
- **mtime:** 1779500918.984

```
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & WScript.Arguments(0) & """", 0, True
```

---

### File: `touch_toggle/touch_settings.json`
- **Path:** `touch_toggle/touch_settings.json`
- **Estimated Tokens:** 219
- **mtime:** 1780554567.289

```json
{
    "toast_pos": "Bottom-Center",
    "toast_custom_x": 100,
    "toast_custom_y": 100,
    "toast_width": 200,
    "toast_height": 55,
    "toast_bg_color": "#000000",
    "toast_fg_color": "#FFFFFF",
    "toast_accent_color": "#ff8800",
    "toast_font_size": 10,
    "toast_font_weight": "normal",
    "toast_font_family": "Segoe UI",
    "toast_emoji": "\ud83d\udd90\ufe0f",
    "toast_radius": 18,
    "toast_padding_x": 12,
    "toast_padding_y": 10,
    "toast_anim_style": "Slide",
    "toast_opacity": 1.0,
    "toast_border_width": 0,
    "toast_border_color": "#000000",
    "toast_gradient": false,
    "toast_gradient_end": "#0a0a0a",
    "toast_shadow": true,
    "toast_accent_stripe": false,
    "toast_text_align": "left",
    "toast_auto_dismiss": true,
    "toast_click_action": "dismiss",
    "toast_progress_bar": false,
    "toast_enable_sound": false
}
```

---

### File: `touch_toggle/touch_toggle.py`
- **Path:** `touch_toggle/touch_toggle.py`
- **Estimated Tokens:** 7,206
- **mtime:** 1781288700.962

```python
# ruff: noqa: E402
"""
Touch Toggle — System Tray App
Provides a tray icon that shows touchscreen ON/OFF state.
Left-click toggles the touchscreen by running TouchToggle.ps1 elevated.
"""

import os
import sys
import subprocess
import threading
import logging
import logging.handlers
import json
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
import queue

ICON_SUPPORT = False
try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
    ICON_SUPPORT = True
except ImportError:
    pystray = None
    Image = None
    ImageDraw = None
    ImageFont = None

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOGGLES_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR = os.path.dirname(TOGGLES_DIR)
PS1_PATH = os.path.join(SCRIPT_DIR, "TouchToggle.ps1")
LOGS_DIR = os.path.join(PROJECT_DIR, "Logs")
LOG_PATH = os.path.join(LOGS_DIR, "touch_toggle.log")
# Allow importing from parent directory (AeroHub root)
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)
import services.aerohub_core.system_utils as system_utils
try:
    from services.aerohub_core.toast_utils import BaseToast, EmojiPickerPanel
except ImportError:
    pass

# ── Logging ──
os.makedirs(LOGS_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.TouchToggle")
except Exception:
    pass
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(
            LOG_PATH, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("TouchToggle")

# ── State ──
touch_enabled = True
tray_icon = None


# ── Settings ──
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "touch_settings.json")
DEFAULT_SETTINGS = {
    "toast_pos": "Center",
    "toast_custom_x": 100,
    "toast_custom_y": 100,
    "toast_width": 260,
    "toast_height": 60,
    "toast_bg_color": "#18181b",
    "toast_fg_color": "#ffffff",
    "toast_accent_color": "#ff8800",
    "toast_font_size": 11,
    "toast_font_weight": "bold",
    "toast_font_family": "Segoe UI",
    "toast_emoji": "🖐️",
    "toast_radius": 15,
    "toast_padding_x": 12,
    "toast_padding_y": 10,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.95,
    "toast_border_width": 1,
    "toast_border_color": "#27272a",
    "toast_gradient": False,
    "toast_gradient_end": "#0a0a0a",
    "toast_shadow": True,
    "toast_accent_stripe": False,
    "toast_text_align": "left",
    "toast_auto_dismiss": True,
    "toast_click_action": "dismiss",
    "toast_progress_bar": False,
    "toast_enable_sound": False,
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                saved = json.load(f)
                return {**DEFAULT_SETTINGS, **saved}
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
    return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        logger.info("Settings saved.")
    except Exception as e:
        logger.error(f"Error saving settings: {e}")


global_settings = load_settings()

TH = {
    "bg": "#0a0a0a",
    "bg2": "#171717",
    "bg3": "#262626",
    "fg": "#e5e5e5",
    "fg_dim": "#a3a3a3",
    "accent": "#ff8800",
    "border": "#333333",
}


def apply_dwm_rounding(window):
    try:
        import ctypes

        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        value = ctypes.c_int(2)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(value),
            ctypes.sizeof(value),
        )
    except Exception:
        pass


class SettingsWindow:
    def __init__(self, parent, settings, on_save):
        self.parent = parent
        self.settings = settings
        self.on_save = on_save
        self.entries = {}

    def show(self):
        root = tk.Toplevel(self.parent)
        root.title("Touch Toggle Config")
        root.geometry("600x500")
        root.configure(bg=TH["bg"])
        root.resizable(False, False)
        root.grab_set()

        try:
            apply_dwm_rounding(root)
        except Exception:
            pass

        try:
            from PIL import ImageTk
            icon_img = create_icon_image(touch_enabled)
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(False, self.icon_photo)
        except Exception as e:
            logger.error(f"Failed to set window icon: {e}")

        def on_closing():
            if (
                hasattr(self, "preview_instance")
                and self.preview_instance
                and hasattr(self.preview_instance, "force_close")
            ):
                self.preview_instance.force_close()
            root.grab_release()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        main_container = tk.Frame(root, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=180)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="TOUCH.SYS",
            font=("Consolas", 16, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
        ).pack(pady=(30, 40))

        self.btn_save = tk.Button(
            self.sidebar,
            text="[ SAVE_CFG ]",
            font=("Consolas", 12, "bold"),
            bg=TH["bg3"],
            fg=TH["accent"],
            activebackground=TH["bg"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._save_settings_clicked,
        )
        self.btn_save.pack(side=tk.BOTTOM, pady=20, padx=20, fill=tk.X)

        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20
        )

        canvas = tk.Canvas(self.content_area, bg=TH["bg"], highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg=TH["bg"])
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_mousewheel(event):
            try:
                w = event.widget.winfo_containing(event.x_root, event.y_root)
                while w:
                    if isinstance(w, tk.Canvas):
                        w.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        break
                    w = w.master
            except Exception:
                pass

        self.content_area.winfo_toplevel().bind_all("<MouseWheel>", _on_mousewheel)

        tk.Label(
            scrollable_frame,
            text="UI / UX CONFIG",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 10))

        f_top = tk.Frame(scrollable_frame, bg=TH["bg"])
        f_top.pack(fill=tk.BOTH, expand=True)
        f2_left = tk.Frame(f_top, bg=TH["bg"])
        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        f2_right = tk.Frame(f_top, bg=TH["bg"])
        f2_right.pack(side=tk.LEFT, fill=tk.Y)

        positions = [
            "Top-Left",
            "Top-Center",
            "Top-Right",
            "Bottom-Left",
            "Bottom-Center",
            "Bottom-Right",
            "Middle-Left",
            "Middle-Right",
            "Custom",
        ]
        animations = ["Slide", "Fade", "Bounce", "Scale", "Typewriter", "Glow", "Drop"]
        fonts = ["Segoe UI", "Consolas", "Cascadia Code", "Arial", "Verdana"]
        actions = ["dismiss", "snooze", "settings"]

        self._add_combo(f2_left, "Position:", "toast_pos", 0, positions)
        self._add_combo(f2_left, "Animation:", "toast_anim_style", 1, animations)
        self._add_field(f2_left, "Width (px):", "toast_width", 2)
        self._add_field(f2_left, "Height (px):", "toast_height", 3)
        self._add_color_field(f2_left, "Background:", "toast_bg_color", 4)
        self._add_color_field(f2_left, "Text Color:", "toast_fg_color", 5)
        self._add_field(f2_left, "Font Size:", "toast_font_size", 6)
        self._add_combo(
            f2_left, "Font Weight:", "toast_font_weight", 7, ["normal", "bold"]
        )
        self._add_combo(f2_left, "Font Family:", "toast_font_family", 8, fonts)
        self._add_color_field(f2_left, "Accent Color:", "toast_accent_color", 9)
        self._add_field(f2_left, "Custom X:", "toast_custom_x", 10)
        self._add_field(f2_left, "Custom Y:", "toast_custom_y", 11)

        self._add_emoji_picker(f2_right, "Emoji Icon:", "toast_emoji", 0)
        self._add_field(f2_right, "Radius (px):", "toast_radius", 1)
        self._add_field(f2_right, "Padding X:", "toast_padding_x", 2)
        self._add_field(f2_right, "Padding Y:", "toast_padding_y", 3)
        self._add_field(f2_right, "Opacity:", "toast_opacity", 4)
        self._add_field(f2_right, "Border Width:", "toast_border_width", 5)
        self._add_color_field(f2_right, "Border Color:", "toast_border_color", 6)
        self._add_color_field(f2_right, "Gradient End:", "toast_gradient_end", 7)
        self._add_combo(
            f2_right, "Text Align:", "toast_text_align", 8, ["left", "center", "right"]
        )
        self._add_combo(f2_right, "Click Action:", "toast_click_action", 9, actions)
        self._add_field(f2_right, "Duration (sec):", "toast_duration_sec", 10)
        self._add_field(f2_right, "Transition (ms):", "toast_transition_time_ms", 11)

        f3 = tk.Frame(scrollable_frame, bg=TH["bg"])
        f3.pack(fill=tk.X, pady=(15, 0))
        self._add_grid_chk(f3, "Enable Shadow/Glow", "toast_shadow", 0)
        self._add_grid_chk(f3, "Enable Gradient BG", "toast_gradient", 1)
        self._add_grid_chk(f3, "Enable Accent Stripe", "toast_accent_stripe", 2)
        self._add_grid_chk(f3, "Show Progress Bar", "toast_progress_bar", 3)
        self._add_grid_chk(f3, "Auto-Dismiss", "toast_auto_dismiss", 4)

        btn_frame = tk.Frame(scrollable_frame, bg=TH["bg"])
        btn_frame.pack(fill=tk.X, pady=20)

        tk.Button(
            btn_frame,
            text="[ PREVIEW_UI ]",
            font=("Consolas", 10, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
            activebackground=TH["bg3"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._preview_toast,
            padx=20,
            pady=8,
        ).pack(side=tk.RIGHT)

    def _add_field(self, parent_frame, label, key, row, is_str=False):
        tk.Label(
            parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))
        tk.Entry(
            parent_frame,
            textvariable=var,
            font=("Consolas", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            insertbackground=TH["accent"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=TH["accent"],
            highlightbackground=TH["border"],
            width=10,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, is_str)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_combo(self, parent_frame, label, key, row, values):
        tk.Label(
            parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=self.settings.get(key, values[0]))
        ttk.Combobox(
            parent_frame,
            textvariable=var,
            values=values,
            font=("Consolas", 10),
            state="readonly",
            width=8,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_color_field(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=self.settings.get(key, "#ffffff"))

        def choose_color(v=var):
            color_code = colorchooser.askcolor(
                title="Choose color", initialcolor=v.get()
            )[1]
            if color_code:
                v.set(color_code)
                btn.config(bg=color_code)

        btn = tk.Button(
            parent_frame,
            bg=var.get(),
            width=6,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_grid_chk(self, parent_frame, label, key, row):
        var = tk.BooleanVar(value=self.settings.get(key, True))
        tk.Checkbutton(
            parent_frame,
            text=label.upper(),
            variable=var,
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
            activeforeground=TH["accent"],
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=8)
        self.entries[key] = (var, "bool")
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_emoji_picker(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "🖐️")))
        f = tk.Frame(parent_frame, bg=TH["bg"])
        f.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        lbl = tk.Label(
            f, textvariable=var, font=("Segoe UI Emoji", 12), bg=TH["bg"], fg=TH["fg"]
        )
        lbl.pack(side=tk.LEFT, padx=(0, 5))

        def _on_select(emoji):
            var.set(emoji)
            self._schedule_preview()

        def _open_picker():
            EmojiPickerPanel(self.parent, _on_select)

        btn = tk.Button(
            f,
            text="Pick",
            font=("Consolas", 8),
            bg=TH["bg2"],
            fg=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=_open_picker,
        )
        btn.pack(side=tk.LEFT)
        self.entries[key] = (var, True)

    def _schedule_preview(self):
        self._preview_toast(is_auto_edit=True)

    def _preview_toast(self, is_auto_edit=False):
        toast_exists = False
        if hasattr(self, "preview_instance") and self.preview_instance:
            if getattr(self.preview_instance, "toast_window", None) and self.preview_instance.toast_window.winfo_exists():
                toast_exists = True
            else:
                self.preview_instance = None

        temp_settings = dict(self.settings)
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    temp_settings[key] = float(val)
                elif not var_type:
                    temp_settings[key] = int(val)
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        if is_auto_edit:
            temp_settings["toast_auto_dismiss"] = False
            temp_settings["toast_enable_sound"] = False

        if toast_exists:
            try:
                self.preview_instance.update_settings(temp_settings)
            except Exception as e:
                logger.error(f"Error updating preview in-place: {e}")
        else:
            if hasattr(self, "preview_instance") and self.preview_instance:
                try:
                    self.preview_instance.force_close()
                except Exception:
                    pass
            self.preview_instance = BaseToast(
                self.parent, "TOUCH PREVIEW", "Preview Toast", temp_settings
            )
            self.preview_instance.show()

    def _save_settings_clicked(self):
        if hasattr(self, "preview_instance") and self.preview_instance:
            try:
                self.preview_instance.force_close()
            except Exception:
                pass
            self.preview_instance = None

        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    self.settings[key] = float(val)
                elif not var_type:
                    self.settings[key] = int(val)
                else:
                    self.settings[key] = val
            except ValueError:
                pass
        save_settings(self.settings)
        self.on_save(self.settings)

        self.btn_save.config(text="[ SAVED ]", state=tk.DISABLED)
        def reset_btn():
            try:
                self.btn_save.config(text="[ SAVE_CFG ]", state=tk.NORMAL)
            except Exception:
                pass
        self.parent.after(2000, reset_btn)


def create_icon_image(enabled: bool) -> Image.Image:
    """Draw a tray icon showing touch ON (green) or OFF (red)."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle
    color = (50, 205, 50, 255) if enabled else (255, 0, 0, 255)  # LimeGreen / Red
    draw.ellipse([4, 4, size - 4, size - 4], fill=color)

    # Draw "T" for Touch
    try:
        font = ImageFont.truetype("arialbd.ttf", 36)
    except IOError:
        font = ImageFont.load_default()

    text = "T"
    # Get bounding box to center the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Adjust for visual center
    x = (size - text_w) / 2
    y = (size - text_h) / 2 - 4

    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

    return img


gui_queue = queue.Queue()
tk_root = None


def _process_gui_queue_loop():
    while not gui_queue.empty():
        try:
            action = gui_queue.get_nowait()
            if action == "settings":

                def on_saved(new_settings):
                    global global_settings
                    global_settings = new_settings

                SettingsWindow(tk_root, dict(global_settings), on_saved).show()
            elif isinstance(action, dict) and action.get("type") == "toast":
                temp_settings = dict(global_settings)
                state = action.get("state", "on")
                if state == "off":
                    temp_settings["toast_accent_color"] = "#ff3b30"
                    temp_settings["toast_emoji"] = "🚫"
                else:
                    temp_settings["toast_accent_color"] = "#34c759"
                    temp_settings["toast_emoji"] = "🖐️"
                BaseToast(tk_root, action["title"], action["msg"], temp_settings).show()
        except Exception as e:
            logger.error(f"Error processing GUI queue: {e}")
    tk_root.after(100, _process_gui_queue_loop)


def open_settings(icon, item):
    gui_queue.put("settings")


def check_touch_state() -> bool:
    """Check if the HID touch screen is currently enabled."""
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                (
                    "Get-PnpDevice -Class 'HIDClass' | Where-Object FriendlyName -match 'touch screen' "
                    "| Select-Object -ExpandProperty Status"
                ),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        status = result.stdout.strip().lower()
        logger.info(f"Touch screen status query result: '{status}'")
        return status == "ok"
    except Exception as e:
        logger.error(f"Failed to check touch state: {e}")
        return True  # Assume enabled on error


class SHELLEXECUTEINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("fMask", ctypes.c_ulong),
        ("hwnd", ctypes.c_void_p),
        ("lpVerb", ctypes.c_wchar_p),
        ("lpFile", ctypes.c_wchar_p),
        ("lpParameters", ctypes.c_wchar_p),
        ("lpDirectory", ctypes.c_wchar_p),
        ("nShow", ctypes.c_int),
        ("hInstApp", ctypes.c_void_p),
        ("lpIDList", ctypes.c_void_p),
        ("lpClass", ctypes.c_wchar_p),
        ("hkeyClass", ctypes.c_void_p),
        ("dwHotKey", ctypes.c_ulong),
        ("hIconOrMonitor", ctypes.c_void_p),
        ("hProcess", ctypes.c_void_p),
    ]


def show_tooltip(text, state):
    """Show a custom floating tooltip notification via gui_queue and BaseToast."""
    gui_queue.put(
        {"type": "toast", "title": "Touch Screen", "msg": text, "state": state}
    )


def toggle_touch():
    """Run the PowerShell toggle script elevated via ShellExecuteExW (runas)."""
    global touch_enabled
    logger.info("Toggling touch screen...")

    # Path to the log file written by PS1
    ps1_log_path = os.path.join(LOGS_DIR, "touch_toggle_run.log")

    # Clean previous run log if exists
    if os.path.exists(ps1_log_path):
        try:
            os.remove(ps1_log_path)
        except Exception as e:
            logger.warning(f"Could not remove old PS1 log: {e}")

    try:
        if not os.path.exists(PS1_PATH):
            logger.error(f"PowerShell script not found: {PS1_PATH}")
            return

        is_admin = False
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            pass

        if is_admin:
            logger.info(
                f"Already running as admin. Executing PowerShell script directly: {PS1_PATH}"
            )
            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-WindowStyle",
                    "Hidden",
                    "-File",
                    PS1_PATH,
                ],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            logger.info("Direct PowerShell script execution completed.")
        else:
            logger.info(
                f"Not running as admin. Executing elevated PowerShell script via ShellExecuteExW: {PS1_PATH}"
            )

            # Use ShellExecuteExW with 'runas' verb for proper UAC elevation
            params = f'-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "{PS1_PATH}"'

            sei = SHELLEXECUTEINFO()
            sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
            sei.fMask = 0x00000040  # SEE_MASK_NOCLOSEPROCESS
            sei.hwnd = None
            sei.lpVerb = "runas"
            sei.lpFile = "powershell.exe"
            sei.lpParameters = params
            sei.lpDirectory = None
            sei.nShow = 0  # SW_HIDE

            if not ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei)):
                error_code = ctypes.GetLastError()
                logger.error(f"ShellExecuteExW failed with error code: {error_code}")
                return

            # Wait for the elevated process to finish using hProcess handle
            if sei.hProcess:
                logger.info("Waiting for elevated PowerShell process to complete...")
                INFINITE = 0xFFFFFFFF
                ctypes.windll.kernel32.WaitForSingleObject(
                    ctypes.c_void_p(sei.hProcess), INFINITE
                )
                ctypes.windll.kernel32.CloseHandle(ctypes.c_void_p(sei.hProcess))
            else:
                # Fallback: wait a bit for the script to run
                import time

                time.sleep(3)

            logger.info("Elevated PowerShell script execution completed.")

        # Check and log touch_toggle_run.log contents
        if os.path.exists(ps1_log_path):
            try:
                with open(ps1_log_path, "r", encoding="utf-16le") as f:
                    log_content = f.read()
                logger.info(
                    f"--- PS1 Log Output ---\n{log_content}----------------------"
                )
            except Exception as e1:
                try:
                    with open(ps1_log_path, "r", encoding="utf-8") as f:
                        log_content = f.read()
                    logger.info(
                        f"--- PS1 Log Output (UTF-8 fallback) ---\n{log_content}----------------------"
                    )
                except Exception as e2:
                    logger.error(f"Failed to read PS1 log file: {e1} / {e2}")
        else:
            logger.warning(f"touch_toggle_run.log not found at: {ps1_log_path}")

        # Re-check state
        touch_enabled = check_touch_state()
        logger.info(
            f"Touch screen is now: {'ENABLED' if touch_enabled else 'DISABLED'}"
        )

        # Update icon
        if tray_icon:
            tray_icon.icon = create_icon_image(touch_enabled)
            state_str = "ON" if touch_enabled else "OFF"
            tray_icon.title = f"Touch: {state_str}"
            tray_icon.menu = create_menu()

            # Show tooltip notification
            show_tooltip(
                f"Touch Screen is now {state_str}", "on" if touch_enabled else "off"
            )

    except Exception as e:
        logger.error(f"Toggle failed: {e}")


def on_toggle(icon, item):
    """Menu callback for toggle action."""
    threading.Thread(target=toggle_touch, daemon=True).start()


def on_quit(icon, item):
    """Quit the tray app."""
    logger.info("Quitting Touch Toggle tray app.")
    icon.stop()
    if tk_root:
        tk_root.quit()


def on_click(icon, item):
    """Left-click handler — toggle touchscreen."""
    threading.Thread(target=toggle_touch, daemon=True).start()


def create_menu():
    """Create the tray context menu."""
    state_text = f"Touch: {'ON ✓' if touch_enabled else 'OFF ✗'}"
    return pystray.Menu(
        pystray.MenuItem(state_text, None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Toggle Touch Screen", on_toggle, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Settings", open_settings),
        pystray.MenuItem("Quit", on_quit),
    )


def main():
    global touch_enabled, tray_icon

    if not ICON_SUPPORT:
        logger.error(
            "TouchToggle requires pystray and Pillow. Install dependencies from requirements.txt and retry."
        )
        sys.exit(1)

    logger.info("=" * 50)
    logger.info("Touch Toggle Tray App starting...")

    # Check initial state
    touch_enabled = check_touch_state()
    logger.info(f"Initial touch state: {'ENABLED' if touch_enabled else 'DISABLED'}")

    # Create tray icon
    icon_image = create_icon_image(touch_enabled)
    tray_icon = pystray.Icon(
        name="TouchToggle",
        icon=icon_image,
        title=f"Touch: {'ON' if touch_enabled else 'OFF'}",
        menu=create_menu(),
    )

    logger.info("Tray icon created. Running...")

    global tk_root
    tk_root = tk.Tk()
    tk_root.withdraw()

    icon_thread = threading.Thread(target=tray_icon.run, daemon=True)
    icon_thread.start()

    # Start parent process monitoring
    system_utils.monitor_parent_process(lambda: on_quit(tray_icon, None))

    tk_root.after(100, _process_gui_queue_loop)
    tk_root.mainloop()


if __name__ == "__main__":
    main()
```

---

### File: `touch_toggle/uninstall_touch_toggle_service.ps1`
- **Path:** `touch_toggle/uninstall_touch_toggle_service.ps1`
- **Estimated Tokens:** 108
- **mtime:** 1780923522.142

```powershell
param(
    [string]$TaskName = "TouchToggle Service"
)

try {
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "Uninstalled scheduled task: $TaskName"
    } else {
        Write-Warning "Scheduled task '$TaskName' not found."
    }
} catch {
    Write-Error "Failed to uninstall TouchToggle service: $_"
    exit 1
}
```

---

