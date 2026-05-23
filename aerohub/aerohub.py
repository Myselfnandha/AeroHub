"""
AeroHub Core — Central background orchestrator with floating dashboard widget.
Manages the lifecycle (start, stop, restart, monitor) of all child utility processes.
Tray icon + floating mini-widget showing process status in the desktop corner.
"""

import os
import sys
import json
import time
import subprocess
import threading
import logging
import logging.handlers
import signal
import psutil
import tkinter as tk
from tkinter import ttk
import queue

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing deps. Run: pip install pystray Pillow psutil")
    sys.exit(1)

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UTILS_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SCRIPT_DIR, "aerohub_config.json")
LOG_PATH = os.path.join(SCRIPT_DIR, "aerohub.log")
os.makedirs(SCRIPT_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes as _ctypes
    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.Core")
except Exception:
    pass

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("AeroHub")

# ── Theme ──
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "bg_card": "#1a1a3e",
    "accent": "#7c3aed",
    "accent_hover": "#9b59f5",
    "success": "#00ff88",
    "danger": "#ff3366",
    "warning": "#ffdd00",
    "fg": "#f0f0f0",
    "fg_dim": "#6a7080",
    "border": "#2d2d5e",
    "running": "#00ff88",
    "stopped": "#ff3366",
}

# ── Default Config ──
DEFAULT_CONFIG = {
    "auto_start": True,
    "restart_delay_sec": 5,
    "processes": [
        {
            "id": "clipboard_manager",
            "name": "Clipboard Manager",
            "icon": "📋",
            "script": "clipboard_manager/clipboard_manager.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "health_app",
            "name": "Health App",
            "icon": "👁️",
            "script": "health_app/health_app.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "media_control",
            "name": "Media Control",
            "icon": "🎵",
            "script": "media_control/media_control.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "battery_monitor",
            "name": "Battery Monitor",
            "icon": "🔋",
            "script": "battery_monitor/battery_monitor.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "temp_monitor",
            "name": "Temp Monitor",
            "icon": "🌡️",
            "script": "temp_monitor/temp_monitor.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "touch_toggle",
            "name": "Touch Toggle",
            "icon": "👆",
            "script": "touch_toggle/touch_toggle.py",
            "auto_start": False,
            "enabled": True,
        },
        {
            "id": "tg_fdm_proxy",
            "name": "Telegram FDM Proxy",
            "icon": "📡",
            "script": "tg_fdm_proxy/tg_fdm_proxy.py",
            "auto_start": False,
            "enabled": True,
        },
        {
            "id": "taskbar_scroll_controller",
            "name": "Taskbar Scroll Controller",
            "icon": "🔊",
            "script": "Taskbar Scroll Controller.exe",
            "auto_start": True,
            "enabled": True,
        },
    ],
}


# ══════════════════════════════════════════════════════════
#  Config Management
# ══════════════════════════════════════════════════════════
def load_config() -> dict:
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Config load error: {e}")
    return dict(DEFAULT_CONFIG)


def save_config(config: dict):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        logger.error(f"Config save error: {e}")


