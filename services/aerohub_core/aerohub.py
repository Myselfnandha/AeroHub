"""
AeroHub Core — Central background orchestrator with floating dashboard widget.
Manages the lifecycle (start, stop, restart, monitor) of all child utility processes.
Tray icon + floating mini-widget showing process status in the desktop corner.
"""

import argparse
import importlib
import os
import sys
import json
import time
import subprocess
import threading
import logging
import logging.handlers
import psutil
import tkinter as tk
import queue

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICES_DIR = os.path.dirname(SCRIPT_DIR)
ROOT_DIR = os.path.dirname(SERVICES_DIR)
UTILS_DIR = ROOT_DIR
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, SERVICES_DIR)

remote_control = importlib.import_module("aerohub_core.remote_control")
LocalControlHandler = remote_control.LocalControlHandler
LocalControlServer = remote_control.LocalControlServer

try:
    from config.loader import load_config as load_runtime_config
    from config.logging import setup_logging
except ImportError:
    def load_runtime_config():
        return {}

    def setup_logging(*args, **kwargs):
        return logging.getLogger()

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None

LOG_PATH = os.path.join(UTILS_DIR, "aerohub.log")
LOGS_DIR = os.path.join(UTILS_DIR, "Logs")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "aerohub_config.json")
os.makedirs(SCRIPT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes as _ctypes

    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.Core")
except Exception:
    pass

# ── Logging ──
runtime_settings = load_runtime_config()
setup_logging("aerohub", config=runtime_settings)
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
            "script": "services/clipboard_manager/ClipboardManager/clipboard_manager.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "health_app",
            "name": "Health App",
            "icon": "👁️",
            "script": "services/health_app/health_app.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "media_control",
            "name": "Media Control",
            "icon": "🎵",
            "script": "services/media_control/media_control.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "battery_monitor",
            "name": "Battery Monitor",
            "icon": "🔋",
            "script": "toggles/battery_monitor/battery_monitor.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "temp_monitor",
            "name": "Temp Monitor",
            "icon": "🌡️",
            "script": "toggles/temp_monitor/temp_monitor.py",
            "auto_start": True,
            "enabled": True,
        },
        {
            "id": "touch_toggle",
            "name": "Touch Toggle",
            "icon": "👆",
            "script": "toggles/touch_toggle/touch_toggle.py",
            "auto_start": False,
            "enabled": True,
        },
        {
            "id": "tg_fdm_proxy",
            "name": "Telegram FDM Proxy",
            "icon": "📡",
            "script": "services/tg_fdm_proxy/TgFdmProxy/tg_fdm_proxy.py",
            "auto_start": False,
            "enabled": True,
        },
        {
            "id": "taskbar_scroll_controller",
            "name": "Taskbar Scroll Controller",
            "icon": "🔊",
            "script": "tools/taskbar_scroll/taskbar_scroll.py",
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
        self.restart_delay = config.get("restart_delay_sec", 5)
        self.max_restarts = config.get("max_restarts", 3)
        self.restart_backoff = config.get("restart_backoff", 2)
        self.utils_dir = utils_dir

        self.process: subprocess.Popen = None
        self.pid = None
        self.status = "stopped"  # running, stopped, crashed, starting
        self.start_time = None
        self.restart_count = 0
        self.last_crash = None
        self.consecutive_crashes = 0
        self.next_restart_time = 0.0

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

        now = time.time()
        if self.status == "crashed" and now < self.next_restart_time:
            logger.warning(
                f"[{self.id}] Restart backoff active until "
                f"{time.strftime('%H:%M:%S', time.localtime(self.next_restart_time))}"
            )
            return

        if self.last_crash and now - self.last_crash > 300:
            self.consecutive_crashes = 0

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
                    creationflags=subprocess.CREATE_NO_WINDOW
                    if sys.platform == "win32"
                    else 0,
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
                            logger.warning(
                                f"[{self.id}] Could not create unique exe, using shared pythonw: {e}"
                            )
                            unique_exe = pythonw

                exe = unique_exe if os.path.exists(unique_exe) else pythonw

                self.process = subprocess.Popen(
                    [exe, script_path],
                    cwd=cwd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                    if sys.platform == "win32"
                    else 0,
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
                self.consecutive_crashes += 1
                backoff = self.restart_delay * (
                    self.restart_backoff ** max(0, self.consecutive_crashes - 1)
                )
                self.next_restart_time = time.time() + min(backoff, 300)
                if self.consecutive_crashes >= self.max_restarts:
                    self.status = "circuit_breaker"
                    logger.error(
                        f"[{self.id}] Circuit breaker triggered after {self.consecutive_crashes} failures"
                    )
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

    def __init__(
        self,
        processes: list,
        on_toggle,
        on_restart,
        on_start_all=None,
        on_stop_all=None,
        on_exit=None,
    ):
        self.processes = processes
        self.on_toggle = on_toggle
        self.on_restart = on_restart
        self.on_start_all = on_start_all
        self.on_stop_all = on_stop_all
        self.on_exit = on_exit
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
        widget_w = 380
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
            title_bar,
            text="🚀 AeroHub",
            font=("Segoe UI", 11, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
        ).pack(side=tk.LEFT, padx=(12, 6))

        # Hover effect helper for title buttons
        def add_hover(widget, hover_fg):
            default_fg = widget.cget("fg")
            widget.bind(
                "<Enter>", lambda e: widget.config(bg=TH["bg_card"], fg=hover_fg)
            )
            widget.bind("<Leave>", lambda e: widget.config(bg=TH["bg2"], fg=default_fg))

        if self.on_start_all:
            btn = tk.Button(
                title_bar,
                text="▶",
                font=("Segoe UI", 10),
                bg=TH["bg2"],
                fg=TH["running"],
                activebackground=TH["bg_card"],
                activeforeground=TH["running"],
                relief=tk.FLAT,
                cursor="hand2",
                command=self.on_start_all,
            )
            btn.pack(side=tk.LEFT, padx=2)
            add_hover(btn, hover_fg=TH["running"])

        if self.on_stop_all:
            btn = tk.Button(
                title_bar,
                text="■",
                font=("Segoe UI", 10),
                bg=TH["bg2"],
                fg=TH["danger"],
                activebackground=TH["bg_card"],
                activeforeground=TH["danger"],
                relief=tk.FLAT,
                cursor="hand2",
                command=self.on_stop_all,
            )
            btn.pack(side=tk.LEFT, padx=2)
            add_hover(btn, hover_fg=TH["danger"])

        if self.on_exit:
            btn = tk.Button(
                title_bar,
                text="⏻",
                font=("Segoe UI", 10),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                activebackground=TH["bg_card"],
                activeforeground=TH["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                command=self.on_exit,
            )
            btn.pack(side=tk.LEFT, padx=2)
            add_hover(btn, hover_fg=TH["accent"])

        # Running count
        self._running_count_var = tk.StringVar(value="")
        tk.Label(
            title_bar,
            textvariable=self._running_count_var,
            font=("Segoe UI", 9),
            bg=TH["bg2"],
            fg=TH["fg_dim"],
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
                row,
                text=proc.icon,
                font=("Segoe UI Emoji", 12),
                bg=TH["bg_card"],
                fg=TH["fg"],
            ).pack(side=tk.LEFT, padx=(2, 4))

            tk.Label(
                row,
                text=proc.name,
                font=("Segoe UI", 9),
                bg=TH["bg_card"],
                fg=TH["fg"],
                width=24,
                anchor=tk.W,
            ).pack(side=tk.LEFT)

            # Status dot
            status_label = tk.Label(
                row, text="●", font=("Segoe UI", 10), bg=TH["bg_card"], fg=TH["stopped"]
            )
            status_label.pack(side=tk.LEFT, padx=4)
            self._status_labels[proc.id] = status_label

            # Uptime
            uptime_label = tk.Label(
                row,
                text="—",
                font=("Consolas", 8),
                bg=TH["bg_card"],
                fg=TH["fg_dim"],
                width=7,
            )
            uptime_label.pack(side=tk.LEFT, padx=2)
            self._uptime_labels[proc.id] = uptime_label

            # Toggle button
            btn = tk.Button(
                row,
                text="▶",
                font=("Segoe UI", 8),
                bg=TH["accent"],
                fg="white",
                relief=tk.FLAT,
                width=3,
                cursor="hand2",
                command=lambda p=proc: self._toggle(p),
            )
            btn.pack(side=tk.RIGHT, padx=2)
            self._btn_labels[proc.id] = btn

            # Restart button
            restart_btn = tk.Button(
                row,
                text="↻",
                font=("Segoe UI", 9),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                relief=tk.FLAT,
                width=2,
                cursor="hand2",
                command=lambda p=proc: self._restart(p),
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
                ctypes.sizeof(corner_pref),
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
    def __init__(self, headless: bool = False):
        self.config = load_config()
        self.runtime_settings = load_runtime_config()
        self.processes: list[ProcessEntry] = []
        self.tray_icon = None
        self.widget = None
        self._running = True
        self.headless = headless
        self.control_port = int(
            self.runtime_settings.get("app", {}).get("control_port", 8200)
        )
        self.control_token = (
            self.runtime_settings.get("app", {}).get("control_token")
            or os.environ.get("AEROHUB_CONTROL_TOKEN")
        )
        self.control_server = None

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
                    if not alive and proc.status == "crashed":
                        logger.warning(f"[{proc.id}] Detected crash for running process")
                if proc.status == "crashed" and proc.enabled and proc.auto_start:
                    now = time.time()
                    if now < proc.next_restart_time:
                        logger.warning(
                            f"[{proc.id}] Waiting for backoff until "
                            f"{time.strftime('%H:%M:%S', time.localtime(proc.next_restart_time))}"
                        )
                    elif proc.consecutive_crashes >= proc.max_restarts:
                        logger.error(
                            f"[{proc.id}] Restart disabled by circuit breaker"
                        )
                    else:
                        logger.warning(
                            f"[{proc.id}] Crashed! Auto-restarting in {restart_delay}s..."
                        )
                        time.sleep(restart_delay)
                        if self._running:
                            proc.start()
                            proc.restart_count += 1

            self._update_tray_icon()
            time.sleep(3)

    def _is_system_in_game_mode(self) -> bool:
        """Checks if the system is running a fullscreen DirectX/OpenGL game or fullscreen app."""
        import ctypes.wintypes

        try:
            # 1. SHQueryUserNotificationState check
            state = ctypes.c_int()
            res = ctypes.windll.shell32.SHQueryUserNotificationState(
                ctypes.byref(state)
            )
            if res == 0:
                # 1: QUNS_BUSY covers fullscreen/presenting.
                # 2: QUNS_RUNNING_D3D_FULL_SCREEN covers exclusive fullscreen games.
                if state.value in (1, 2):
                    return True
        except Exception:
            pass

        # 2. Fallback to Active Bounding Window Check
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return False

            # Ignore common desktop and shell windows
            class_name = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, class_name, 256)
            cname = class_name.value
            if cname in ("Progman", "WorkerW", "Shell_TrayWnd", "Button"):
                return False

            # Get window rect
            rect = ctypes.wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            width = rect.right - rect.left
            height = rect.bottom - rect.top

            # Get active monitor info
            monitor = ctypes.windll.user32.MonitorFromWindow(
                hwnd, 1
            )  # MONITOR_DEFAULTTOPRIMARY = 1

            # MONITORINFO structure size is 40 bytes
            class MONITORINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.c_ulong),
                    ("rcMonitor", ctypes.wintypes.RECT),
                    ("rcWork", ctypes.wintypes.RECT),
                    ("dwFlags", ctypes.c_ulong),
                ]

            info = MONITORINFO()
            info.cbSize = ctypes.sizeof(MONITORINFO)
            if ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
                m_width = info.rcMonitor.right - info.rcMonitor.left
                m_height = info.rcMonitor.bottom - info.rcMonitor.top
                # Check if dimensions match active monitor dimensions
                if width >= m_width and height >= m_height:
                    # Check window styles: WS_POPUP (0x80000000) or lack of WS_CAPTION (0x00C00000)
                    style = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
                    if (style & 0x80000000) or not (style & 0x00C00000):
                        return True
        except Exception:
            pass
        return False

    def _set_service_priority(self, service_id: str, priority_class: int):
        """Set process priority of a managed service."""
        for proc in self.processes:
            if proc.id == service_id:
                if proc.status == "running" and proc.pid:
                    try:
                        p = psutil.Process(proc.pid)
                        p.nice(priority_class)
                    except Exception as e:
                        logger.warning(
                            f"[GAME MODE] Failed to set priority of {service_id}: {e}"
                        )

    def _send_udp_ipc_message(self, port: int, message: str):
        """Send a UDP packet to local port."""
        import socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message.encode("utf-8"), ("127.0.0.1", port))
            sock.close()
            logger.info(f"[GAME MODE] Sent IPC '{message}' to port {port}")
        except Exception as e:
            logger.error(f"[GAME MODE] IPC send failed: {e}")

    def _control_service(self, service_id: str, action: str):
        """Start or stop a service by its ID."""
        for proc in self.processes:
            if proc.id == service_id:
                if action == "stop":
                    if proc.status == "running":
                        logger.info(f"[GAME MODE] Stopping service: {service_id}")
                        proc.stop()
                elif action == "start":
                    if proc.enabled and proc.status != "running":
                        logger.info(f"[GAME MODE] Starting service: {service_id}")
                        proc.start()

    def _game_mode_monitor(self):
        """Periodically polls to check if game/fullscreen mode is active and manages utilities."""
        game_mode_active = False
        cooldown_end_time = 0
        temp_monitor_paused = False
        consecutive_gaming = 0
        consecutive_nongaming = 0

        while self._running:
            try:
                is_gaming = self._is_system_in_game_mode()
            except Exception as e:
                logger.error(f"Error checking game mode: {e}")
                is_gaming = False

            if is_gaming:
                consecutive_gaming += 1
                consecutive_nongaming = 0
            else:
                consecutive_gaming = 0
                consecutive_nongaming += 1

            # If we paused it, check if user manually started it
            if temp_monitor_paused:
                for proc in self.processes:
                    if proc.id == "temp_monitor" and proc.status == "running":
                        logger.info(
                            "[GAME MODE] temp_monitor manually started by user. Overriding pause."
                        )
                        temp_monitor_paused = False

            # --- STATE TRANSITIONS ---
            if not game_mode_active and consecutive_gaming >= 2:
                # Entering game mode (detected for 2 consecutive polls, ~6s)
                cooldown_end_time = 0  # reset cooldown

                # Force IDLE priority
                self._set_service_priority("health_app", psutil.IDLE_PRIORITY_CLASS)

                logger.info(
                    "[GAME MODE] Fullscreen/Game detected. Activating AeroEco..."
                )
                game_mode_active = True

                # Send UDP IPC packet game_mode:on to health_app
                self._send_udp_ipc_message(5098, "game_mode:on")

                # Send UDP IPC packet game_mode:on to temp_monitor to pause it
                self._send_udp_ipc_message(5099, "game_mode:on")
                temp_monitor_paused = True

            elif game_mode_active and consecutive_nongaming >= 2:
                # Exiting game mode (not detected for 2 consecutive polls, ~6s)
                logger.info(
                    "[GAME MODE] Fullscreen/Game exited. Entering resume cooldown..."
                )
                game_mode_active = False
                consecutive_gaming = 0

                # Restore health_app priority to NORMAL immediately
                self._set_service_priority("health_app", psutil.NORMAL_PRIORITY_CLASS)

                # Send UDP IPC packet game_mode:off to health_app immediately
                self._send_udp_ipc_message(5098, "game_mode:off")

                # Initialize cooldown period for temp_monitor
                cooldown_end_time = time.time() + 30.0

            elif game_mode_active and is_gaming:
                # Sustaining game mode, keep priority low
                self._set_service_priority("health_app", psutil.IDLE_PRIORITY_CLASS)

            # Check if cooldown has expired
            if cooldown_end_time > 0:
                remaining = cooldown_end_time - time.time()
                if remaining <= 0:
                    logger.info("[GAME MODE] Cooldown expired. Resuming temp_monitor.")
                    cooldown_end_time = 0

                    if temp_monitor_paused:
                        # Send UDP IPC packet game_mode:off to temp_monitor to resume it
                        self._send_udp_ipc_message(5099, "game_mode:off")
                        temp_monitor_paused = False

            time.sleep(3.0)

    def _update_tray_icon(self):
        """Update tray icon based on running process count."""
        running = sum(1 for p in self.processes if p.status == "running")
        if self.tray_icon:
            try:
                self.tray_icon.icon = create_aerohub_icon(running, len(self.processes))
                self.tray_icon.title = (
                    f"AeroHub — {running}/{len(self.processes)} running"
                )
            except Exception:
                pass

    def get_health(self) -> dict:
        return {
            "status": "running" if self._running else "stopped",
            "processes": len(self.processes),
            "running": sum(1 for p in self.processes if p.status == "running"),
        }

    def get_status(self) -> dict:
        return {
            "processes": [
                {
                    "id": proc.id,
                    "name": proc.name,
                    "status": proc.status,
                    "pid": proc.pid,
                    "uptime": proc.uptime_str,
                    "restart_count": proc.restart_count,
                }
                for proc in self.processes
            ]
        }

    def get_metrics(self) -> dict:
        metrics = {
            "process_running_total": sum(1 for p in self.processes if p.status == "running"),
            "process_crashed_total": sum(1 for p in self.processes if p.status == "crashed"),
            "process_circuit_breakers": sum(
                1 for p in self.processes if p.status == "circuit_breaker"
            ),
        }
        return metrics

    def perform_self_update(self) -> dict:
        if self_update():
            return {"status": "updated", "message": "Self-update succeeded."}
        return {"status": "failed", "message": "Self-update failed. See logs."}

    def control_service(self, service_id: str, action: str) -> dict:
        proc = next((p for p in self.processes if p.id == service_id), None)
        if not proc:
            return {"error": "service not found", "service": service_id}
        if action == "start":
            proc.start()
            return {"status": "started", "service": service_id}
        if action == "stop":
            proc.stop()
            return {"status": "stopped", "service": service_id}
        if action == "restart":
            proc.restart()
            return {"status": "restarted", "service": service_id}
        return {"error": "invalid action", "action": action}

    def _cli_status_reporter(self):
        def runner():
            while self._running:
                statuses = [
                    f"{proc.id}: {proc.status} (pid={proc.pid or 'n/a'})"
                    for proc in self.processes
                ]
                logger.info("[AeroHub] %s", " | ".join(statuses))
                time.sleep(5)

        thread = threading.Thread(target=runner, daemon=True)
        thread.start()

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

        sys.exit(0)

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
                            with winreg.OpenKey(
                                root, subkey_name, 0, winreg.KEY_READ
                            ) as sk:
                                exe_path, _ = winreg.QueryValueEx(sk, "ExecutablePath")
                                if exe_path and (
                                    "python" in exe_path.lower()
                                    or "utilities" in exe_path.lower()
                                ):
                                    to_delete.append(subkey_name)
                        except (FileNotFoundError, OSError):
                            pass
                    except OSError:
                        break

            if to_delete:
                for subkey_name in to_delete:
                    try:
                        winreg.DeleteKey(
                            winreg.HKEY_CURRENT_USER, f"{base_key}\\{subkey_name}"
                        )
                    except OSError:
                        pass
                logger.info(
                    f"Cleared {len(to_delete)} stale tray icon registry entries."
                )

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
                                with winreg.OpenKey(
                                    root,
                                    subkey_name,
                                    0,
                                    winreg.KEY_READ | winreg.KEY_WRITE,
                                ) as sk:
                                    try:
                                        exe_path, _ = winreg.QueryValueEx(
                                            sk, "ExecutablePath"
                                        )
                                        if exe_path and (
                                            "python" in exe_path.lower()
                                            or "utilities" in exe_path.lower()
                                        ):
                                            winreg.SetValueEx(
                                                sk, "IsPromoted", 0, winreg.REG_DWORD, 1
                                            )
                                            promoted += 1
                                    except (FileNotFoundError, OSError):
                                        pass
                            except OSError:
                                break
                    if promoted > 0:
                        logger.info(
                            f"Promoted {promoted} tray icon(s) to always-visible."
                        )
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
        logger.info(f"Headless mode: {self.headless}")

        # Clear stale tray icons and schedule promotion of new ones
        self._promote_tray_icons()

        # Save default config if not exists
        if not os.path.exists(CONFIG_PATH):
            save_config(self.config)

        # Start local control API
        try:
            server_address = ("127.0.0.1", self.control_port)
            self.control_server = LocalControlServer(
                server_address, LocalControlHandler, self, self.control_token
            )
            control_thread = threading.Thread(target=self.control_server.serve_forever, daemon=True)
            control_thread.start()
            logger.info(f"Control API listening on http://127.0.0.1:{self.control_port}")
        except Exception as exc:
            logger.warning(f"Could not start control API: {exc}")

        # Auto-start processes
        if self.config.get("auto_start", True):
            auto_thread = threading.Thread(target=self._auto_start_all, daemon=True)
            auto_thread.start()

        # Start health monitor
        health_thread = threading.Thread(target=self._health_monitor, daemon=True)
        health_thread.start()

        # Start Game Mode monitor
        game_mode_thread = threading.Thread(target=self._game_mode_monitor, daemon=True)
        game_mode_thread.start()

        if self.headless or pystray is None:
            logger.info("Running without tray icon; CLI status reporter enabled.")
            self._cli_status_reporter()
            try:
                while self._running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self._on_quit(None, None)
            return

        # Create tray icon
        running = 0
        icon_image = create_aerohub_icon(running, len(self.processes))

        self.tray_icon = pystray.Icon(
            name="AeroHub",
            icon=icon_image,
            title=f"AeroHub — {running}/{len(self.processes)} running",
            menu=pystray.Menu(
                pystray.MenuItem(
                    "🚀 Show Dashboard", self._on_show_widget, default=True
                ),
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

        # Create and run floating dashboard widget (tkinter main loop on main thread)
        self.widget = DashboardWidget(
            self.processes,
            self._on_toggle,
            self._on_restart,
            on_start_all=self._start_all,
            on_stop_all=self._stop_all,
            on_exit=lambda: self._on_quit(self.tray_icon, None),
        )
        self.widget.create()

        logger.info("AeroHub dashboard running.")
        self.widget.root.mainloop()


def check_admin_and_elevate(no_uac: bool = False, headless: bool = False):
    import ctypes

    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if is_admin:
        logger.info("✓ Running with Administrator privileges.")
        return

    if no_uac or headless:
        logger.warning(
            "Skipping UAC elevation because --no-uac or headless mode was requested."
        )
        return

    logger.info("Requesting elevation via UAC in non-blocking mode...")
    try:
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            f'"{script}" {params}',
            os.path.dirname(script),
            1,
        )
        if int(ret) > 32:
            logger.info("Elevation requested; exiting parent process.")
            sys.exit(0)
        logger.error(f"UAC elevation failed with return value: {ret}")
    except Exception as e:
        logger.error(f"Failed to elevate: {e}")


def self_update():
    if not os.path.isdir(os.path.join(ROOT_DIR, ".git")):
        logger.error("No git repository found. Self-update requires git.")
        return False
    try:
        old_rev = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT_DIR
        ).decode("utf-8").strip()
        subprocess.run(["git", "fetch", "--all"], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "pull", "--ff-only"], cwd=ROOT_DIR, check=True)
        logger.info("Self-update pulled the latest revision.")
        return True
    except Exception as exc:
        logger.error(f"Self-update failed: {exc}")
        try:
            subprocess.run(["git", "reset", "--hard", old_rev], cwd=ROOT_DIR, check=True)
            logger.info("Rolled back to previous revision.")
        except Exception as rollback_exc:
            logger.error(f"Rollback failed: {rollback_exc}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AeroHub Core Launcher")
    parser.add_argument("--service", action="store_true", help="Run in service/headless mode")
    parser.add_argument("--headless", action="store_true", help="Run without GUI/tray")
    parser.add_argument("--no-uac", action="store_true", help="Do not request UAC elevation")
    parser.add_argument("--self-update", action="store_true", help="Update from git and restart")
    args = parser.parse_args()

    try:
        if args.self_update:
            success = self_update()
            if success:
                logger.info("Restarting AeroHub Core after self-update...")
                new_args = [arg for arg in sys.argv[1:] if arg != "--self-update"]
                os.execv(sys.executable, [sys.executable, sys.argv[0]] + new_args)
            sys.exit(0 if success else 1)

        check_admin_and_elevate(args.no_uac, args.headless or args.service)
        app = AeroHubCore(headless=(args.headless or args.service))
        app.run()
    except Exception:
        import traceback

        with open(
            os.path.join(LOGS_DIR, "aerohub_crash.log"), "w", encoding="utf-8"
        ) as f:
            f.write(f"Crash at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            traceback.print_exc(file=f)
        try:
            logger.exception("AeroHub crashed on startup:")
        except Exception:
            pass
        sys.exit(1)
