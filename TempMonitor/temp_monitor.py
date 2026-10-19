"""
TempMonitor — Cross-platform CPU/GPU thermal monitoring with tray icon.

Displays current temperature as a number on a color-coded tray icon.
Green < 60°C, Yellow < 75°C, Orange < 85°C, Red ≥ 85°C.

Backends:
- Linux: psutil.sensors_temperatures() (/sys/class/hwmon & thermal_zone)
- Windows: LibreHardwareMonitor (.NET DLL via pythonnet) -> WMI fallback

Features:
- Auto-select hottest component mode
- Thermal history ring buffer for sparklines
- Overheat warning & critical toast alerts

Usage:
    python TempMonitor/temp_monitor.py
"""

import collections
import os
import sys
import time
import threading

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import psutil
import pystray
from PIL import Image, ImageDraw, ImageFont

from common.logger import get_logger
from common.settings import load_settings, save_settings
from common.singleton import acquire_mutex
from common.toast import show_toast
from common.tray import set_appusermodelid

log = get_logger("TempMonitor")

_SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

_DEFAULTS = {
    "warning_temp": 75,
    "critical_temp": 85,
    "poll_interval_sec": 3,
    "selected_sensor": "auto_hottest",
    "alert_cooldown_sec": 120,
    "auto_hottest": True,
    "autostart": True,
    "adaptive_polling": True,
}

# ── State ──
settings: dict = {}
_all_temps: dict[str, float] = {}
_temp_history: dict[str, collections.deque] = collections.defaultdict(lambda: collections.deque(maxlen=30))
_display_temp: float = 0.0
_display_sensor: str = ""
_backend: str = "none"
_icon_ref: pystray.Icon | None = None
_stop_event = threading.Event()
_alert_state: str = "NORMAL"
_last_alert_time: float = 0


# ── Power & Fast Sysfs Subsystems ──

class FastSysfsReader:
    """Pre-cached file descriptor reader for Linux sysfs hwmon nodes.
    Eliminates directory traversal and inode lookups for microsecond reads."""
    def __init__(self):
        self._sensors: list[tuple[str, int]] = []
        self._initialized = False

    def init_sensors(self) -> None:
        self.close()
        import glob
        sensors = []
        for p in sorted(glob.glob("/sys/class/hwmon/hwmon*/temp*_input")):
            try:
                name_path = os.path.join(os.path.dirname(p), "name")
                chip_name = open(name_path).read().strip() if os.path.exists(name_path) else "hwmon"
                label_path = p.replace("_input", "_label")
                label = open(label_path).read().strip() if os.path.exists(label_path) else os.path.basename(p)
                name = f"{chip_name} ({label})" if label else chip_name
                fd = os.open(p, os.O_RDONLY)
                sensors.append((name, fd))
            except Exception:
                pass
        self._sensors = sensors
        self._initialized = len(sensors) > 0

    def read(self) -> dict[str, float]:
        if not self._initialized:
            self.init_sensors()
        if not self._sensors:
            return {}

        temps = {}
        for name, fd in self._sensors:
            try:
                os.lseek(fd, 0, os.SEEK_SET)
                raw = os.read(fd, 16)
                if raw:
                    millideg = int(raw.strip())
                    if millideg > 0:
                        temps[name] = round(millideg / 1000.0, 1)
            except Exception:
                pass
        return temps

    def close(self) -> None:
        for _, fd in self._sensors:
            try:
                os.close(fd)
            except Exception:
                pass
        self._sensors = []
        self._initialized = False


class AdaptivePowerManager:
    """Detects power delivery state (AC vs Battery) and session idle time."""
    @staticmethod
    def is_on_battery() -> bool:
        ac_path = "/sys/class/power_supply/AC/online"
        if os.path.exists(ac_path):
            try:
                with open(ac_path) as f:
                    return f.read().strip() == "0"
            except Exception:
                pass
        try:
            bat = psutil.sensors_battery()
            if bat is not None:
                return not bat.power_plugged
        except Exception:
            pass
        return False

    @staticmethod
    def get_idle_seconds() -> float:
        try:
            import subprocess
            out = subprocess.check_output(["xprintidle"], stderr=subprocess.DEVNULL)
            return int(out.strip()) / 1000.0
        except Exception:
            return 0.0


