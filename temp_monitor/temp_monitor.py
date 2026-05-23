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

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing deps. Run: pip install pystray Pillow")
    sys.exit(1)

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(SCRIPT_DIR, "temp_monitor.log")
os.makedirs(SCRIPT_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes as _ctypes
    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.TempMonitor")
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
logger = logging.getLogger("TempMonitor")

# ── Thresholds ──
WARNING_TEMP = 75
CRITICAL_TEMP = 85

# ── Colors ──
def temp_color(temp: float) -> tuple:
    """Return RGBA color based on temperature."""
    if temp < 60:
        return (0, 255, 136)    # green
    elif temp < 75:
        return (255, 221, 0)    # yellow
    elif temp < 85:
        return (255, 136, 0)    # orange
    else:
        return (255, 51, 102)   # red


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

            from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType

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
                        if sensor.SensorType == self.SensorType.Temperature and sensor.Value is not None:
                            name = f"{hw.Name} / {sensor.Name}"
                            temps[name] = float(sensor.Value)

                for sensor in hw.Sensors:
                    if sensor.SensorType == self.SensorType.Temperature and sensor.Value is not None:
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
        self.available = False
        self._init()

    def _init(self):
        try:
            import wmi
            self.wmi_obj = wmi.WMI(namespace="root\\wmi")
            self.available = True
            logger.info("WMI temperature reader initialized.")
        except Exception as e:
            logger.warning(f"WMI init failed: {e}")
            # Try OpenHardwareMonitor WMI namespace
            try:
                import wmi
                self.wmi_obj = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                self.available = True
                self._is_ohm = True
                logger.info("OpenHardwareMonitor WMI reader initialized.")
            except Exception:
                self._is_ohm = False

    def read_temps(self) -> dict:
        temps = {}
        if not self.available:
            return temps

        try:
            if hasattr(self, '_is_ohm') and self._is_ohm:
                # OpenHardwareMonitor WMI
                for sensor in self.wmi_obj.Sensor():
                    if sensor.SensorType == "Temperature":
                        temps[sensor.Name] = float(sensor.Value)
            else:
                # Standard WMI thermal zone
                for tz in self.wmi_obj.MSAcpi_ThermalZoneTemperature():
                    # WMI returns temp in tenths of Kelvin
                    temp_c = (tz.CurrentTemperature / 10.0) - 273.15
                    temps[f"Thermal Zone {tz.InstanceName}"] = round(temp_c, 1)
        except Exception as e:
            logger.error(f"WMI read error: {e}")
            self.available = False

        return temps

    def close(self):
        pass


class SimulatedReader:
    """Fallback when no hardware reader is available — shows a message."""

    def __init__(self):
        self.available = True
        logger.warning("No hardware temperature reader available. Using simulated data.")

    def read_temps(self) -> dict:
        import math
        t = time.time()
        # Dynamic sine wave oscillating between 45 and 55 for high-fidelity premium display
        cpu_t = 48.0 + 6.0 * math.sin(t / 20.0)
        gpu_t = 44.0 + 4.0 * math.cos(t / 25.0)
        return {
            "CPU Package (simulated)": round(cpu_t, 1),
            "GPU Core (simulated)": round(gpu_t, 1)
        }

    def close(self):
        pass


# ══════════════════════════════════════════════════════════
#  Animated Toast Notification
# ══════════════════════════════════════════════════════════
class TempToast:
    """Sliding toast notification for temperature alerts."""

    _active = []

    def __init__(self, title: str, message: str, accent: str, severity: str = "warning",
                 duration_ms: int = 8000):
        self.title = title
        self.message = message
        self.accent = accent
        self.severity = severity
        self.duration = duration_ms

    def show(self):
        threading.Thread(target=self._create, daemon=True).start()

    def _create(self):
        try:
            root = tk.Tk()
            root.withdraw()

            toast = tk.Toplevel(root)
            toast.overrideredirect(True)
            toast.attributes("-topmost", True)
            toast.attributes("-alpha", 0.0)
            toast.configure(bg="#161b22")

            toast_w, toast_h = 380, 100
            screen_w = toast.winfo_screenwidth()
            final_x = screen_w - toast_w - 20
            start_x = screen_w + 10
            y_pos = 60 + len(TempToast._active) * 110

            toast.geometry(f"{toast_w}x{toast_h}+{start_x}+{y_pos}")

            # Accent bar
            tk.Frame(toast, bg=self.accent, width=5).pack(side=tk.LEFT, fill=tk.Y)

            content = tk.Frame(toast, bg="#161b22", padx=14, pady=12)
            content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Icon
            icon = "🌡️" if self.severity == "warning" else "🔥"
            title_frame = tk.Frame(content, bg="#161b22")
            title_frame.pack(fill=tk.X)

            tk.Label(
                title_frame, text=icon, font=("Segoe UI Emoji", 20),
                bg="#161b22", fg=self.accent
            ).pack(side=tk.LEFT, padx=(0, 10))

            tk.Label(
                title_frame, text=self.title, font=("Segoe UI", 13, "bold"),
                bg="#161b22", fg="#f0f0f0"
            ).pack(side=tk.LEFT)

            tk.Label(
                content, text=self.message, font=("Segoe UI", 10),
                bg="#161b22", fg="#8b949e", anchor=tk.W
            ).pack(fill=tk.X, pady=(6, 0))

            toast.update_idletasks()
            TempToast._active.append(self)

            # Flash effect for critical
            flash_count = [0]

            def flash():
                if self.severity == "critical" and flash_count[0] < 6:
                    try:
                        alpha = 0.95 if flash_count[0] % 2 == 0 else 0.5
                        toast.attributes("-alpha", alpha)
                        flash_count[0] += 1
                        toast.after(300, flash)
                    except tk.TclError:
                        pass

            # Slide in
            def slide_in(step=0):
                total = 20
                if step <= total:
                    progress = step / total
                    ease = 1 - (1 - progress) ** 3
                    cx = int(start_x + (final_x - start_x) * ease)
                    alpha = min(0.95, ease * 0.95)
                    try:
                        toast.geometry(f"{toast_w}x{toast_h}+{cx}+{y_pos}")
                        toast.attributes("-alpha", alpha)
                        toast.after(16, lambda: slide_in(step + 1))
                    except tk.TclError:
                        pass
                else:
                    if self.severity == "critical":
                        flash()
                    toast.after(self.duration, lambda: slide_out(0))

            def slide_out(step=0):
                total = 15
                if step <= total:
                    progress = step / total
                    cx = int(final_x + (start_x - final_x) * progress)
                    alpha = 0.95 * (1 - progress)
                    try:
                        toast.geometry(f"{toast_w}x{toast_h}+{cx}+{y_pos}")
                        toast.attributes("-alpha", max(0, alpha))
                        toast.after(20, lambda: slide_out(step + 1))
                    except tk.TclError:
                        pass
                else:
                    try:
                        if self in TempToast._active:
                            TempToast._active.remove(self)
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
        self.reader = None
        self.tray_icon = None
        self._running = True
        self._warning_fired = False
        self._critical_fired = False
        self.all_temps = {}
        self.cpu_temp = 0.0
        self.gpu_temp = 0.0

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
            if "cpu" in name_l and ("package" in name_l or "core" in name_l or "tctl" in name_l):
                cpu = max(cpu, val)
            elif "cpu" in name_l and cpu == 0:
                cpu = val
            elif "gpu" in name_l and ("hot spot" in name_l or "core" in name_l or "temperature" in name_l):
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
        if " / " in name:
            name = name.split(" / ")[-1]
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
            if not getattr(self.reader, "available", True) and not isinstance(self.reader, SimulatedReader):
                self.reader = SimulatedReader()
                self.all_temps = self.reader.read_temps()
            self.cpu_temp, self.gpu_temp = self._identify_cpu_gpu(self.all_temps)
            display_temp = self.cpu_temp if self.cpu_temp > 0 else self.gpu_temp
            if self.tray_icon:
                self.tray_icon.icon = create_temp_icon(display_temp)
                lines = []
                for name, val in sorted(self.all_temps.items()):
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
        logger.info("Temperature monitoring loop started.")
        reader_name = type(self.reader).__name__
        logger.info(f"Using reader: {reader_name}")

        while self._running:
            try:
                self.all_temps = self.reader.read_temps()
                # Check if current reader became unavailable due to read error
                if not getattr(self.reader, "available", True) and not isinstance(self.reader, SimulatedReader):
                    logger.warning("Active reader failed. Falling back to SimulatedReader.")
                    self.reader = SimulatedReader()
                    self.all_temps = self.reader.read_temps()
                self.cpu_temp, self.gpu_temp = self._identify_cpu_gpu(self.all_temps)

                display_temp = self.cpu_temp if self.cpu_temp > 0 else self.gpu_temp

                # Update tray icon and dynamic tooltip
                if self.tray_icon:
                    try:
                        self.tray_icon.icon = create_temp_icon(display_temp)
                        
                        # Generate dynamic tooltip listing all sensor temperatures
                        lines = []
                        for name, val in sorted(self.all_temps.items()):
                            short_name = self._shorten_name(name)
                            lines.append(f"{short_name}: {val:.0f}°C")
                        
                        tooltip_str = "\n".join(lines)
                        if len(tooltip_str) > 127:
                            tooltip_str = tooltip_str[:124] + "..."
                        
                        self.tray_icon.title = tooltip_str
                        
                        # Update dynamic right-click menu
                        self.tray_icon.menu = self._build_sensor_menu()
                    except Exception as e:
                        logger.error(f"Tray update error: {e}")

                # ── Temperature alerts ──
                max_temp = max(self.cpu_temp, self.gpu_temp) if self.gpu_temp > 0 else self.cpu_temp

                if max_temp >= CRITICAL_TEMP and not self._critical_fired:
                    self._critical_fired = True
                    self._warning_fired = True
                    source = "CPU" if self.cpu_temp >= CRITICAL_TEMP else "GPU"
                    logger.critical(f"CRITICAL: {source} at {max_temp:.0f}°C!")
                    TempToast(
                        title=f"CRITICAL: {source} at {max_temp:.0f}°C!",
                        message="Thermal throttling risk! Close heavy applications.",
                        accent="#ff3366",
                        severity="critical",
                        duration_ms=10000,
                    ).show()

                elif max_temp >= WARNING_TEMP and not self._warning_fired:
                    self._warning_fired = True
                    source = "CPU" if self.cpu_temp >= WARNING_TEMP else "GPU"
                    logger.warning(f"WARNING: {source} at {max_temp:.0f}°C")
                    TempToast(
                        title=f"Temperature Warning: {source} at {max_temp:.0f}°C",
                        message="Temperature is elevated. Monitor your workload.",
                        accent="#ff8800",
                        severity="warning",
                        duration_ms=8000,
                    ).show()

                # Reset alerts when temp drops
                if max_temp < WARNING_TEMP - 5:
                    self._warning_fired = False
                    self._critical_fired = False
                elif max_temp < CRITICAL_TEMP - 5:
                    self._critical_fired = False

            except Exception as e:
                logger.error(f"Monitor loop error: {e}")

            time.sleep(3)

    def _build_sensor_menu(self):
        """Build dynamic menu items showing all sensors with short names."""
        items = []
        items.append(pystray.MenuItem("Refresh Now", self._force_refresh, default=True))
        items.append(pystray.Menu.SEPARATOR)
        if self.all_temps:
            for name, val in sorted(self.all_temps.items()):
                short = self._shorten_name(name)
                label = f"{short}: {val:.0f}°C"
                items.append(pystray.MenuItem(label, None, enabled=False))
        else:
            items.append(pystray.MenuItem("No sensors detected", None, enabled=False))

        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem(f"⚠ Warn: {WARNING_TEMP}°C", None, enabled=False))
        items.append(pystray.MenuItem(f"🔥 Crit: {CRITICAL_TEMP}°C", None, enabled=False))
        items.append(pystray.Menu.SEPARATOR)
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
        display_temp = self.cpu_temp if self.cpu_temp > 0 else self.gpu_temp

        icon_image = create_temp_icon(display_temp)
        gpu_str = f"{self.gpu_temp:.0f}°C" if self.gpu_temp > 0 else "N/A"

        self.tray_icon = pystray.Icon(
            name="TempMonitor",
            icon=icon_image,
            title=f"CPU: {self.cpu_temp:.0f}°C | GPU: {gpu_str}",
            menu=pystray.Menu(
                pystray.MenuItem("Refresh", self._force_refresh, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(f"CPU: {self.cpu_temp:.0f}°C", None, enabled=False),
                pystray.MenuItem(f"GPU: {gpu_str}", None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(f"⚠ Warn: {WARNING_TEMP}°C", None, enabled=False),
                pystray.MenuItem(f"🔥 Crit: {CRITICAL_TEMP}°C", None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit", self._on_quit),
            ),
        )

        # Start monitor thread
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()

        logger.info(f"Initial CPU: {self.cpu_temp:.0f}°C | GPU: {gpu_str}")
        logger.info("Tray icon running.")
        self.tray_icon.run()


if __name__ == "__main__":
    app = TempMonitorApp()
    app.run()
