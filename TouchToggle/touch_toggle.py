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

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing dependencies. Run: pip install pystray Pillow")
    sys.exit(1)

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOGGLES_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR = os.path.dirname(TOGGLES_DIR)
PS1_PATH = os.path.join(SCRIPT_DIR, "TouchToggle.ps1")
LOGS_DIR = r"c:\Users\NANDHA A\Desktop\UTILITIES\Logs"
LOG_PATH = os.path.join(LOGS_DIR, "touch_toggle.log")

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
        logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=2*1024*1024, backupCount=2, encoding="utf-8"),
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
    "toast_anim_style": "Slide",
    "toast_width": 260,
    "toast_height": 60,
    "toast_bg_color": "#18181B",
    "toast_fg_color": "#FFFFFF",
    "toast_font_size": 11,
    "toast_font_weight": "bold",
    "toast_emoji": "🖐️",
    "toast_radius": 15,
    "toast_padding_x": 12,
    "toast_padding_y": 10,
    "toast_opacity": 0.95,
    "toast_border_width": 1,
    "toast_border_color": "#27272A",
    "toast_enable_sound": False
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
    "border": "#333333"
}

def apply_dwm_rounding(window):
    try:
        import ctypes
        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        value = ctypes.c_int(2)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, ctypes.byref(value), ctypes.sizeof(value))
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

        try: apply_dwm_rounding(root)
        except Exception: pass

        def on_closing():
            if hasattr(self, 'preview_instance') and self.preview_instance and hasattr(self.preview_instance, 'force_close'):
                self.preview_instance.force_close()
            root.grab_release()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)

        main_container = tk.Frame(root, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=180)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="TOUCH.SYS", font=("Consolas", 16, "bold"), bg=TH["bg2"], fg=TH["accent"]).pack(pady=(30, 40))

        tk.Button(
            self.sidebar, text="[ SAVE_CFG ]", font=("Consolas", 12, "bold"),
            bg=TH["bg3"], fg=TH["accent"], activebackground=TH["bg"], activeforeground=TH["accent"],
            relief=tk.FLAT, cursor="hand2", command=lambda: self._save_and_close(root)
        ).pack(side=tk.BOTTOM, pady=20, padx=20, fill=tk.X)

        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(self.content_area, text="UI / UX CONFIG", font=("Consolas", 14, "bold"), bg=TH["bg"], fg=TH["fg"]).pack(anchor=tk.W, pady=(0, 10))
        
        f2_left = tk.Frame(self.content_area, bg=TH["bg"])
        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        f2_right = tk.Frame(self.content_area, bg=TH["bg"])
        f2_right.pack(side=tk.LEFT, fill=tk.Y)

        self._add_combo(f2_left, "Position:", "toast_pos", 0, ["Left", "Center", "Right"])
        self._add_combo(f2_left, "Animation:", "toast_anim_style", 1, ["Slide", "Fade"])
        self._add_field(f2_left, "Width (px):", "toast_width", 2)
        self._add_field(f2_left, "Height (px):", "toast_height", 3)
        self._add_color_field(f2_left, "Background:", "toast_bg_color", 4)
        self._add_color_field(f2_left, "Text Color:", "toast_fg_color", 5)
        self._add_field(f2_left, "Font Size:", "toast_font_size", 6)
        self._add_combo(f2_left, "Font Weight:", "toast_font_weight", 7, ["normal", "bold"])
        
        self._add_field(f2_right, "Emoji Icon:", "toast_emoji", 0, is_str=True)
        self._add_field(f2_right, "Radius (px):", "toast_radius", 1)
        self._add_field(f2_right, "Padding X:", "toast_padding_x", 2)
        self._add_field(f2_right, "Padding Y:", "toast_padding_y", 3)
        self._add_field(f2_right, "Opacity:", "toast_opacity", 4)
        self._add_field(f2_right, "Border Width:", "toast_border_width", 5)
        self._add_color_field(f2_right, "Border Color:", "toast_border_color", 6)
        
        btn_frame = tk.Frame(self.content_area, bg=TH["bg"])
        btn_frame.pack(fill=tk.X, pady=20, side=tk.BOTTOM)
        
        tk.Button(
            btn_frame, text="[ PREVIEW_UI ]", font=("Consolas", 10, "bold"),
            bg=TH["bg2"], fg=TH["accent"], activebackground=TH["bg3"], activeforeground=TH["accent"],
            relief=tk.FLAT, cursor="hand2", command=self._preview_toast, padx=20, pady=8,
        ).pack(side=tk.RIGHT)

    def _add_field(self, parent_frame, label, key, row, is_str=False):
        tk.Label(parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))
        tk.Entry(parent_frame, textvariable=var, font=("Consolas", 10), bg=TH["bg"], fg=TH["fg"], insertbackground=TH["accent"], relief=tk.FLAT, highlightthickness=1, highlightcolor=TH["accent"], highlightbackground=TH["border"], width=10).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, is_str)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_combo(self, parent_frame, label, key, row, values):
        tk.Label(parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=self.settings.get(key, values[0]))
        ttk.Combobox(parent_frame, textvariable=var, values=values, font=("Consolas", 10), state="readonly", width=8).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_color_field(self, parent_frame, label, key, row):
        tk.Label(parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=self.settings.get(key, "#ffffff"))
        def choose_color(v=var):
            color_code = colorchooser.askcolor(title="Choose color", initialcolor=v.get())[1]
            if color_code:
                v.set(color_code)
                btn.config(bg=color_code)
        btn = tk.Button(parent_frame, bg=var.get(), width=6, relief=tk.FLAT, cursor="hand2", command=choose_color)
        btn.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _schedule_preview(self):
        if hasattr(self, '_preview_timer') and self._preview_timer:
            try: self.parent.after_cancel(self._preview_timer)
            except Exception: pass
        self._preview_timer = self.parent.after(400, self._preview_toast)

    def _preview_toast(self):
        temp_settings = dict(self.settings)
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if key in ("toast_opacity",): temp_settings[key] = float(val)
                elif not var_type: temp_settings[key] = int(val)
                else: temp_settings[key] = val
            except ValueError: pass
        
        # Save temp settings, launch preview
        with open(os.path.join(SCRIPT_DIR, "temp_preview.json"), "w") as f:
            json.dump(temp_settings, f)
            
        notifier_script = os.path.join(SCRIPT_DIR, "tooltip_notifier.py")
        subprocess.Popen(["pythonw", notifier_script, "Preview Toast", "on", "1"], creationflags=subprocess.CREATE_NO_WINDOW)

    def _save_and_close(self, root):
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if key in ("toast_opacity",): self.settings[key] = float(val)
                elif not var_type: self.settings[key] = int(val)
                else: self.settings[key] = val
            except ValueError: pass
        save_settings(self.settings)
        self.on_save(self.settings)
        root.grab_release()
        root.destroy()