def _compute_adaptive_interval(
    temp: float,
    last_temp: float,
    dt: float,
    warning_temp: float = 75.0,
    critical_temp: float = 85.0,
    is_battery: bool = False,
    is_idle: bool = False,
) -> float:
    """Dynamically scales polling frequency with thermal acceleration, risk brackets, and power state."""
    if is_idle and temp < warning_temp:
        return 20.0

    gradient = (temp - last_temp) / max(dt, 0.1) if dt > 0 else 0.0

    if temp >= critical_temp:
        return 1.0
    if temp >= warning_temp or gradient >= 1.5:
        return 1.5
    if temp >= 60.0:
        return 3.5 if not is_battery else 5.5

    return 6.0 if not is_battery else 12.0


_fast_sysfs = FastSysfsReader()


# ── Linux Temperature Reader ──

def _read_linux_temps() -> dict[str, float]:
    """Read temperatures via psutil from /sys/class/thermal and /sys/class/hwmon."""
    temps = {}
    try:
        sensor_data = psutil.sensors_temperatures()
        if not sensor_data:
            return temps

        for chip_name, entries in sensor_data.items():
            for entry in entries:
                label = entry.label or chip_name
                # Clean up sensor name
                name = f"{chip_name} ({label})" if entry.label else chip_name
                if entry.current is not None and entry.current > 0:
                    temps[name] = round(entry.current, 1)
    except Exception:
        pass
    return temps


# ── Windows Temperature Reader ──

def _read_windows_temps() -> dict[str, float]:
    try:
        from TempMonitor.lhm_reader import read_temperatures as lhm_read, is_available as lhm_available
        if lhm_available():
            t = lhm_read()
            if t:
                return t
    except Exception:
        pass

    try:
        from TempMonitor.wmi_reader import read_temperatures as wmi_read
        t = wmi_read()
        if t:
            return t
    except Exception:
        pass

    return {}


# ── Unified Reading ──

def _read_temps() -> dict[str, float]:
    global _backend
    if sys.platform.startswith("linux"):
        # Fast path: pre-cached direct sysfs descriptors
        t = _fast_sysfs.read()
        if t:
            _backend = "sysfs/fast"
            return t
        t = _read_linux_temps()
        if t:
            _backend = "sysfs/psutil"
            return t
    elif sys.platform == "win32":
        t = _read_windows_temps()
        if t:
            _backend = "lhm/wmi"
            return t

    # Fallback to psutil generally
    try:
        t = _read_linux_temps()
        if t:
            _backend = "psutil"
            return t
    except Exception:
        pass

    _backend = "none"
    return {}


def _pick_display_sensor(temps: dict[str, float], selected: str | None) -> tuple[str, float]:
    """Choose sensor: either user-selected or auto-hottest."""
    if not temps:
        return "N/A", 0.0

    if selected and selected != "auto_hottest" and selected in temps:
        return selected, temps[selected]

    if settings.get("auto_hottest", True) or selected == "auto_hottest":
        # Find maximum temperature sensor
        hottest_sensor = max(temps.items(), key=lambda x: x[1])
        return hottest_sensor[0], hottest_sensor[1]

    # Priority: CPU > GPU > first available
    for keyword in ["CPU Package", "Package id 0", "Core 0", "CPU", "GPU", "composite"]:
        for name, val in temps.items():
            if keyword.lower() in name.lower():
                return name, val

    name = next(iter(temps))
    return name, temps[name]


# ── Tray Icon Drawing ──