# ══════════════════════════════════════════════════════════
#  Process Manager
# ══════════════════════════════════════════════════════════
class ProcessEntry:
    """Represents a managed child process."""

    def __init__(self, config: dict, utils_dir: str):
        self.id = config["id"]
        self.name = config["name"]
        self.icon = config.get("icon", "⚙️")
        self.script = config["script"]
        self.auto_start = config.get("auto_start", False)
        self.enabled = config.get("enabled", True)
        self.utils_dir = utils_dir

        self.process: subprocess.Popen = None
        self.pid = None
        self.status = "stopped"  # running, stopped, crashed, starting
        self.start_time = None
        self.restart_count = 0
        self.last_crash = None

    @property
    def full_path(self) -> str:
        return os.path.join(self.utils_dir, self.script)

    @property
    def uptime_str(self) -> str:
        if not self.start_time:
            return "—"
        elapsed = time.time() - self.start_time
        if elapsed < 60:
            return "<1m"
        h, m = divmod(int(elapsed), 3600)
        m, _ = divmod(m, 60)
        if h > 0:
            return f"{h}h {m}m"
        return f"{m}m"

    def start(self):
        """Start the process."""
        if self.status == "running" and self.process and self.process.poll() is None:
            logger.info(f"[{self.id}] Already running (PID {self.pid})")
            return

        script_path = self.full_path
        if not os.path.exists(script_path):
            logger.error(f"[{self.id}] Script not found: {script_path}")
            self.status = "stopped"
            return

        try:
            self.status = "starting"
            cwd = os.path.dirname(script_path)

            if script_path.lower().endswith(".exe"):
                self.process = subprocess.Popen(
                    [script_path],
                    cwd=cwd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
            else:
                # Use a per-utility hardlink of pythonw.exe so Windows shows
                # each tray icon separately (identified by unique exe path)
                python_exe = sys.executable
                python_dir = os.path.dirname(python_exe)
                pythonw = os.path.join(python_dir, "pythonw.exe")

                # Create a uniquely-named hardlink for this utility
                unique_exe_name = f"pythonw_{self.id}.exe"
                unique_exe = os.path.join(python_dir, unique_exe_name)

                if not os.path.exists(unique_exe):
                    try:
                        os.link(pythonw, unique_exe)  # NTFS hardlink, zero extra space
                        logger.info(f"[{self.id}] Created hardlink: {unique_exe}")
                    except OSError:
                        try:
                            import shutil
                            shutil.copy2(pythonw, unique_exe)
                            logger.info(f"[{self.id}] Copied exe: {unique_exe}")
                        except Exception as e:
                            logger.warning(f"[{self.id}] Could not create unique exe, using shared pythonw: {e}")
                            unique_exe = pythonw

                exe = unique_exe if os.path.exists(unique_exe) else pythonw

                self.process = subprocess.Popen(
                    [exe, script_path],
                    cwd=cwd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
            self.pid = self.process.pid
            self.start_time = time.time()
            self.status = "running"
            logger.info(f"[{self.id}] Started (PID {self.pid})")

        except Exception as e:
            logger.error(f"[{self.id}] Start failed: {e}")
            self.status = "crashed"
            self.last_crash = time.time()

    def stop(self):
        """Stop the process gracefully."""
        if self.process:
            try:
                # Try to terminate the entire process tree
                parent = psutil.Process(self.pid)
                children = parent.children(recursive=True)
                for child in children:
                    try:
                        child.terminate()
                    except psutil.NoSuchProcess:
                        pass
                parent.terminate()

                # Wait up to 5 seconds
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill
                    parent.kill()
                    for child in children:
                        try:
                            child.kill()
                        except psutil.NoSuchProcess:
                            pass

                logger.info(f"[{self.id}] Stopped (PID {self.pid})")
            except (psutil.NoSuchProcess, ProcessLookupError):
                pass
            except Exception as e:
                logger.error(f"[{self.id}] Stop error: {e}")

        self.process = None
        self.pid = None
        self.status = "stopped"
        self.start_time = None

    def restart(self):
        """Restart the process."""
        self.stop()
        time.sleep(1)
        self.start()
        self.restart_count += 1

    def check_health(self) -> bool:
        """Check if the process is still alive."""
        if not self.process or self.status != "running":
            return False

        poll = self.process.poll()
        if poll is not None:
            # Process has exited
            exit_code = poll
            logger.warning(f"[{self.id}] Exited with code {exit_code}")
            if exit_code == 0:
                self.status = "stopped"
            else:
                self.status = "crashed"
                self.last_crash = time.time()
            self.process = None
            self.pid = None
            return False

        # Double-check with psutil
        try:
            proc = psutil.Process(self.pid)
            if not proc.is_running():
                self.status = "crashed"
                self.last_crash = time.time()
                return False
        except psutil.NoSuchProcess:
            self.status = "crashed"
            self.last_crash = time.time()
            return False

        return True


# ══════════════════════════════════════════════════════════
#  Floating Dashboard Widget
# ══════════════════════════════════════════════════════════
class DashboardWidget:
    """Floating mini-widget on the desktop corner showing process status."""

    def __init__(self, processes: list, on_toggle, on_restart):
        self.processes = processes
        self.on_toggle = on_toggle
        self.on_restart = on_restart
        self.queue = queue.Queue()
        self.root = None
        self._visible = False
        self._drag_data = {"x": 0, "y": 0}
        self._status_labels = {}
        self._uptime_labels = {}
        self._btn_labels = {}

    def create(self):
        """Create the floating dashboard."""
        self.root = tk.Tk()
        self.root.title("AeroHub")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.0)
        self.root.configure(bg=TH["bg"])

        n = len(self.processes)
        widget_w = 310
        widget_h = 50 + n * 38 + 10
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w - widget_w - 16
        y = screen_h - widget_h - 60

        self.root.geometry(f"{widget_w}x{widget_h}+{x}+{y}")

        # ── Title bar ──
        title_bar = tk.Frame(self.root, bg=TH["bg2"], height=36)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar, text="🚀 AeroHub", font=("Segoe UI", 11, "bold"),
            bg=TH["bg2"], fg=TH["accent"]
        ).pack(side=tk.LEFT, padx=12)

        # Running count
        self._running_count_var = tk.StringVar(value="")
        tk.Label(
            title_bar, textvariable=self._running_count_var,
            font=("Segoe UI", 9), bg=TH["bg2"], fg=TH["fg_dim"]
        ).pack(side=tk.RIGHT, padx=12)

        # Drag support on title bar
        title_bar.bind("<Button-1>", self._start_drag)
        title_bar.bind("<B1-Motion>", self._do_drag)

        # ── Process rows ──
        container = tk.Frame(self.root, bg=TH["bg"], padx=8, pady=4)
        container.pack(fill=tk.BOTH, expand=True)

        for i, proc in enumerate(self.processes):
            row = tk.Frame(container, bg=TH["bg_card"], pady=3, padx=6)
            row.pack(fill=tk.X, pady=2)

            # Icon + Name
            tk.Label(
                row, text=proc.icon, font=("Segoe UI Emoji", 12),
                bg=TH["bg_card"], fg=TH["fg"]
            ).pack(side=tk.LEFT, padx=(2, 4))

            tk.Label(
                row, text=proc.name, font=("Segoe UI", 9),
                bg=TH["bg_card"], fg=TH["fg"], width=14, anchor=tk.W
            ).pack(side=tk.LEFT)

            # Status dot
            status_label = tk.Label(
                row, text="●", font=("Segoe UI", 10),
                bg=TH["bg_card"], fg=TH["stopped"]
            )
            status_label.pack(side=tk.LEFT, padx=4)
            self._status_labels[proc.id] = status_label

            # Uptime
            uptime_label = tk.Label(
                row, text="—", font=("Consolas", 8),
                bg=TH["bg_card"], fg=TH["fg_dim"], width=7
            )
            uptime_label.pack(side=tk.LEFT, padx=2)
            self._uptime_labels[proc.id] = uptime_label

            # Toggle button
            btn = tk.Button(
                row, text="▶", font=("Segoe UI", 8),
                bg=TH["accent"], fg="white", relief=tk.FLAT,
                width=3, cursor="hand2",
                command=lambda p=proc: self._toggle(p)
            )
            btn.pack(side=tk.RIGHT, padx=2)
            self._btn_labels[proc.id] = btn

            # Restart button
            restart_btn = tk.Button(
                row, text="↻", font=("Segoe UI", 9),
                bg=TH["bg2"], fg=TH["fg_dim"], relief=tk.FLAT,
                width=2, cursor="hand2",
                command=lambda p=proc: self._restart(p)
            )
            restart_btn.pack(side=tk.RIGHT, padx=1)

        # Apply DWM native rounded corners (DWMWA_WINDOW_CORNER_PREFERENCE = 33, DWMWCP_ROUND = 2)
        self.root.update_idletasks()
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            if hwnd == 0:
                hwnd = self.root.winfo_id()
            dwmapi = ctypes.windll.dwmapi
            corner_pref = ctypes.c_int(2)
            dwmapi.DwmSetWindowAttribute(
                ctypes.c_void_p(hwnd),
                33,
                ctypes.byref(corner_pref),
                ctypes.sizeof(corner_pref)
            )
        except Exception as e:
            logger.error(f"DWM rounding error: {e}")

        self.root.after(100, self._poll_queue)
        self.root.withdraw()
        self._visible = False

    def _toggle(self, proc):
        threading.Thread(target=self.on_toggle, args=(proc,), daemon=True).start()

    def _restart(self, proc):
        threading.Thread(target=self.on_restart, args=(proc,), daemon=True).start()

    def _start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_data["x"])
        y = self.root.winfo_y() + (event.y - self._drag_data["y"])
        self.root.geometry(f"+{x}+{y}")

    def update_status(self):
        """Update all process status displays."""
        running = 0
        for proc in self.processes:
            sid = proc.id

            if sid in self._status_labels:
                if proc.status == "running":
                    self._status_labels[sid].config(fg=TH["running"])
                    self._btn_labels[sid].config(text="■", bg=TH["danger"])
                    running += 1
                elif proc.status == "crashed":
                    self._status_labels[sid].config(fg=TH["warning"])
                    self._btn_labels[sid].config(text="▶", bg=TH["accent"])
                else:
                    self._status_labels[sid].config(fg=TH["stopped"])
                    self._btn_labels[sid].config(text="▶", bg=TH["accent"])

            if sid in self._uptime_labels:
                self._uptime_labels[sid].config(text=proc.uptime_str)

        self._running_count_var.set(f"{running}/{len(self.processes)}")

    def _periodic_update(self):
        """Update status every 2 seconds."""
        if self._visible and self.root:
            self.update_status()
            self.root.after(2000, self._periodic_update)

    def _fade_in(self, step=0):
        total = 15
        if step <= total:
            alpha = min(0.92, step / total * 0.92)
            try:
                self.root.attributes("-alpha", alpha)
                self.root.after(20, lambda: self._fade_in(step + 1))
            except tk.TclError:
                pass

    def show(self):
        if self.root:
            self.root.deiconify()
            self.root.focus_force()
            self._visible = True
            self._fade_in()
            self._periodic_update()

            # Bind FocusOut to automatically hide when clicking elsewhere
            def on_focus_out(event):
                if event.widget == self.root:
                    def check_focus():
                        if self.root.focus_displayof() is None:
                            self.hide_safe()
                    self.root.after(100, check_focus)
            
            self.root.bind("<FocusOut>", on_focus_out)

    def hide(self):
        if self.root:
            self.root.withdraw()
            self._visible = False

    def show_safe(self):
        if self.root:
            self.queue.put((self.show, ()))

    def hide_safe(self):
        if self.root:
            self.queue.put((self.hide, ()))

    def _poll_queue(self):
        if not self.root:
            return
        try:
            while not self.queue.empty():
                callback, args = self.queue.get_nowait()
                callback(*args)
        except Exception as e:
            logger.error(f"Error in queue poll: {e}")
        try:
            self.root.after(100, self._poll_queue)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════