def create_icon_image(enabled: bool) -> Image.Image:
    """Draw a tray icon showing touch ON (green) or OFF (red)."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle
    color = (50, 205, 50, 255) if enabled else (255, 0, 0, 255) # LimeGreen / Red
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



import queue
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
                "powershell", "-NoProfile", "-Command",
                "Get-PnpDevice -Class 'HIDClass' | Where-Object FriendlyName -match 'touch screen' | Select-Object -ExpandProperty Status"
            ],
            capture_output=True, text=True, timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW
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
    """Show a custom floating tooltip notification above the taskbar using a separate process."""
    try:
        notifier_script = os.path.join(SCRIPT_DIR, "tooltip_notifier.py")
        subprocess.Popen(
            ["pythonw", notifier_script, text, state],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        logger.error(f"Failed to spawn tooltip: {e}")

def toggle_touch():
    """Run the PowerShell toggle script elevated via ShellExecuteExW (runas)."""
    global touch_enabled, tray_icon
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
            logger.info(f"Already running as admin. Executing PowerShell script directly: {PS1_PATH}")
            subprocess.run(
                [
                    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-WindowStyle", "Hidden", "-File", PS1_PATH
                ],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            logger.info("Direct PowerShell script execution completed.")
        else:
            logger.info(f"Not running as admin. Executing elevated PowerShell script via ShellExecuteExW: {PS1_PATH}")

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
                    ctypes.c_void_p(sei.hProcess),
                    INFINITE
                )
                ctypes.windll.kernel32.CloseHandle(
                    ctypes.c_void_p(sei.hProcess)
                )
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
                logger.info(f"--- PS1 Log Output ---\n{log_content}----------------------")
            except Exception as e1:
                try:
                    with open(ps1_log_path, "r", encoding="utf-8") as f:
                        log_content = f.read()
                    logger.info(f"--- PS1 Log Output (UTF-8 fallback) ---\n{log_content}----------------------")
                except Exception as e2:
                    logger.error(f"Failed to read PS1 log file: {e1} / {e2}")
        else:
            logger.warning(f"touch_toggle_run.log not found at: {ps1_log_path}")

        # Re-check state
        touch_enabled = check_touch_state()
        logger.info(f"Touch screen is now: {'ENABLED' if touch_enabled else 'DISABLED'}")

        # Update icon
        if tray_icon:
            tray_icon.icon = create_icon_image(touch_enabled)
            state_str = "ON" if touch_enabled else "OFF"
            tray_icon.title = f"Touch: {state_str}"
            tray_icon.menu = create_menu()

            # Show tooltip notification
            show_tooltip(f"Touch Screen is now {state_str}", "on" if touch_enabled else "off")

    except Exception as e:
        logger.error(f"Toggle failed: {e}")


def on_toggle(icon, item):
    """Menu callback for toggle action."""
    threading.Thread(target=toggle_touch, daemon=True).start()


def on_quit(icon, item):
    """Quit the tray app."""
    logger.info("Quitting Touch Toggle tray app.")
    icon.stop()
    if tk_root: tk_root.quit()


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
    
    tk_root.after(100, _process_gui_queue_loop)
    tk_root.mainloop()


if __name__ == "__main__":
    main()