def _temp_color(temp: float) -> tuple[int, int, int]:
    if temp < 60:
        return (16, 185, 129)   # Vibrant Emerald Green
    elif temp < 75:
        return (245, 158, 11)   # Vibrant Amber
    elif temp < 85:
        return (249, 115, 22)   # Vibrant Orange
    else:
        return (239, 68, 68)    # Vibrant Red


def _draw_icon(temp: float) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    color = _temp_color(temp)

    # Rounded rectangle background
    draw.rounded_rectangle([2, 2, size - 2, size - 2], radius=14, fill=color)

    text = str(int(temp)) if temp > 0 else "--"
    font_family = "DejaVuSans-Bold.ttf" if sys.platform != "win32" else "segoeui.ttf"
    try:
        font_size = 28 if len(text) <= 2 else 22
        font = ImageFont.truetype(font_family, font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((size - tw) // 2, (size - th) // 2 - 2),
        text, fill=(255, 255, 255), font=font,
    )

    # Small ° mark
    try:
        small_font = ImageFont.truetype(font_family, 12)
    except OSError:
        small_font = ImageFont.load_default()
    draw.text(
        ((size + tw) // 2 + 1, (size - th) // 2 - 4),
        "°", fill=(255, 255, 255, 200), font=small_font,
    )

    return img


# ── Tooltip ──

def _build_tooltip(on_battery: bool = False) -> str:
    if not _all_temps:
        return "TempMonitor — No sensors detected"

    pwr_mode = "🔋 Battery" if on_battery else "⚡ AC Power"
    adapt_mode = "Adaptive" if settings.get("adaptive_polling", True) else "Fixed"
    lines = [f"TempMonitor ({_backend.upper()} • {pwr_mode} • {adapt_mode})"]
    for name, val in sorted(_all_temps.items()):
        marker = " ◄" if name == _display_sensor else ""
        lines.append(f"  {name}: {val:.0f}°C{marker}")
    return "\n".join(lines)


# ── Alerts State Machine with Hysteresis ──

def _check_alerts(temp: float, sensor_name: str) -> None:
    """Alert state machine: notifies once on threshold crossing; suppresses repeats until CPU cools down."""
    global _alert_state, _last_alert_time
    now = time.time()
    warning_temp = settings.get("warning_temp", 75)
    critical_temp = settings.get("critical_temp", 85)
    # 5°C hysteresis margin: must cool below (warning - 5°C) before resetting to NORMAL
    reset_temp = warning_temp - 5.0

    if temp >= critical_temp:
        # Alert once on entering CRITICAL
        if _alert_state != "CRITICAL":
            log.warning(f"CRITICAL: {sensor_name} at {temp:.0f}°C")
            show_toast(
                "TempMonitor",
                "Critical Temperature!",
                f"{sensor_name} — High thermal throttling risk",
                icon_text="🔥",
                accent_color="#dc2626",
                temp_level=f"{temp:.0f}°C",
                style="dynamic_island",
                duration_sec=0,
                sound=True,
            )
            _alert_state = "CRITICAL"
            _last_alert_time = now

    elif temp >= warning_temp:
        # Alert once on entering WARNING from NORMAL.
        # If cooling down from CRITICAL, transition silently without double-firing warning toast.
        if _alert_state == "NORMAL":
            log.info(f"WARNING: {sensor_name} at {temp:.0f}°C")
            show_toast(
                "TempMonitor",
                "High Temperature Warning",
                f"{sensor_name}",
                icon_text="🔥",
                accent_color="#ef4444",
                temp_level=f"{temp:.0f}°C",
                style="dynamic_island",
                duration_sec=4,
                sound=False,
            )
            _alert_state = "WARNING"
            _last_alert_time = now
        elif _alert_state == "CRITICAL":
            _alert_state = "WARNING"

    elif temp < reset_temp:
        # Reset state only after CPU has cooled down sufficiently
        if _alert_state != "NORMAL":
            log.debug(f"Temperature normalized to {temp:.0f}°C (< {reset_temp:.0f}°C). Reset alert state.")
            _alert_state = "NORMAL" 


# ── Polling Loop ──

def _poll_loop() -> None:
    global _all_temps, _display_temp, _display_sensor

    last_temp = 0.0
    last_time = time.time()
    last_rendered_int_temp = -1
    last_rendered_color = None

    while not _stop_event.is_set():
        loop_start = time.time()
        temps = _read_temps()
        _all_temps = temps

        # Update history
        for name, val in temps.items():
            _temp_history[name].append(val)

        sensor, temp = _pick_display_sensor(temps, settings.get("selected_sensor"))
        _display_temp = temp
        _display_sensor = sensor

        # Query power and idle states
        on_battery = AdaptivePowerManager.is_on_battery()
        idle_sec = AdaptivePowerManager.get_idle_seconds()
        is_idle = idle_sec > 300.0  # 5 minutes idle or screen sleep

        # Smart icon redraw: dirty-check avoids redundant redraws
        curr_int_temp = int(round(temp)) if temp > 0 else 0
        curr_color = _temp_color(temp) if temp > 0 else None
        should_render = (curr_int_temp != last_rendered_int_temp or curr_color != last_rendered_color)

        if _icon_ref:
            try:
                if should_render or not is_idle:
                    _icon_ref.icon = _draw_icon(temp)
                    last_rendered_int_temp = curr_int_temp
                    last_rendered_color = curr_color
                _icon_ref.title = _build_tooltip(on_battery=on_battery)
            except Exception:
                pass

        if temp > 0:
            _check_alerts(temp, sensor)

        # Compute next sleep interval
        dt = loop_start - last_time
        if settings.get("adaptive_polling", True):
            next_interval = _compute_adaptive_interval(
                temp=temp,
                last_temp=last_temp,
                dt=dt,
                warning_temp=settings.get("warning_temp", 75),
                critical_temp=settings.get("critical_temp", 85),
                is_battery=on_battery,
                is_idle=is_idle,
            )
        else:
            next_interval = settings.get("poll_interval_sec", 3)

        last_temp = temp
        last_time = loop_start

        _stop_event.wait(next_interval)


# ── Menu & Settings ──

def _build_sensor_menu() -> list:
    items = []

    def _select_auto(_, __=None):
        settings["selected_sensor"] = "auto_hottest"
        settings["auto_hottest"] = True
        save_settings(_SETTINGS_PATH, settings)

    items.append(pystray.MenuItem("🔥 Auto (Hottest Sensor)", _select_auto, checked=lambda _: settings.get("selected_sensor") == "auto_hottest"))
    items.append(pystray.Menu.SEPARATOR)

    for name in sorted(_all_temps.keys()):
        def _select(_, sensor_name=name):
            settings["selected_sensor"] = sensor_name
            settings["auto_hottest"] = False
            save_settings(_SETTINGS_PATH, settings)

        items.append(pystray.MenuItem(name, _select, checked=lambda _, n=name: n == _display_sensor and not settings.get("auto_hottest", False)))
    return items


def _on_settings(_icon=None, _=None):
    try:
        from TempMonitor.settings_gui import open_settings
        open_settings(settings, _all_temps, _temp_history, on_save=lambda s: settings.update(s))
    except Exception as e:
        log.error(f"Failed to open settings: {e}")


def _on_exit(icon, _=None):
    log.info("Shutting down TempMonitor...")
    _stop_event.set()
    _fast_sysfs.close()
    icon.stop()


# ── OS Autostart Management ──

def is_autostart_enabled() -> bool:
    """Check if TempMonitor is configured to start on OS boot."""
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_READ,
            )
            val, _ = winreg.QueryValueEx(key, "TempMonitor")
            winreg.CloseKey(key)
            return bool(val)
        except Exception:
            return False
    else:
        # Linux XDG autostart
        desktop_file = os.path.expanduser("~/.config/autostart/temp_monitor.desktop")
        return os.path.exists(desktop_file)


def set_autostart(enabled: bool) -> bool:
    """Enable or disable TempMonitor startup on OS boot."""
    global settings
    if not settings:
        settings = load_settings(_SETTINGS_PATH, _DEFAULTS)

    script_path = os.path.abspath(__file__)
    py_exec = sys.executable

    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE,
            )
            if enabled:
                pythonw = py_exec.replace("python.exe", "pythonw.exe")
                cmd = f'"{pythonw}" -B "{script_path}"'
                winreg.SetValueEx(key, "TempMonitor", 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, "TempMonitor")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
            settings["autostart"] = enabled
            save_settings(_SETTINGS_PATH, settings)
            return True
        except Exception as e:
            log.error(f"Failed to set Windows autostart: {e}")
            return False
    else:
        # Linux XDG autostart
        try:
            autostart_dir = os.path.expanduser("~/.config/autostart")
            os.makedirs(autostart_dir, exist_ok=True)
            desktop_file = os.path.join(autostart_dir, "temp_monitor.desktop")

            if enabled:
                content = f"""[Desktop Entry]
Type=Application
Exec={py_exec} -B {script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=AeroHub TempMonitor
Comment=CPU/GPU Thermal Tray Monitor
Icon=utilities-system-monitor
"""
                with open(desktop_file, "w", encoding="utf-8") as f:
                    f.write(content)
            else:
                if os.path.exists(desktop_file):
                    os.remove(desktop_file)
            settings["autostart"] = enabled
            save_settings(_SETTINGS_PATH, settings)
            return True
        except Exception as e:
            log.error(f"Failed to set Linux autostart: {e}")
            return False