def create_aerohub_icon(running_count: int, total: int) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background
    if running_count == total:
        bg_color = (0, 255, 136, 220)  # all running - green
    elif running_count > 0:
        bg_color = (124, 58, 237, 220)  # some running - purple
    else:
        bg_color = (100, 100, 100, 220)  # none running - gray

    draw.rounded_rectangle([2, 2, 62, 62], radius=10, fill=bg_color)

    # Rocket icon (simple triangle)
    draw.polygon([(32, 8), (20, 48), (44, 48)], fill=(255, 255, 255, 220))
    # Exhaust
    draw.polygon([(26, 48), (32, 58), (38, 48)], fill=(255, 200, 50, 200))

    return img


# ══════════════════════════════════════════════════════════
#  AeroHub Core
# ══════════════════════════════════════════════════════════
class AeroHubCore:
    def __init__(self):
        self.config = load_config()
        self.processes: list[ProcessEntry] = []
        self.tray_icon = None
        self.widget = None
        self._running = True

        # Initialize process entries
        for proc_config in self.config.get("processes", DEFAULT_CONFIG["processes"]):
            entry = ProcessEntry(proc_config, UTILS_DIR)
            self.processes.append(entry)

    def _on_toggle(self, proc: ProcessEntry):
        """Toggle a process on/off."""
        if proc.status == "running":
            proc.stop()
        else:
            proc.start()
        self._update_tray_icon()

    def _on_restart(self, proc: ProcessEntry):
        """Restart a process."""
        proc.restart()
        self._update_tray_icon()

    def _auto_start_all(self):
        """Start all processes that have auto_start enabled."""
        for proc in self.processes:
            if proc.auto_start and proc.enabled:
                logger.info(f"Auto-starting: {proc.name}")
                proc.start()
                time.sleep(1)  # Stagger starts

    def _health_monitor(self):
        """Background thread: monitor all processes and auto-restart crashed ones."""
        restart_delay = self.config.get("restart_delay_sec", 5)

        while self._running:
            for proc in self.processes:
                if proc.status == "running":
                    alive = proc.check_health()
                    if not alive and proc.status == "crashed" and proc.enabled and proc.auto_start:
                        logger.warning(f"[{proc.id}] Crashed! Auto-restarting in {restart_delay}s...")
                        time.sleep(restart_delay)
                        if self._running:  # Check we haven't been told to stop
                            proc.start()
                            proc.restart_count += 1

            self._update_tray_icon()
            time.sleep(3)

    def _update_tray_icon(self):
        """Update tray icon based on running process count."""
        running = sum(1 for p in self.processes if p.status == "running")
        if self.tray_icon:
            try:
                self.tray_icon.icon = create_aerohub_icon(running, len(self.processes))
                self.tray_icon.title = f"AeroHub — {running}/{len(self.processes)} running"
            except Exception:
                pass

    def _start_all(self, icon=None, item=None):
        """Start all enabled processes."""
        def _start():
            for proc in self.processes:
                if proc.enabled and proc.status != "running":
                    proc.start()
                    time.sleep(0.5)
            self._update_tray_icon()
        threading.Thread(target=_start, daemon=True).start()

    def _stop_all(self, icon=None, item=None):
        """Stop all processes."""
        def _stop():
            for proc in self.processes:
                if proc.status == "running":
                    proc.stop()
            self._update_tray_icon()
        threading.Thread(target=_stop, daemon=True).start()

    def _on_show_widget(self, icon=None, item=None):
        """Show/hide the floating dashboard."""
        if self.widget:
            if self.widget._visible:
                self.widget.hide_safe()
            else:
                self.widget.show_safe()

    def _on_quit(self, icon, item):
        """Quit AeroHub and stop all child processes."""
        logger.info("AeroHub shutting down — stopping all processes...")
        self._running = False

        for proc in self.processes:
            if proc.status == "running":
                proc.stop()

        icon.stop()

        # Save config
        save_config(self.config)

        os._exit(0)

    def _promote_tray_icons(self):
        """Clear stale Python tray icon entries and promote current ones to always-visible."""
        try:
            import winreg
            base_key = r"Control Panel\NotifyIconSettings"

            # Phase 1: Delete all old Python/UTILITIES entries for a clean slate
            to_delete = []
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_key) as root:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(root, i)
                        i += 1
                        try:
                            with winreg.OpenKey(root, subkey_name, 0, winreg.KEY_READ) as sk:
                                exe_path, _ = winreg.QueryValueEx(sk, "ExecutablePath")
                                if exe_path and ("python" in exe_path.lower() or "utilities" in exe_path.lower()):
                                    to_delete.append(subkey_name)
                        except (FileNotFoundError, OSError):
                            pass
                    except OSError:
                        break

            if to_delete:
                for subkey_name in to_delete:
                    try:
                        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"{base_key}\\{subkey_name}")
                    except OSError:
                        pass
                logger.info(f"Cleared {len(to_delete)} stale tray icon registry entries.")

            # Phase 2: After child processes create new icons, promote them
            # (runs on a delayed thread so icons have time to register)
            def _delayed_promote():
                import time as _t
                _t.sleep(8)  # Wait for child processes to create their tray icons
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_key) as root:
                        i = 0
                        promoted = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(root, i)
                                i += 1
                                with winreg.OpenKey(root, subkey_name, 0, winreg.KEY_READ | winreg.KEY_WRITE) as sk:
                                    try:
                                        exe_path, _ = winreg.QueryValueEx(sk, "ExecutablePath")
                                        if exe_path and ("python" in exe_path.lower() or "utilities" in exe_path.lower()):
                                            winreg.SetValueEx(sk, "IsPromoted", 0, winreg.REG_DWORD, 1)
                                            promoted += 1
                                    except (FileNotFoundError, OSError):
                                        pass
                            except OSError:
                                break
                    if promoted > 0:
                        logger.info(f"Promoted {promoted} tray icon(s) to always-visible.")
                except Exception as e:
                    logger.warning(f"Delayed tray promotion failed: {e}")

            threading.Thread(target=_delayed_promote, daemon=True).start()

        except Exception as e:
            logger.warning(f"Tray icon cleanup failed (non-critical): {e}")

    def run(self):
        logger.info("=" * 60)
        logger.info("  AeroHub Core starting...")
        logger.info("=" * 60)
        logger.info(f"Utilities directory: {UTILS_DIR}")
        logger.info(f"Managed processes: {len(self.processes)}")

        # Clear stale tray icons and schedule promotion of new ones
        self._promote_tray_icons()

        # Save default config if not exists
        if not os.path.exists(CONFIG_PATH):
            save_config(self.config)

        # Create tray icon
        running = 0
        icon_image = create_aerohub_icon(running, len(self.processes))

        self.tray_icon = pystray.Icon(
            name="AeroHub",
            icon=icon_image,
            title=f"AeroHub — {running}/{len(self.processes)} running",
            menu=pystray.Menu(
                pystray.MenuItem("🚀 Show Dashboard", self._on_show_widget, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("▶ Start All", self._start_all),
                pystray.MenuItem("■ Stop All", self._stop_all),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit AeroHub", self._on_quit),
            ),
        )

        # Run tray in background thread
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

        # Auto-start processes
        if self.config.get("auto_start", True):
            auto_thread = threading.Thread(target=self._auto_start_all, daemon=True)
            auto_thread.start()

        # Start health monitor
        health_thread = threading.Thread(target=self._health_monitor, daemon=True)
        health_thread.start()

        # Create and run floating dashboard widget (tkinter main loop on main thread)
        self.widget = DashboardWidget(self.processes, self._on_toggle, self._on_restart)
        self.widget.create()

        logger.info("AeroHub dashboard running.")
        self.widget.root.mainloop()


def check_admin_and_elevate():
    import ctypes
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if "--no-elevate" in sys.argv:
        logger.info("Running without elevation (bypassed via --no-elevate)")
        return

    if not is_admin:
        try:
            script = os.path.abspath(sys.argv[0])
            params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}" {params}', os.path.dirname(script), 1
            )
            if int(ret) > 32:
                sys.exit(0)
            else:
                logger.error(f"UAC elevation failed with return value: {ret}")
        except Exception as e:
            logger.error(f"Failed to elevate: {e}")
        
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        proceed = messagebox.askyesno(
            "Privilege Warning",
            "AeroHub was not elevated to Administrator. Running without Admin privileges may cause some features to fail.\n\n"
            "Do you want to proceed anyway?",
            icon="warning"
        )
        root.destroy()
        if not proceed:
            sys.exit(0)


if __name__ == "__main__":
    try:
        check_admin_and_elevate()
        app = AeroHubCore()
        app.run()
    except Exception as e:
        import traceback
        with open(os.path.join(SCRIPT_DIR, "aerohub_crash.log"), "w", encoding="utf-8") as f:
            f.write(f"Crash at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            traceback.print_exc(file=f)
        try:
            logger.exception("AeroHub crashed on startup:")
        except Exception:
            pass
        sys.exit(1)
