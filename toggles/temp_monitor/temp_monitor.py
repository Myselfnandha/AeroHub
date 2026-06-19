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
            "toast_enable_sound": True,
            "toast_sound_effect": "mac_connect",
            "toast_volume": 80,
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