def _build_menu():
    sensor_items = _build_sensor_menu()
    sensor_submenu = pystray.Menu(*sensor_items) if sensor_items else pystray.Menu(
        pystray.MenuItem("No sensors detected", None, enabled=False)
    )

    def _toggle_autostart(_icon=None, _item=None):
        new_state = not is_autostart_enabled()
        set_autostart(new_state)

    def _toggle_adaptive(_icon=None, _item=None):
        new_state = not settings.get("adaptive_polling", True)
        settings["adaptive_polling"] = new_state
        save_settings(_SETTINGS_PATH, settings)

    on_bat = AdaptivePowerManager.is_on_battery()
    power_label = "🔋 Power: Battery (Power Saver)" if on_bat else "⚡ Power: AC (High Performance)"

    return pystray.Menu(
        pystray.MenuItem(f"Backend: {_backend.upper()}", None, enabled=False),
        pystray.MenuItem(power_label, None, enabled=False),
        pystray.MenuItem("⚡ Adaptive Power Efficiency", _toggle_adaptive, checked=lambda _: settings.get("adaptive_polling", True)),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Target Sensor", sensor_submenu),
        pystray.MenuItem("⚙ Thermal Settings", _on_settings),
        pystray.MenuItem("🚀 Launch on Startup", _toggle_autostart, checked=lambda _: is_autostart_enabled()),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Exit", _on_exit),
    )


# ── Main ──

def main():
    global settings, _icon_ref

    if not acquire_mutex("AeroHub_TempMonitor_Mutex"):
        print("TempMonitor is already running.")
        sys.exit(0)

    set_appusermodelid("AeroHub.TempMonitor")
    log.info(f"TempMonitor starting on {sys.platform}...")

    settings = load_settings(_SETTINGS_PATH, _DEFAULTS)

    # Sync autostart on launch
    if settings.get("autostart", True) and not is_autostart_enabled():
        set_autostart(True)

    temps = _read_temps()
    log.info(f"Backend: {_backend}, sensors detected: {len(temps)}")

    poll_thread = threading.Thread(target=_poll_loop, daemon=True)
    poll_thread.start()

    initial_icon = _draw_icon(_display_temp)
    icon = pystray.Icon(
        "TempMonitor",
        initial_icon,
        _build_tooltip(),
        menu=_build_menu(),
    )
    _icon_ref = icon

    log.info("TempMonitor ready.")
    icon.run()


if __name__ == "__main__":
    main()

